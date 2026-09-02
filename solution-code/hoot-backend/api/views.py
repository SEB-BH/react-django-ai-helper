from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from google import genai
from google.genai import errors, types
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Hoot, Comment
from .serializers import UserSerializer, HootSerializer, CommentSerializer


MAX_AI_MESSAGES = 9
MAX_AI_MESSAGE_LENGTH = 2000
SYSTEM_INSTRUCTION = (
    "You are Hoot Helper, a friendly assistant inside a social app. "
    "Give clear, concise answers. If you are unsure, say so. "
    "Do not claim to have access to Hoot posts or private user data."
)


def validate_ai_messages(messages):
    if not isinstance(messages, list) or not messages:
        return "Send at least one message."

    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            return "Each message must be an object."

        expected_role = "user" if index % 2 == 0 else "assistant"

        if message.get("role") != expected_role:
            return "Messages must alternate between user and assistant."

        text = message.get("text")

        if not isinstance(text, str) or not text.strip():
            return "Each message must include text."

        if len(text) > MAX_AI_MESSAGE_LENGTH:
            return "Each message must be 2,000 characters or fewer."

    if messages[-1]["role"] != "user":
        return "The final message must come from the user."

    return None


def build_gemini_contents(messages):
    contents = []

    for message in messages:
        gemini_role = "model" if message["role"] == "assistant" else "user"
        content = types.Content(
            role=gemini_role,
            parts=[types.Part.from_text(text=message["text"].strip())],
        )
        contents.append(content)

    return contents


def create_access_token(user):
    token = RefreshToken.for_user(user).access_token
    token["payload"] = {
        "_id": str(user.id),
        "username": user.username
    }
    return str(token)


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    confirm_password = request.data.get("confirmPassword", "")

    if not username or not password:
        return Response(
            {"err": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if password != confirm_password:
        return Response(
            {"err": "Passwords do not match."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"err": "That username is already taken."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, password=password)
    token = create_access_token(user)

    return Response({"token": token}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"err": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = create_access_token(user)
    return Response({"token": token})


@api_view(["GET"])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def ai_helper(request):
    messages = request.data.get("messages")

    if not isinstance(messages, list):
        return Response(
            {"err": "Messages must be sent as a list."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    messages = messages[-MAX_AI_MESSAGES:]
    validation_error = validate_ai_messages(messages)

    if validation_error:
        return Response(
            {"err": validation_error},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.GEMINI_API_KEY:
        return Response(
            {"err": "The AI service has not been configured."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    contents = build_gemini_contents(messages)
    generation_config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        max_output_tokens=500,
        temperature=0.7,
    )

    try:
        with genai.Client(api_key=settings.GEMINI_API_KEY) as client:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=generation_config,
            )
    except errors.APIError as error:
        print(f"Gemini API error: {error.code} {error.message}")
        return Response(
            {"err": "The AI service is unavailable. Please try again."},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    reply = (response.text or "").strip()

    if not reply:
        return Response(
            {"err": "The AI service returned an empty response."},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response({"reply": reply})


@api_view(["GET", "POST"])
def hoot_list_create(request):
    # getting hoot index
    if request.method == "GET":
        hoots = Hoot.objects.all()
        serializer = HootSerializer(hoots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # otherwise create a hoot
    serializer = HootSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "PUT", "DELETE"])
def hoot_detail(request, hoot_id):
    hoot = get_object_or_404(Hoot, pk=hoot_id)

    if request.method == "GET":
        serializer = HootSerializer(hoot)
        return Response(serializer.data)

    if hoot.author != request.user:
        return Response(
            {"err": "You can only change your own hoots."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PUT":
        serializer = HootSerializer(hoot, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    deleted_id = str(hoot.id)
    hoot.delete()
    return Response({"message": "Hoot deleted", "_id": deleted_id})


@api_view(["POST"])
def comment_create(request, hoot_id):
    hoot = get_object_or_404(Hoot, pk=hoot_id)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user, hoot=hoot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def comment_detail(request, hoot_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, hoot_id=hoot_id)

    if comment.author != request.user:
        return Response(
            {"err": "You can only change your own comments."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    deleted_id = str(comment.id)
    comment.delete()
    return Response({"message": "Comment deleted", "_id": deleted_id})
