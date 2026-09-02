<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Instructor Guide</span>
</h1>

## Lesson purpose

This lesson introduces AI as a third-party API integration rather than as a
special category of frontend feature. The central learning goals are boundary
design, secret handling, translating API documentation, validating untrusted
input, and managing an asynchronous user flow.

Authentication, Hoot CRUD, comments, models, and serializers are already
complete. Do not rebuild them during this lesson.

## Provider rationale

The lesson uses Gemini because its current free tier, Bahrain availability,
official Python SDK, and stable Flash-Lite model make it more approachable for a
cohort than a pay-as-you-go gateway. The model is configured through
`GEMINI_MODEL` so it can be replaced without rewriting the view if provider
availability changes.

Before delivery, verify:

1. Bahrain remains on the provider's supported-region list.
2. `gemini-3.5-flash-lite` still has a free tier.
3. A new student account can create a key without enabling billing.
4. The installed `google-genai` major version remains compatible with the
   lesson.
5. One complete one-message and three-message request works from the classroom
   network.

## Suggested pacing

| Segment | Time | Instructor emphasis |
| ------- | :--: | ------------------- |
| Concepts and provider decision | 20 min | Trace the key and data boundaries. |
| Account and SDK setup | 20 min | Never display or commit a real key. |
| Page, route, and link scaffold | 20 min | Check each layer before adding state. |
| Temporary Django endpoint | 15 min | Prove routing and authentication first. |
| Validation and translation | 20 min | Inspect one concept at a time in Postman. |
| Provider call | 20 min | Read the official method and response shape. |
| Local React state | 35 min | Make state observable before networking. |
| Service and asynchronous flow | 35 min | Explain `nextMessages` and failed-request rollback. |
| Feedback, styling, and review | 25 min | Test success, failure, follow-up, and clear flows. |

The total is approximately 3 hours 30 minutes. The backend Postman checkpoints
and the frontend state checkpoints are natural places for a short break.

## Recommended live-code order

Keep this order even if students suggest jumping directly to the provider:

1. Scaffold `AIHelper.jsx`.
2. Add `/ai-helper` inside the protected route group.
3. Add the **AI HELPER** navigation link.
4. Return a fixed response from `/ai/ask`.
5. Prove `401` without a token and `200` with a token.
6. Validate the outer list and each message.
7. Translate `assistant` to Gemini's `model` role.
8. Make one real provider request in Postman.
9. Build the controlled field and local message array.
10. Inspect local state before adding a service.
11. Add the service request and inspect the Network panel.
12. Append the provider reply.
13. Add rollback, waiting, error, and clear states.
14. Style only after the data flow is complete.

This sequence narrows the possible cause whenever a check fails.

## Questions to ask at checkpoints

### After the architecture section

- What code reaches the browser?
- Which server has permission to read the provider key?
- Why is a free tier still a resource we should limit?

### After the temporary endpoint

- What did the `401` prove?
- Why can the view rely on the project's default permission?
- What have we tested without involving Gemini?

### After validation

- Why do we validate data created by our own React application?
- Why does a valid request end with the `user` role?
- Why is nine a useful first limit for an alternating sequence?

### After local state

- Why do we replace the array instead of calling `push`?
- What does the controlled field prove before a network request exists?
- Why is the error stored separately from messages?

### After the service connection

- Why does the request use `nextMessages` instead of `messages`?
- What would happen if the user could submit twice while a request was active?
- Why does the failure path restore the prompt and earlier array?

## Common issues

| Symptom | Likely cause | Fast check |
| ------- | ------------ | ---------- |
| `ModuleNotFoundError: google` | SDK installed outside the active environment | Check the environment path and run the import command. |
| `bool(settings.GEMINI_API_KEY)` is `False` | Wrong `.env` location or server not restarted | Place `.env` beside `manage.py`; restart. |
| `401` in Postman or browser | Missing, expired, or malformed bearer token | Inspect the exact `Authorization` header. |
| `400` role error on a retry | Failed user message remained in state | Restore the previous `messages` array in `catch`. |
| `429` in the Django terminal | Provider free-tier limit | Pause requests and inspect AI Studio usage. |
| `502` from Django | Provider key, model, quota, or transient error | Read the provider code logged in the terminal. |
| Browser receives a network error | Django stopped, wrong frontend environment value, or CORS | Test `/ai/ask` in Postman and inspect the request URL. |
| Follow-up ignores context | Only the newest text was sent | Inspect the Network payload for the full recent sequence. |
| Clearing during a request is undone | Clear button remained enabled | Disable clear while `isSending` is true. |

## Classroom fallback

If account creation or provider quota blocks the cohort, keep the same API
contract and temporarily return a deterministic response after validation:

```python
latest_question = messages[-1]["text"]
return Response({
    "reply": f"Temporary classroom response to: {latest_question}"
})
```

Students can complete the React state, service, loading, and error work against
this response. Restore the real provider call for the instructor demonstration
and final solution. Describe the fallback honestly; it does not test the
external integration.

## Security and privacy notes

- Do not provide one unrestricted instructor key to the whole cohort.
- Do not ask students to show their full `.env` or key on screen.
- If a key appears in a commit, replace it before removing it from Git history.
- Use fictional prompts because free-tier data may be used to improve provider
  products.
- The system instruction is guidance, not a security boundary.
- Authentication does not replace throttling. A production version needs
  per-user and global request controls.

## Solution verification

The solution backend contains provider-independent tests that mock the Gemini
client. From `solution-code/hoot-backend`, run:

```bash
python manage.py test
```

The tests check empty-message rejection and the successful response shape. A
real key is still required for the manual Postman and browser flows.

The solution frontend should also pass:

```bash
npm run build
npm run lint
```

## Assessment evidence

A student has met the core objectives when they can:

- Explain why the key is absent from React.
- Show a protected `POST /ai/ask` request in Postman.
- Identify the application-to-provider role translation.
- Show a second browser request containing earlier messages.
- Demonstrate waiting, success, failure, and clear states.
- State that the provider does not automatically have access to the Hoot
  database.
