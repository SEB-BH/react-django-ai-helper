# Solution code

This directory contains the completed AI Helper implementation:

- `hoot-frontend`: `AIHelper.jsx`, `/ai-helper`, the AI service, and interface
  states
- `hoot-backend`: `/ai/ask`, validation, Gemini translation, provider handling,
  and introductory tests

Create local `.env` files from the examples. A real Gemini API key is required
for manual provider requests; the backend tests mock the provider client and do
not use quota.
