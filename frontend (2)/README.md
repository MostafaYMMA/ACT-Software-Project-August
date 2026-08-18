# ACT — Frontend

Plain HTML/CSS/JS frontend for the ACT project: login, signup, and a dashboard app
(Dashboard, Tasks, Projects, Team, Reports, Settings) behind a top header and an
animated collapsible sidebar. Orange & white theme. No build step, no framework —
open the files directly or serve the folder statically.

## Pages

| File             | Purpose                                                    |
|-------------------|-------------------------------------------------------------|
| `index.html`      | Login (entry point)                                        |
| `signup.html`     | Create account (name, email, password)                     |
| `dashboard.html`  | Overview: open/completed stat tiles, recent tasks           |
| `tasks.html`      | Full task list — add, complete, delete, filter              |
| `projects.html`   | Project cards with progress and status (mock data)          |
| `team.html`       | Team directory (mock data)                                  |
| `reports.html`    | Completion rate, priority breakdown, tasks added per day    |
| `settings.html`   | Profile + sidebar preference                                |

## Structure

```
frontend/
├── index.html
├── signup.html
├── dashboard.html
├── tasks.html
├── projects.html
├── team.html
├── reports.html
├── settings.html
├── css/
│   └── style.css       # orange/white design tokens + all page styles
├── js/
│   ├── app.js           # auth guard, header/sidebar wiring, shared state (Store)
│   ├── auth.js           # login/signup form logic
│   ├── tasks.js           # task CRUD + rendering
│   ├── projects.js         # mock project data + rendering
│   └── team.js              # mock team data + rendering
└── README.md
```

## Layout

- **Top header** — company logo on the left (with the sidebar toggle button next to it),
  and a manager/profile pill on the right (avatar + name).
- **Sidebar** — Dashboard, Tasks, Projects, Team, Reports up top; Settings and Logout
  pinned to the bottom in their own section.
- **Collapsible sidebar** — the toggle button smoothly animates the sidebar between its
  full width and an icon-only rail (labels fade/slide out via CSS transitions, icons stay
  visible). The main content area resizes to fill the freed space. Collapsed state
  persists across pages via `localStorage`. On narrow screens (≤780px) the same toggle
  instead opens the sidebar as an overlay drawer.

## Running it

Any static server works, e.g.:

```bash
cd frontend
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## How auth/data currently works

This is a **frontend-only demo**: accounts and tasks are stored in the browser's
`localStorage` (see `Store` in `js/app.js`) so the flows are fully clickable without
a backend yet. Swap the `Store.*` methods for real API calls once the backend is ready —
the rest of the pages don't need to change since they only talk to `Store`. Projects and
Team currently use static mock data in `js/projects.js` / `js/team.js` — replace those
arrays with an API call when that data has a real source.

- `act_users` — array of `{ name, email, password, createdAt }`
- `act_session` — the signed-in user's email
- `act_tasks_<email>` — that user's task list
- `act_sidebar_collapsed` — `"1"` or `"0"`, remembers sidebar state

## Design notes

Orange & white theme: white surfaces, warm off-white page background, orange (`#F97316`)
as the single accent for the logo, primary buttons, active nav state, and highlights.
Fonts: Fraunces (headings), Inter (UI text), IBM Plex Mono (labels/numbers). Fully
responsive, with a collapsible desktop sidebar and a mobile overlay drawer.
