<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Connect React and Django</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to send
the current conversation to Django, append the generated response, and recover
from a failed asynchronous request.

## Keep the request in a service module

The page should manage interface state. A service module should know the URL,
HTTP method, headers, and JSON body.

Create `src/services/ai.js`.

Begin with the endpoint URL:

```javascript
const BASE_URL = `${import.meta.env.VITE_BACK_END_SERVER_URL}/ai/ask`
```

This environment variable contains only our Django origin. It does not contain
the Gemini key.

## Begin the service function

Below the URL, add:

```javascript
const sendMessage = async (messages) => {
```

Inside the function, begin the request:

```javascript
const response = await fetch(BASE_URL, {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ messages }),
})
```

The bearer token authenticates the Hoot user. The JSON body matches the API
contract tested in Postman.

## Read both success and error JSON

After the `fetch`, parse the response:

```javascript
const data = await response.json()
```

`fetch` does not throw merely because a server returns `400`, `401`, `429`, or
`502`. Check the status explicitly:

```javascript
if (!response.ok) {
  throw new Error(data.err || 'The AI assistant could not answer.')
}
```

Return successful data after the check:

```javascript
return data
```

Close the function and export it:

```javascript
}

export {
  sendMessage,
}
```

The completed service returns `{ reply: '...' }` for success and throws an
`Error` for a handled backend failure.

## Import the service into the page

Open `src/pages/AIHelper.jsx`. Beneath the `useState` import, add:

```javascript
import * as aiService from '../services/ai'
```

The namespace name tells us which module owns `sendMessage` when we call it.

## Add request state one variable at a time

Inside the component, add:

```javascript
const [isSending, setIsSending] = useState(false)
```

`isSending` will prevent duplicate submissions and let the interface show that
work is in progress.

Add a separate error state:

```javascript
const [errorMessage, setErrorMessage] = useState('')
```

The error is not part of the conversation. Keeping it separate means we can
clear or replace it without changing successful messages.

### Stop and inspect the initial values

Use React Developer Tools to select `AIHelper`. Confirm that:

- `isSending` begins as `false`.
- `errorMessage` begins as an empty string.

## Prepare the submit handler for an asynchronous request

Change the function declaration:

```javascript
const handleSubmit = async (event) => {
```

Extend the existing guard:

```javascript
if (!trimmedMessage || isSending) {
  return
}
```

The second condition prevents a rapid double click from starting overlapping
requests that could return out of order.

Keep the existing `userMessage` and `nextMessages` code. Immediately after
those variables, keep the optimistic updates:

```javascript
setMessages(nextMessages)
setFormData('')
```

The word *optimistic* means the interface displays the user's message before the
server finishes. The application already knows what the user typed, so it does
not need to wait to display it.

Reset the old error and mark the request as active:

```javascript
setErrorMessage('')
setIsSending(true)
```

## Call the service before handling the reply

After those state updates, add:

```javascript
try {
  const data = await aiService.sendMessage(nextMessages)
  console.log('AI response:', data)
}
```

The request uses `nextMessages`, not `messages`. A state setter schedules a
render; it does not immediately change the `messages` variable in the currently
running function. `nextMessages` already contains the new question.

The `try` statement is not complete without `catch` or `finally`. For this
temporary checkpoint, immediately add:

```javascript
catch (error) {
  console.error(error)
} finally {
  setIsSending(false)
}
```

### Stop and inspect the first browser request

1. Keep Django and Vite running.
2. Open the browser Network panel.
3. Enter a question and select **SEND**.
4. Select the `ai/ask` request.
5. Inspect the request payload and confirm it contains `messages`.
6. Inspect the request headers and confirm they contain `Authorization`.
7. Confirm that the response contains `reply`.
8. Confirm that the browser console logs the same object.

The generated response does not render yet. This checkpoint isolates the
service from the next state update. Refresh the page before this first request
if Fast Refresh preserved user-only messages from the previous lesson.

Remove the temporary `console.log` after the check. Keep `console.error` until
we replace the failure behavior below.

## Build the assistant message

Inside `try`, immediately after the `await`, add:

```javascript
const assistantMessage = {
  role: 'assistant',
  text: data.reply,
}
```

Append that object to the same request history:

```javascript
setMessages([...nextMessages, assistantMessage])
```

This order creates the alternating sequence expected by Django:

1. Existing messages.
2. New user message.
3. New assistant message.

### Stop and check a full turn

Ask one question. Confirm that:

- The user message renders immediately.
- The generated message appears only after the request completes.
- React Developer Tools shows two message objects in order.

Ask a follow-up question. In the Network panel, inspect the second payload. It
should contain all three messages sent to Django: the first user message, the
first assistant message, and the new user message.

## Recover from a failed request

Replace the temporary `catch` contents with:

```javascript
setMessages(messages)
setFormData(trimmedMessage)
setErrorMessage(error.message)
```

This deliberately restores the state from before the failed request:

- The optimistic user message is removed so the role order remains valid.
- The text returns to the field so the user can retry it.
- The readable error is saved for display.

Keep the `finally` block:

```javascript
finally {
  setIsSending(false)
}
```

`finally` runs after either success or failure, so the interface does not remain
stuck in a sending state.

### Stop and force an error

Temporarily stop Django. Enter a question and select **SEND**.

Confirm in React Developer Tools that:

- `isSending` returns to `false`.
- The earlier successful messages remain.
- The failed question returns to `formData`.
- `errorMessage` contains a network error.

Restart Django and submit the restored question again. It should succeed.

## Use request state in the button

Change the submit button's opening tag:

```javascript
<button
  type="submit"
  disabled={!formData.trim() || isSending}
>
```

Change its label:

```javascript
{isSending ? 'SENDING...' : 'SEND'}
```

Now the button describes and enforces the state already managed by the
function. In the next lesson, we will add the remaining visible feedback and
finish the layout.
