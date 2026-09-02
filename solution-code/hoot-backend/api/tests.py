from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase


class AIHelperTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)

    def test_rejects_an_empty_message_list(self):
        response = self.client.post(
            "/ai/ask",
            {"messages": []},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(
        GEMINI_API_KEY="test-key",
        GEMINI_MODEL="gemini-test-model",
    )
    @patch("api.views.genai.Client")
    def test_returns_the_model_reply(self, mock_client_class):
        mock_response = MagicMock()
        mock_response.text = "Hello from the model"

        mock_client = mock_client_class.return_value.__enter__.return_value
        mock_client.models.generate_content.return_value = mock_response

        response = self.client.post(
            "/ai/ask",
            {
                "messages": [
                    {"role": "user", "text": "Hello"},
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"reply": "Hello from the model"})
