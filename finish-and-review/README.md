<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Finish and Review</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to
complete the helper's feedback states, style the conversation, and verify the
feature from browser to provider and back.

## Announce the waiting state

Open `src/pages/AIHelper.jsx`. Add `aria-busy` to the existing messages section:

```javascript
<section
  className="ai-helper-messages"
  aria-live="polite"
  aria-busy={isSending}
>
```

After the message `map`, but still inside that section, add:

```javascript
{isSending && (
  <p className="ai-helper-status">Hoot Helper is thinking...</p>
)}
```

The user now receives feedback in two places: the button says **SENDING...** and
the message area explains what is happening.

### Stop and check

Submit a question. Confirm that the status appears during the request and is
removed after either success or failure.

## Display the error state

Immediately after the closing tag for the messages section, add:

```javascript
{errorMessage && (
  <p className="ai-helper-error" role="alert">
    {errorMessage}
  </p>
)}
```

`role="alert"` makes an important new error easier for assistive technology to
announce.

Stop Django again and submit a question. Confirm that the error appears in the
page, not only in developer tools. Restart Django after the check.

## Add a clear action

Above `return`, below `handleSubmit`, add:

```javascript
const handleClear = () => {
  setMessages([])
  setFormData('')
  setErrorMessage('')
}
```

The function does not call the backend because the conversation currently
exists only in React state.

Wrap the existing submit button in a new action container:

```javascript
<div className="ai-helper-actions">
  {/* Keep the submit button here. */}
</div>
```

The comment marks the existing button's location. Remove the comment after
placing the button inside the `<div>`.

After the submit button, add a second button:

```javascript
<button
  className="secondary-button"
  type="button"
  disabled={
    isSending || (messages.length === 0 && !errorMessage)
  }
  onClick={handleClear}
>
  CLEAR CONVERSATION
</button>
```

`type="button"` matters. Without it, a button inside a form defaults to submit
behavior.

The button is disabled while a request is active. Otherwise, a late provider
response could repopulate a conversation the user had just cleared.

### Stop and check

1. Complete two turns.
2. Select **CLEAR CONVERSATION**.
3. Confirm that the empty state returns and the input clears.
4. Confirm that the clear button becomes disabled.
5. Confirm that no network request occurs.

## Add the privacy reminder

Below the form but inside the outer page section, add:

```javascript
<p className="ai-helper-note">
  Use test content only. Do not share passwords, personal information,
  or private client data with the AI service.
</p>
```

This reminder is especially important because free-tier provider data may be
used to improve provider products.

## Style the outer helper

Open `src/App.css`. Add:

```css
.ai-helper {
  max-width: 720px;
}
```

The existing `.card` class supplies the surface, border, padding, and shadow.
This class changes only the maximum width.

## Style the message area

Add the layout for the scrolling area:

```css
.ai-helper-messages {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 260px;
  max-height: 480px;
  margin-bottom: 20px;
  padding: 16px;
  overflow-y: auto;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}
```

The column layout lets individual messages align themselves left or right. The
height and `overflow-y` rules keep a longer conversation inside the card.

Style the non-message feedback:

```css
.ai-helper-empty,
.ai-helper-status {
  color: var(--color-text-light);
}
```

Refresh and confirm that the empty state is visually quieter than a message.

## Build the message bubble

Add shared bubble styles:

```css
.ai-message {
  max-width: 80%;
  padding: 12px;
  border-radius: 12px;
}
```

Preserve line breaks in generated text:

```css
.ai-message p {
  margin-bottom: 0;
  white-space: pre-wrap;
}
```

Position and color the user's message:

```css
.ai-message-user {
  align-self: flex-end;
  background-color: var(--color-primary);
  color: white;
}
```

Position and color the assistant message:

```css
.ai-message-assistant {
  align-self: flex-start;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
}
```

The role stored in each message now affects the bubble's label, class, color,
and alignment.

## Style errors and actions

Add the error color:

```css
.ai-helper-error {
  color: var(--color-error);
}
```

Place the two buttons in one row:

```css
.ai-helper-actions {
  display: flex;
  gap: 12px;
}

.ai-helper-actions button {
  flex: 1;
}
```

Give the secondary action a quieter color:

```css
.secondary-button {
  background-color: var(--color-text-light);
}
```

Finish with the privacy note:

```css
.ai-helper-note {
  margin-top: 16px;
  margin-bottom: 0;
  color: var(--color-text-light);
  font-size: 0.85rem;
}
```

## Complete the full user flow

Keep the Django terminal, browser console, and browser Network panel visible.
Complete each check in order:

1. Sign out and confirm that **AI HELPER** is not in the signed-out navigation.
2. Sign in and open `/ai-helper` from the navigation link.
3. Confirm that the empty state and privacy reminder appear.
4. Confirm that the submit button is disabled for an empty or whitespace-only
   prompt.
5. Submit a short question.
6. Confirm that the user bubble appears before the generated bubble.
7. Confirm that the waiting text and disabled buttons appear during the request.
8. Ask a follow-up that depends on the first exchange.
9. Inspect the second request payload and confirm that it contains the recent
   message sequence.
10. Select **CLEAR CONVERSATION** and confirm that the page resets without a
    request.
11. Stop Django, submit a question, and confirm that the question is restored to
    the field with a visible error.
12. Restart Django and confirm that the restored question can be sent.
13. Refresh the page and confirm that the conversation resets. This is the
    intended first-version behavior.

## Review the responsibility of each layer

| Layer | Responsibility |
| ----- | -------------- |
| `AIHelper.jsx` | Input, ordered messages, waiting state, error state, rendering |
| `services/ai.js` | Django URL, JWT header, JSON request, HTTP error conversion |
| `api/urls.py` | Maps `/ai/ask` to the view |
| `api/views.py` | Authentication through DRF defaults, validation, translation, provider call |
| `settings.py` and `.env` | Server-only key and replaceable model name |
| Gemini | Generates text from the system instruction and recent messages |

No database model or migration was required because the first version does not
persist conversations.

## Known limitations

The first version intentionally keeps its scope small:

- Refreshing the page clears the conversation.
- Only the nine most recent messages are sent.
- The browser waits for one complete response rather than receiving a stream.
- Generated text is displayed as plain text rather than rendered Markdown.
- The helper has no automatic access to Hoots, comments, or private user data.
- The free tier has provider-controlled quotas and is not a production service
  guarantee.

These are design decisions, not hidden behavior. A developer should be able to
state them clearly before shipping the feature.

## Level-ups

### Persist conversations

Create conversation and message models associated with `request.user`. Load the
user's saved conversations only after adding object-level authorization.

### Make the helper Hoot-aware

Allow a user to select a Hoot and send its permitted title and text as explicit
context. Do not imply database access through the system instruction.

### Add DRF throttling

Apply a per-user request limit to protect a shared classroom or production API
key from abuse and accidental loops.

### Stream the response

Use the provider's streaming method and a streaming response protocol so text
can appear in smaller pieces. This changes both backend response handling and
frontend state updates.

### Render a safe subset of Markdown

Add a Markdown renderer and HTML sanitization. Never insert generated HTML with
`dangerouslySetInnerHTML` without a carefully reviewed sanitizer.

### Add provider-independent tests

Mock the Gemini client and test validation, authentication, error mapping, and
successful response shapes without spending quota. The provided solution shows
two introductory DRF tests in `api/tests.py`.
