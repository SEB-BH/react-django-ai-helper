<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Build the Conversation State</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to use
React state to control the prompt field and represent an ordered conversation.

## Begin with the input state

Open `src/pages/AIHelper.jsx`. Import `useState` above the component:

```javascript
import { useState } from 'react'
```

Inside `AIHelper`, before `return`, add:

```javascript
const [formData, setFormData] = useState('')
```

This state holds the text currently in the input. The empty string is the
initial value because the user has not typed anything yet.

## Add the controlled field

Still above `return`, create the change handler:

```javascript
const handleChange = (event) => {
  setFormData(event.target.value)
}
```

Inside the existing outer `<section>`, below its `<header>`, add a form:

```javascript
<form>
  <label htmlFor="message">Message</label>
  <textarea
    id="message"
    name="message"
    rows="3"
    maxLength="2000"
    value={formData}
    onChange={handleChange}
    placeholder="Ask Hoot Helper..."
  />
  <button type="submit">SEND</button>
</form>
```

The `value` comes from state, and `onChange` updates that state. Those two props
make the field controlled by React.

### Stop and make the state visible

Temporarily add this paragraph above the form:

```javascript
<p>Current input: {formData || '(empty)'}</p>
```

Type slowly in the field. Confirm that the paragraph changes after each
keystroke.

You can also open React Developer Tools, select `AIHelper`, and watch `formData`
change there.

Remove the temporary paragraph after the check. We have seen the state work and
do not need to keep debugging output in the interface.

## Represent the conversation as a list

Add a second state variable beside `formData`:

```javascript
const [messages, setMessages] = useState([])
```

We use an array because:

- A conversation has multiple messages.
- Their order matters.
- We will append a new object without replacing earlier objects.

Each item will contain a `role` and `text`:

```javascript
{
  role: 'user',
  text: 'What is a Django model?'
}
```

## Stop the browser's default submit

Above `return`, add the submit handler:

```javascript
const handleSubmit = (event) => {
  event.preventDefault()
}
```

Connect it to the form:

```javascript
<form onSubmit={handleSubmit}>
```

### Stop and check the browser behavior

Open the browser's Network panel, enter text, and select **SEND**. The page
should not reload and no request should appear yet. We have handled only the
browser event; the function does not have request code.

## Clean and guard the input

Inside `handleSubmit`, after `event.preventDefault()`, add:

```javascript
const trimmedMessage = formData.trim()
```

Then add the guard:

```javascript
if (!trimmedMessage) {
  return
}
```

Whitespace is not a useful question. The guard ends the function before we add
an empty message.

## Build one user message

Below the guard, create the object:

```javascript
const userMessage = {
  role: 'user',
  text: trimmedMessage,
}
```

Build a new array containing the old messages and the new object:

```javascript
const nextMessages = [...messages, userMessage]
```

The spread operator copies the previous array items. We do not call
`messages.push(...)` because React state should be replaced with a new array.

## Inspect before setting state

Temporarily log the new array:

```javascript
console.log('Next messages:', nextMessages)
```

Then update the two state variables:

```javascript
setMessages(nextMessages)
setFormData('')
```

### Stop and check the state transition

1. Open the browser console.
2. Enter `What is Django?`.
3. Select **SEND**.
4. Confirm that the console shows an array with one object.
5. Confirm that the text field clears.
6. Inspect `messages` in React Developer Tools.

Remove the temporary `console.log` after this check.

## Render the empty state

Between the page header and form, add a section for the messages:

```javascript
<section className="ai-helper-messages" aria-live="polite">
  {messages.length === 0 && (
    <p className="ai-helper-empty">
      No messages yet. Ask Hoot Helper a question.
    </p>
  )}
</section>
```

`aria-live="polite"` asks assistive technology to announce new content without
interrupting its current announcement.

Refresh the page and confirm that the empty-state sentence appears.

## Render each message

Inside the message section, after the empty-state block, map over the array:

```javascript
{messages.map((message, index) => (
  <article
    className={`ai-message ai-message-${message.role}`}
    key={`${message.role}-${index}`}
  >
    <strong>
      {message.role === 'user' ? 'You' : 'Hoot Helper'}
    </strong>
    <p>{message.text}</p>
  </article>
))}
```

The role controls both the label and a CSS class. Later, the classes will place
user messages and generated messages on different sides.

Using the array index as part of a key is acceptable here because messages are
only appended or the whole conversation is cleared. We are not reordering or
editing items.

### Stop and check the rendered array

1. Enter a question.
2. Select **SEND**.
3. Confirm that the empty state disappears.
4. Confirm that a **You** article appears with the exact trimmed text.
5. Enter text with spaces before and after it and confirm those spaces are not
   displayed.

The page can now represent local conversation state. It still does not contact
Django; we will make that boundary explicit in the next lesson.
