<h1>
  <span class="headline">Build an AI Helper</span>
  <span class="subhead">Scaffold the AI Helper</span>
</h1>

**Learning objective:** By the end of this lesson, students will be able to add
a new protected React page by creating the component, registering its route,
and adding its navigation link in that order.

## Create the page first

In the frontend, create `src/pages/AIHelper.jsx`.

Add only the component shell:

```javascript
const AIHelper = () => {
  return (
    <section className="card ai-helper">
      <header>
        <h1>Hoot AI Helper</h1>
        <p>Ask a question and continue the conversation.</p>
      </header>
    </section>
  )
}

export default AIHelper
```

At this point the component exists, but nothing renders it. That is expected.

## Register the route

Open `src/App.jsx` and import the new page with the other page imports:

```javascript
import AIHelper from './pages/AIHelper'
```

Locate the routes available only when `user` exists. Add this route inside that
protected group:

```javascript
<Route path='/ai-helper' element={<AIHelper />} />
```

Placing the route in this group means the application renders it only for a
signed-in user. It also matches the Django endpoint, which will use the existing
default `IsAuthenticated` permission.

### Stop and check the route directly

1. Make sure Vite is running.
2. Sign in.
3. Type `/ai-helper` after the frontend origin in the address bar.
4. Confirm that the heading and description appear.
5. Sign out and try the same URL again.

When signed out, the page should not render because its route is not present in
the signed-out route group.

If the signed-in page is blank, inspect the browser console for an import path
or component-name error before moving on.

## Add the navigation link

Open `src/components/Nav.jsx`. In the list rendered for a signed-in user, add:

```javascript
<li><Link to='/ai-helper'>AI HELPER</Link></li>
```

Place it before **SIGN OUT** so that authentication remains the final navigation
action.

### Stop and check the complete scaffold

1. Refresh the app while signed in.
2. Confirm that **AI HELPER** appears in the navigation.
3. Select the link.
4. Confirm that the URL becomes `/ai-helper`.
5. Confirm that the page heading appears without a full browser reload.

We now know that the component, route, protected-route placement, and link all
work. The next steps can focus on the feature itself.
