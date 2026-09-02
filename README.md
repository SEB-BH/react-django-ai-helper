<h1>
  <span class="prefix"></span>
  <span class="headline">Django + React</span>
  <span class="subhead">Build an AI Helper</span>
</h1>

## About

In this lesson, we will add a conversational AI helper to the completed Hoot
application. A signed-in user will be able to open a dedicated page, submit a
question, receive a generated response, and ask follow-up questions that use the
recent conversation as context.

We will keep the Gemini API key in Django. React will communicate only with our
own protected Django REST Framework endpoint, and Django will communicate with
Gemini. This structure protects the key and gives our application one place to
validate requests and handle provider errors.

The work will be built in small, testable steps. We will scaffold the page before
adding its route and navigation link, inspect state before calling an external
service, test the Django endpoint in Postman, and connect the two applications
only after each side works independently.

## Learning objectives

By the end of this lesson, students will be able to:

- Explain why a third-party API key belongs on the backend.
- Translate application message objects into the shape expected by an AI API.
- Build and test a protected DRF endpoint that calls an external service.
- Manage a multi-turn conversation with React state.
- Represent waiting, success, empty, and error states in the interface.
- Identify privacy, cost, and reliability concerns in an AI integration.

## The feature

A signed-in user will be able to:

1. Select **AI HELPER** in the navigation.
2. Enter a question on the Hoot AI Helper page.
3. See the question appear immediately.
4. Wait while Django asks Gemini for a response.
5. See the response appear beneath the question.
6. Ask a follow-up question that includes recent messages as context.
7. Clear the current conversation.

## Content

| Lesson | Estimated time | Skills |
| ------ | :------------: | ------ |
| [Concepts and architecture](./concepts-and-architecture/README.md) | 20 min | Evaluate the provider and trace the request flow. |
| [Set up Gemini](./setup/README.md) | 20 min | Create a key, install the SDK, and configure Django. |
| [Scaffold the AI Helper](./scaffold-ai-helper/README.md) | 20 min | Create the page, protected route, and navigation link. |
| [Build the Django endpoint](./backend-ai-endpoint/README.md) | 55 min | Inspect input, validate messages, call Gemini, and test with Postman. |
| [Build the conversation state](./conversation-state/README.md) | 35 min | Use controlled input and inspect state changes. |
| [Connect the applications](./connect-the-app/README.md) | 35 min | Build the service and handle an asynchronous request. |
| [Finish and review](./finish-and-review/README.md) | 25 min | Add feedback states, styling, final checks, and level-ups. |
| **Total** | **3 hr 30 min** | |

## Starter and solution code

- [Starter Hoot frontend](./starter-code/hoot-frontend)
- [Starter Hoot backend](./starter-code/hoot-backend)
- [Completed Hoot frontend](./solution-code/hoot-frontend)
- [Completed Hoot backend](./solution-code/hoot-backend)

The starter applications already include authentication, Hoot CRUD, and
comments. We will add only the AI Helper feature.

## Prerequisites

Students should already be able to:

- Run the Hoot React frontend and Django backend locally.
- Sign up, sign in, and send a JWT in an `Authorization` header.
- Create a protected function-based DRF view and URL pattern.
- Build a controlled React form with `useState`.
- Call a backend service with `fetch` and `async`/`await`.
- Inspect requests in Postman and the browser developer tools.

## References

📖 [Reference materials](./references/README.md)

## Internal

✏️ [Instructor guide](./internal-resources/instructor-guide.md)
