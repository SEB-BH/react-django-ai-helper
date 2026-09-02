<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Concepts and Architecture</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to
explain how a React application can use a backend to communicate safely with an
AI provider.

## What are we integrating?

A generative AI model accepts input and generates a response based on patterns
learned during training. We do not run that model inside Hoot. Instead, Hoot will
send an HTTPS request to an AI provider and receive JSON in return.

This is still a third-party API integration. The provider happens to perform a
more open-ended task than APIs we may have used for weather, maps, or payments.

Our application must still decide:

- What data to send.
- Where to keep the API key.
- How to translate between our data shape and the provider's data shape.
- What to do while the provider is working.
- What to do when the provider rejects or cannot complete a request.

## Provider choice: Gemini

We will use Google's Gemini Developer API and the official `google-genai` Python
package.

Gemini is a better classroom fit than Eden AI for this lesson because:

- Gemini has a documented free tier for supported text models.
- New accounts begin on the free tier; moving to a paid tier is a separate
  billing action.
- Google AI Studio and the Gemini API are available in Bahrain.
- Google supplies an official Python SDK and clear multi-turn examples.
- A stable Flash-Lite model is fast and sufficient for short classroom prompts.

Eden AI is useful when an application needs one gateway for many AI providers,
but its current standard pricing is pay-as-you-go plus a platform fee. Trial
credits are less suitable for a lesson that should remain repeatable for a whole
cohort.

> **Important:** Google states that free-tier content may be used to improve its
> products. Use made-up classroom content. Do not submit passwords, personal
> information, unpublished client information, or other sensitive data.

## Decide where the API call belongs

It may seem convenient to call Gemini directly from React, but browser code is
delivered to the user. Any key stored in a `VITE_` environment variable becomes
part of the frontend build and can be recovered from the browser.

The request will therefore travel through both Hoot applications:

1. React stores the visible conversation in state.
2. React sends the messages and the user's JWT to Django.
3. DRF authenticates the user and validates the message data.
4. Django reads the Gemini key from its server-side environment.
5. Django translates the messages and calls Gemini.
6. Django returns only `{ "reply": "..." }` to React.
7. React adds the reply to state and renders it.

This gives the browser the result without giving it the provider key.

## Two message shapes

Our React application and Gemini use slightly different role names.

| Meaning | React role | Gemini role |
| ------- | ---------- | ----------- |
| The signed-in person wrote the message | `user` | `user` |
| The AI generated the message | `assistant` | `model` |

React will store a message like this:

```javascript
{
  role: 'assistant',
  text: 'A serializer changes complex Django data into JSON-friendly data.'
}
```

Django will translate that object into a Gemini `Content` object before making
the external request.

## Where does the memory come from?

The model does not automatically remember a previous HTTP request. React will
send the recent message history each time the user asks a question.

For example, the second request may contain:

```json
{
  "messages": [
    { "role": "user", "text": "What does a serializer do?" },
    { "role": "assistant", "text": "It translates complex data." },
    { "role": "user", "text": "Can you give me an example?" }
  ]
}
```

Because the request includes the earlier exchange, Gemini can understand what
"it" refers to in the follow-up question.

We will send only the nine most recent messages. Limiting the history keeps the
request small and demonstrates that AI usage grows with the amount of text sent
and generated.

## Check your understanding

Before continuing, answer these questions with a partner:

1. Why would `VITE_GEMINI_API_KEY` expose the provider key?
2. Which application is responsible for authenticating the Hoot user?
3. Which application translates `assistant` into `model`?
4. Why must each new request include recent messages?
5. What kinds of information should not be entered while using the free tier?
