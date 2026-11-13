# MiniBank (Python mini project)

A web-based ATM/banking system. The web framework (Flask) and every piece
of logic — accounts, transactions, persistence, calculations — is written
in Python. HTML/CSS are used only as the display layer Flask renders
(there is no JavaScript required for the app to function).

## Project structure

```
minibank/
├── app.py                 # Flask routes (the website's pages)
├── bank_system.py         # All banking logic (OOP, files, functional programming)
├── api/index.py           # Entry point Vercel's Python runtime loads
├── vercel.json            # Vercel build/routing config
├── requirements.txt
├── data/
│   └── accounts.json      # Where accounts + transactions are stored
├── templates/              # Jinja2 HTML templates (structure only)
└── static/style.css        # All styling
```

## How each syllabus unit shows up in the code

| Unit | Concepts | Where |
|---|---|---|
| I | control flow, exceptions, operators, data types | `try/except` in `bank_system.py` (deposit/withdraw validation), `app.py` route logic |
| II | functions, default args, `*args`/`**kwargs`, strings | `Account.__init__(*args, **kwargs)`, `login_required` decorator, `_generate_number()` |
| III | dictionaries, tuples, sets | `BankSystem.accounts` dict, transaction records as tuples, grouped bill categories |
| IV | files, OOP (classes, inheritance, encapsulation, polymorphism) | `Account` → `SavingsAccount`/`CurrentAccount`, JSON + CSV + pickle I/O, private `__password` |
| V | functional programming, JSON, NumPy/Pandas | `transaction_summary()` (map/filter/reduce/lambda), `analytics_with_pandas()`, JSON persistence |

## Website features

- **Login / create account** — first screen users see.
- Left profile bar (top of sidebar): **profile details, settings, cards**.
- Main navigation is a collapsible **Menu**: overview, account, transfer,
  deposit, withdraw, bill payment, percentage calculator.
- **Overview** combines the balance/quick-actions dashboard with the full
  transaction ledger and stats — no separate "transaction history" page.
- **Transfer** never shows a directory of other customers. You type the
  exact recipient username, the app looks it up and shows you their name
  to confirm, then you enter the amount and send.
- **Bill payment** groups billers into sub-branches/plans (e.g. Electricity
  Board → North Circle) via a native grouped dropdown, and requires a
  consumer/reference number so it's always clear which account is being
  paid. Shows your 5 most recent bill payments as receipts below the form.
- **Indian rupee formatting** (`₹ 10,00,000.00`, proper lakh/crore
  grouping) everywhere a balance or amount is shown — done with a plain
  Python function used as a Jinja filter (`bank_system.format_inr`).
- **Review-then-confirm** on transfer, withdraw, bill payment, and the
  admin's credit/debit action: each shows exactly what's about to happen
  on a second screen before it executes — a server round-trip standing in
  for a JS confirmation modal.
- **Toast-style notifications** for every action (green for success, red
  for errors), floating top-right and auto-fading after 4 seconds using a
  pure CSS animation — no JavaScript timers involved.
- **Masked debit card number** by default (`CARD •••• •••• 9243`) with a
  "Reveal" link that re-renders the page with the full number.
- **"Remember me"** on login extends the Flask session to 30 days via
  `session.permanent`.
- **Search / filter** on the Overview ledger (by keyword or type) and the
  admin dashboard (by name/username/account number), plus simple
  pagination on the admin list — all done as normal GET requests with
  Python's `filter()`, not live JavaScript typing.

### On the JavaScript-heavy asks that got left out

A later round of feedback asked for things like live-as-you-type
calculators/search, a password show/hide eye icon, and true overlay modals.
Those genuinely need JavaScript to work the way they're described, which
conflicts with this project's "Python only" brief and isn't part of the
syllabus units it's built to demonstrate. Everything above delivers the
same *outcome* (confirmation before a risky action, feedback after an
action, filtering data, hiding a sensitive number) using only Python,
Jinja, and CSS. If you'd rather have the literal JS versions, that's a
straightforward add-on — just say the word and note that it moves outside
the "everything is Python" constraint.

## Run it locally

```bash
cd minibank
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000`, create an account, and log in.

## Admin console

A separate console for managing the site, at `/admin/login` (also linked
from the bottom of the customer login page).

- Default credentials: username `admin`, password `admin123` — **change
  these** by setting the `ADMIN_USERNAME` and `ADMIN_PASSWORD`
  environment variables before you deploy anywhere public.
- From the admin dashboard you can see every account and its balance,
  open an account to view its full transaction history, credit or debit
  its balance directly, and delete an account (you have to type the
  username to confirm).
- Admin sessions are completely separate from customer logins — a
  customer's session can't reach `/admin`, and logging into `/admin`
  doesn't log you into any customer account.

## Deploy to Vercel

1. Push this folder to a GitHub repo.
2. In Vercel, "Add New Project" → import the repo. Vercel will detect
   `vercel.json` and use the `@vercel/python` builder automatically.
3. Deploy. No extra configuration is required for a first deploy.

### Important limitation to know about

Vercel's Python functions are **serverless and stateless**: the
filesystem is read-only except `/tmp`, and each cold start gets a fresh
copy of the bundled code. That means `data/accounts.json` works great
for local development and demos, but **new accounts/transactions won't
reliably persist between requests once deployed on Vercel** — a write
in one function invocation may not be visible to the next one.

For a real deployment you'd swap the JSON file in `bank_system.py`'s
`_load()`/`save()` methods for a hosted database (e.g. Vercel Postgres,
Vercel KV, or Supabase). The rest of the app (routes, OOP model,
calculations) doesn't need to change — only those two methods would
talk to a database instead of a file. Happy to wire that up if you tell
me which database you'd like to use.

## Notes

- Passwords are stored in plain text in `data/accounts.json` for
  simplicity, matching the scope of a lab mini-project. Don't reuse a
  real password when testing this.
- `SECRET_KEY` for Flask sessions defaults to a dev value; set the
  `SECRET_KEY` environment variable in Vercel's project settings for a
  real deployment.
