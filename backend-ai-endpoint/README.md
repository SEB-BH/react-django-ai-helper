<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Build the Django Endpoint</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to
build and test a protected DRF endpoint that validates conversation messages,
translates them for Gemini, and returns a generated reply.

## Define the API contract

Before writing the view, decide what React will send and what Django will
return.

### Request

- Method: `POST`
- Path: `/ai/ask`
- Authentication: existing Hoot bearer token
- JSON body:

```json
{
  "messages": [
    { "role": "user", "text": "What is Django?" }
  ]
}
```

### Successful response

- Status: `200 OK`
- JSON body:

```json
{
  "reply": "Django is a Python web framework..."
}
```

Defining this shape first lets us test the Django and React sides separately.

## Scaffold the view with a temporary response

Open `api/views.py`. Below `user_list`, add:

```python
@api_view(["POST"])
def ai_helper(request):
    messages = request.data.get("messages")
    print("AI messages received:", messages)

    return Response({"reply": "Django received the request."})
```

This first version does not use Gemini. It proves that DRF can receive the
expected JSON.

We do not add `@permission_classes([AllowAny])`. The project's default DRF
permission is `IsAuthenticated`, so this endpoint automatically requires the
existing JWT.

## Register the backend URL

Open `api/urls.py`. Add the path near the other top-level endpoints:

```python
path('ai/ask', views.ai_helper, name="ai-helper"),
```

The React route describes a page, while this URL describes an API action. That
is why the two paths do not need to match.

### Stop and check authentication first

Start Django:

```bash
python manage.py runserver
```

In Postman, send a `POST` request to:

```plaintext
http://localhost:8000/ai/ask
```

Do not add a token yet. Use this JSON body:

```json
{
  "messages": [
    { "role": "user", "text": "What is Django?" }
  ]
}
```

The endpoint should return `401 Unauthorized`. This confirms that it is
protected.

Sign in through `POST /auth/sign-in`, copy the token, and add this header to the
AI request:

```plaintext
Authorization: Bearer YOUR_TOKEN
```

Send the request again. Confirm three results:

1. Postman receives `{ "reply": "Django received the request." }`.
2. The Django terminal prints the message list.
3. The Django request log shows `POST /ai/ask` with status `200`.

If this check fails, fix the route, token, or JSON before adding the provider.

## Validate the outer data shape

The browser is not the only possible API client. Django must not assume that
`messages` is a list just because our React code will send a list.

Inside `ai_helper`, place this immediately after reading `messages`:

```python
if not isinstance(messages, list):
    return Response(
        {"err": "Messages must be sent as a list."},
        status=status.HTTP_400_BAD_REQUEST,
    )
```

### Stop and send deliberately incorrect data

Change the Postman body to:

```json
{
  "messages": "What is Django?"
}
```

The endpoint should return `400 Bad Request` with the error we just wrote.

Change the body back to a list before continuing.

## Limit the conversation size

Near the top of `api/views.py`, below the local imports, add:

```python
MAX_AI_MESSAGES = 9
```

Add a separate limit for each individual message:

```python
MAX_AI_MESSAGE_LENGTH = 2000
```

Back in the view, place this after the list check:

```python
messages = messages[-MAX_AI_MESSAGES:]
```

The negative slice keeps the final nine items. An odd limit is intentional: a
valid request ends with a user message, so an odd-length slice also begins with
a user message.

This is not a complete cost-control system, but it prevents an ever-growing
browser conversation from producing an ever-growing request.

## Begin a validation helper

Above `create_access_token`, add:

```python
def validate_ai_messages(messages):
    if not messages:
        return "Send at least one message."

    return None
```

This function returns an error string when it finds a problem. It returns
`None` when the data is valid.

Call the helper in `ai_helper` after slicing the list:

```python
validation_error = validate_ai_messages(messages)
```

Then respond when an error exists:

```python
if validation_error:
    return Response(
        {"err": validation_error},
        status=status.HTTP_400_BAD_REQUEST,
    )
```

### Stop and check an empty list

Send:

```json
{
  "messages": []
}
```

Confirm that the endpoint returns `400` and `Send at least one message.`

## Inspect each message object

The provider needs messages to alternate between the person and the model. Add
this loop inside `validate_ai_messages`, before `return None`:

```python
for index, message in enumerate(messages):
    if not isinstance(message, dict):
        return "Each message must be an object."

    expected_role = "user" if index % 2 == 0 else "assistant"

    if message.get("role") != expected_role:
        return "Messages must alternate between user and assistant."
```

`enumerate` gives us both the object and its position. Even positions
(`0`, `2`, `4`) belong to the user. Odd positions (`1`, `3`, `5`) belong to the
assistant.

### Stop and check the role order

Send two consecutive user messages:

```json
{
  "messages": [
    { "role": "user", "text": "First question" },
    { "role": "user", "text": "Second question" }
  ]
}
```

Confirm that Django rejects the request before it reaches the external API.

## Validate each message's text

Still inside the loop, after the role check, read the text:

```python
text = message.get("text")
```

Reject missing, non-string, or whitespace-only text:

```python
if not isinstance(text, str) or not text.strip():
    return "Each message must include text."
```

Reject a message that exceeds the frontend limit:

```python
if len(text) > MAX_AI_MESSAGE_LENGTH:
    return "Each message must be 2,000 characters or fewer."
```

After the loop but before `return None`, confirm that the request ends with a
user question:

```python
if messages[-1]["role"] != "user":
    return "The final message must come from the user."
```

### Stop and check blank text

Send:

```json
{
  "messages": [
    { "role": "user", "text": "   " }
  ]
}
```

Django should return `400` and should not call Gemini.

## Translate the messages for Gemini

Add the provider types import near the top of `api/views.py`:

```python
from google.genai import types
```

Create a second helper beneath the validation helper:

```python
def build_gemini_contents(messages):
    contents = []
```

Inside the function, loop over our application messages:

```python
for message in messages:
    gemini_role = "model" if message["role"] == "assistant" else "user"
```

Build one typed Gemini `Content` object:

```python
content = types.Content(
    role=gemini_role,
    parts=[types.Part.from_text(text=message["text"].strip())],
)
```

Add it to the list, then return the completed list after the loop:

```python
contents.append(content)

return contents
```

The indentation should communicate this sequence:

- The function creates one list.
- The loop creates and appends one `Content` object per message.
- The function returns only after the loop finishes.

Call the helper in the view after the key and validation checks:

```python
contents = build_gemini_contents(messages)
```

For one temporary check, print the result:

```python
print("Gemini contents:", contents)
```

Send a valid one-message request in Postman. Confirm that the Django terminal
shows a Gemini `Content` object with the `user` role. Remove the temporary print
after the check.

## Add the system instruction

Near the two limits, add:

```python
SYSTEM_INSTRUCTION = (
    "You are Hoot Helper, a friendly assistant inside a social app. "
    "Give clear, concise answers. If you are unsure, say so. "
    "Do not claim to have access to Hoot posts or private user data."
)
```

A system instruction establishes the assistant's general behavior. It does not
give the model access to the Hoot database. The final sentence makes that
boundary explicit.

## Check the server configuration

Add the Django settings import near the top of the file:

```python
from django.conf import settings
```

In the view, before building the provider contents, add:

```python
if not settings.GEMINI_API_KEY:
    return Response(
        {"err": "The AI service has not been configured."},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
```

`503 Service Unavailable` communicates that the route exists but its required
external service is not currently configured.

### Stop and check the missing-key path

Temporarily comment out `GEMINI_API_KEY` in `.env` and restart Django. Send a
valid request. Confirm that it returns `503` rather than crashing.

Restore the environment variable and restart Django again.

## Configure one generation

After `contents = build_gemini_contents(messages)`, add:

```python
generation_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    max_output_tokens=500,
    temperature=0.7,
)
```

These values mean:

- `system_instruction` supplies the behavior we defined.
- `max_output_tokens` limits the length of the generated result.
- `temperature` allows some variation without making the output extremely
  unpredictable.

The token limit is not exactly 500 words. Tokens may be whole words, pieces of
words, punctuation, or characters.

## Call Gemini

Add the remaining provider imports:

```python
from google import genai
from google.genai import errors, types
```

Because this line includes `types`, remove the earlier standalone `types`
import.

After `generation_config`, open a provider client and call the model:

```python
try:
    with genai.Client(api_key=settings.GEMINI_API_KEY) as client:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=generation_config,
        )
```

The context manager closes the client's network resources after the request.
The call sends the configured model, the translated conversation, and the
generation settings.

Complete the `try` statement by handling provider API errors:

```python
except errors.APIError as error:
    print(f"Gemini API error: {error.code} {error.message}")
    return Response(
        {"err": "The AI service is unavailable. Please try again."},
        status=status.HTTP_502_BAD_GATEWAY,
    )
```

The terminal receives details that help the developer debug. The browser gets a
short provider-neutral message. `502 Bad Gateway` communicates that our server
was working as a gateway to another service and that upstream request failed.

## Return the generated text

After the error handler, read and clean the response text:

```python
reply = (response.text or "").strip()
```

Handle the possibility that the provider returns no visible text:

```python
if not reply:
    return Response(
        {"err": "The AI service returned an empty response."},
        status=status.HTTP_502_BAD_GATEWAY,
    )
```

Return the successful API shape:

```python
return Response({"reply": reply})
```

Remove the original temporary `return Response(...)`. Python must reach only
the appropriate final response.

## Test one complete request

Send this authenticated Postman request:

```json
{
  "messages": [
    {
      "role": "user",
      "text": "Explain a Django serializer in two simple sentences."
    }
  ]
}
```

Confirm that:

- The response status is `200`.
- The JSON has one `reply` key.
- The value was generated rather than hard-coded.
- The API key does not appear in the terminal output or response.

## Test a follow-up question

Copy the first generated response into the `assistant` message below, then send
the three-message request:

```json
{
  "messages": [
    {
      "role": "user",
      "text": "Explain a Django serializer in two simple sentences."
    },
    {
      "role": "assistant",
      "text": "PASTE_THE_FIRST_REPLY_HERE"
    },
    {
      "role": "user",
      "text": "Now give me one small example."
    }
  ]
}
```

The reply should treat the final message as a follow-up. This proves that the
conversation history is reaching the model.

## Read common errors

| Status | Likely meaning | What to check |
| ------ | -------------- | ------------- |
| `400` | Our validation rejected the JSON | List shape, role order, and text |
| `401` | DRF did not authenticate the request | Bearer header and token |
| `429` shown in the Django terminal | Free-tier quota or rate limit reached | Wait, reduce requests, and check AI Studio usage |
| `502` | Gemini rejected or could not complete the request | Terminal error code, key restrictions, model name, and quota |
| `503` | Django did not load a key | `.env` location and server restart |

Do not move on until a one-message request and a three-message follow-up both
work in Postman.
