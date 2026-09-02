<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Reference Materials</span>
</h1>

## Gemini documentation

- [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)
  lists the free and paid tiers by model. The lesson uses
  `gemini-3.5-flash-lite`, which is listed with free-tier text input and output.
- [Gemini API billing](https://ai.google.dev/gemini-api/docs/billing) explains
  that new accounts begin on the free tier and that moving to a paid tier is a
  separate billing setup.
- [Available regions](https://ai.google.dev/gemini-api/docs/available-regions)
  lists Bahrain as supported for Google AI Studio and the Gemini API.
- [API key guidance](https://ai.google.dev/gemini-api/docs/api-key) covers
  environment variables, restrictions, and the steps to take after a leak.
- [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/) documents
  `Client`, typed `Content` objects, generation configuration, context managers,
  and `APIError`.
- [Google Gen AI on PyPI](https://pypi.org/project/google-genai/) lists the
  current package release and supported Python versions. This lesson targets
  version 2 of the SDK.
- [Text generation](https://ai.google.dev/gemini-api/docs/generate-content/text-generation)
  explains message history, `user` and `model` roles, and multi-turn requests.
- [Models](https://ai.google.dev/gemini-api/docs/models) lists current model IDs
  and capabilities.
- [Troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting)
  explains common status codes, quotas, and automatic retry behavior in the
  official SDK.

## Provider comparison

- [Eden AI pricing](https://www.edenai.co/pricing) describes its API gateway as
  pay-as-you-go with a platform fee. It is useful for accessing many providers
  through one interface, but it does not provide the same durable free-tier fit
  for this cohort lesson.

## Privacy reminder

The Gemini pricing page states that free-tier content may be used to improve
Google products. Use fictional or public classroom prompts. Do not send
credentials, personal data, protected student data, or confidential client
material.

Provider models, quotas, prices, and account interfaces can change. Instructors
should review the pricing, model, and regional pages shortly before delivering
the lesson.
