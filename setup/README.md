<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Set Up Gemini</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to
configure the Gemini Python SDK in Django without exposing an API key.

## Start both Hoot applications

Use your completed Hoot frontend and backend, or copy the applications from the
lesson's [`starter-code`](../starter-code) directory.

Open one terminal for each application. Confirm that you can:

1. Start Django.
2. Start Vite.
3. Sign in.
4. Open the Hoot index.

Do not begin the integration until the existing application works. This gives
us a known starting point and makes new errors easier to locate.

## Create a Gemini API key

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Sign in with a Google account.
3. Open the **API Keys** page.
4. Select **Create API key**.
5. Copy the new key and keep it private.
6. Restrict the key to the Gemini API when AI Studio offers that option.

Google AI Studio can create the Google Cloud project required for a new key. A
billing upgrade is not required to begin on the free tier.

> Never paste an API key into Slack, a screenshot, a pull request, frontend
> code, or a lesson submission. If a key is exposed, replace it and disable the
> old key.

## Add the backend environment variables

Open the backend `.env` file. Add these lines without changing the existing
database and Django settings:

```plaintext
GEMINI_API_KEY=paste-your-real-key-here
GEMINI_MODEL=gemini-3.5-flash-lite
```

The model name is configuration rather than a secret, but keeping it beside the
key makes the model easy to change later.

Now open `.env.example` and add placeholders, not the real key:

```plaintext
GEMINI_API_KEY=replace-this-with-your-gemini-api-key
GEMINI_MODEL=gemini-3.5-flash-lite
```

### Check the ignore rule

Open the backend `.gitignore` and confirm that it includes:

```plaintext
.env
```

Run this command from the backend directory:

```bash
git status
```

The `.env` file should not appear as an untracked or modified file.

## Install the official Python SDK

Activate the backend virtual environment.

On macOS:

```bash
source .venv/bin/activate
```

On Windows with Git Bash:

```bash
source .venv/Scripts/activate
```

Add the SDK to `requirements.txt`:

```plaintext
google-genai>=2,<3
```

Install the requirements:

```bash
python -m pip install -r requirements.txt
```

### Stop and check

Ask Python to import the package:

```bash
python -c "from google import genai; print('Gemini SDK ready')"
```

Expected output:

```plaintext
Gemini SDK ready
```

If Python cannot find `google`, confirm that the virtual environment is active
and rerun the install command.

## Read the configuration in Django

Open `hoot_api/settings.py`. At the bottom of the file, add:

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
```

This reads the secret from the server environment. The empty string is a safe
fallback that will let our endpoint return a clear configuration error.

On the next line, add:

```python
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
```

The second argument gives the application a default model if the model variable
is missing.

### Stop and check without printing the key

Open the Django shell:

```bash
python manage.py shell
```

Import the settings:

```python
from django.conf import settings
```

Check whether a key was loaded without displaying it:

```python
bool(settings.GEMINI_API_KEY)
```

Expected output:

```python
True
```

Check the model name:

```python
settings.GEMINI_MODEL
```

Expected output:

```python
'gemini-3.5-flash-lite'
```

Exit the shell:

```python
exit()
```

If the first check returns `False`, confirm that `.env` is in the backend root
beside `manage.py`, and then restart the Django shell.
