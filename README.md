# Stonewick

A Django e-commerce site for a refill-only candle & diffuser brand: reusable
stone/ceramic vessels, compostable refill pouches, a seasonal subscription,
and a "Scent Memory Quiz" that matches fragrances to nostalgic memories
instead of generic notes.

This README explains, step by step, how to run the site on your own computer
and how to deploy it to production. No prior Django experience is assumed —
just follow the steps in order.

---

## A quick note about hosting

The original brief asked for Netlify. **Netlify can't run this site.** Netlify
only hosts static files and small serverless functions — it has no
always-on server process and no built-in database, and Django needs both.

Instead, this project is set up to deploy to **Render** (render.com), which
works almost exactly like Netlify (push to GitHub, it builds and deploys
automatically) but fully supports Python, Django, and a real Postgres
database. Everything below uses Render.

---

## Part 1 — Running it on your own computer (local development)

### What you'll need first

- **Python 3.12** (or newer 3.x) installed — check with `python3 --version`
- **Git** installed
- A terminal / command line

### Step-by-step

1. **Get the code onto your computer** (skip this if you already have the
   folder — just open a terminal inside it):
   ```bash
   cd stonewick
   ```

2. **Create a virtual environment.** This keeps this project's Python
   packages separate from everything else on your computer.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # on Windows: .venv\Scripts\activate
   ```
   You'll know it worked because your terminal prompt now starts with
   `(.venv)`.

3. **Install the project's dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create your local settings file.** Copy the example file and you're
   done — the defaults are already correct for local development:
   ```bash
   cp .env.example .env
   ```
   Open `.env` in a text editor and change `SECRET_KEY` to any long random
   string (it just needs to be unique to you). Everything else can stay as-is.

5. **Create the database tables.** Locally this uses SQLite, a
   file-based database that needs zero setup:
   ```bash
   python manage.py migrate
   ```

6. **Create an admin account for yourself:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts (username, email, password).

7. **(Optional but recommended) Add some demo products, scents, and quiz
   questions** so the site isn't empty:
   ```bash
   python manage.py seed_demo_data
   ```

8. **Start the site:**
   ```bash
   python manage.py runserver
   ```
   Now open **http://127.0.0.1:8000/** in your browser. You should see the
   homepage. Visit **http://127.0.0.1:8000/admin/** and log in with the
   superuser account you created to add/edit products, scents, quiz
   questions, categories, and journal posts.

That's it — you're running the full site locally.

### Running the automated tests

```bash
pytest
```
This checks the shopping cart math, the Scent Memory Quiz matching logic,
and subscription pause/resume/cancel/swap behavior.

### Testing Stripe payments locally (optional)

The site works without Stripe configured — you just won't be able to
complete a real checkout. To test real checkout flows locally:

1. Create a free account at [stripe.com](https://stripe.com) and switch to
   **Test mode**.
2. Copy your **test** Publishable key and Secret key into `.env`:
   ```
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   ```
3. Install the [Stripe CLI](https://docs.stripe.com/stripe-cli), then run:
   ```bash
   stripe login
   stripe listen --forward-to localhost:8000/cart/stripe/webhook/
   ```
   This prints a webhook signing secret starting with `whsec_...` — copy it
   into `.env` as `STRIPE_WEBHOOK_SECRET`.
4. Restart `python manage.py runserver` and test a checkout using
   [Stripe's test card numbers](https://docs.stripe.com/testing) (e.g.
   `4242 4242 4242 4242`, any future expiry, any CVC).

---

## Part 2 — Deploying to production (Render)

### Step-by-step

1. **Push this project to GitHub** (create a new repository and push the
   code if you haven't already).

2. **Create a Render account** at [render.com](https://render.com) and
   connect your GitHub account.

3. **Create a new Blueprint.** Render will read the `render.yaml` file
   already included in this project and set up both the web service and the
   Postgres database automatically:
   - In the Render dashboard, click **New → Blueprint**
   - Select your `stonewick` GitHub repository
   - Render will show you the services it's about to create (a web service
     and a database) — click **Apply**

4. **Add your Stripe live keys.** `render.yaml` intentionally leaves these
   blank for you to fill in securely (they're never committed to the repo):
   - In the Render dashboard, open your web service → **Environment**
   - Add `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, and
     `STRIPE_WEBHOOK_SECRET` using your **live mode** Stripe keys
   - To get the webhook secret: in your Stripe dashboard, go to
     **Developers → Webhooks → Add endpoint**, set the URL to
     `https://<your-render-url>/cart/stripe/webhook/`, subscribe to the
     `checkout.session.completed` event, and copy the signing secret it gives you

5. **Wait for the first deploy to finish.** Render will automatically:
   - install everything in `requirements.txt`
   - run `python manage.py collectstatic` (gathers CSS/JS/images)
   - run `python manage.py migrate` (creates all database tables — this
     project ships with the migration files already written, so this works
     out of the box with no extra steps)
   - start the site with Gunicorn

6. **Create your admin account on production.** In the Render dashboard,
   open your web service and use the **Shell** tab to run:
   ```bash
   python manage.py createsuperuser
   ```

7. **(Optional) Seed demo data the same way as local:**
   ```bash
   python manage.py seed_demo_data
   ```

8. **Visit your site.** Render gives you a free `.onrender.com` URL
   immediately — your site is live.

### Connecting a custom domain (e.g. stonewick.com)

1. In the Render dashboard, open your web service → **Settings → Custom
   Domains → Add Custom Domain**.
2. Render will give you a CNAME record to add at your domain registrar
   (wherever you bought the domain).
3. Once DNS updates (can take a few minutes to a few hours), Render
   automatically issues a free HTTPS certificate for it.
4. Update the `SITE_DOMAIN` environment variable on your web service to
   your real domain, and add it to `ALLOWED_HOSTS` and
   `CSRF_TRUSTED_ORIGINS` (as `https://yourdomain.com`).

### Rolling back a bad deploy

In the Render dashboard, open your web service → **Events/Deploys** tab,
find the last known-good deploy, and click **Rollback to this deploy**.
No command line needed.

### Ongoing costs

- Render's free tier is enough to launch on. As traffic grows, upgrade the
  web service and database plans from the Render dashboard — no code
  changes required.
- Stripe only charges a small percentage per transaction — no fixed monthly
  cost.

---

## Project structure, for reference

```
stonewick/
├── config/                 # Django settings, root URLs
│   └── settings/
│       ├── base.py         # shared settings
│       ├── dev.py          # local development
│       └── production.py   # Render production settings
├── apps/
│   ├── core/                # homepage, about, FAQ, contact, sitemap, robots.txt
│   ├── accounts/             # signup, login, account dashboard
│   ├── catalog/              # products, categories, scents (the shop)
│   ├── quiz/                 # the Scent Memory Quiz
│   ├── orders/                # cart, checkout, Stripe payments
│   ├── subscriptions/        # seasonal refill subscription management
│   ├── journal/               # blog/content for SEO
│   └── reviews/               # product reviews (admin-managed)
├── templates/                # all HTML templates
├── static/css/style.css      # hand-written CSS (no framework)
├── tests/                    # automated tests (pytest)
├── render.yaml                # Render infrastructure config
├── Procfile                    # tells Render how to run/release the app
└── requirements.txt
```

## Before you launch: two images to add

The templates reference two brand image files that aren't included (this is
a code template, not a photoshoot) — add real files at these exact paths so
social sharing previews and structured data look right:

- `static/img/og-default.jpg` — the fallback image shown when a page is
  shared on social media (recommended size: 1200×630px)
- `static/img/logo.png` — your logo, used in the `Organization` structured
  data that helps search engines show your logo in results

## Making day-to-day content changes (no coding required)

Once deployed, most ongoing work happens in the Django admin at
`/admin/` — a non-developer (e.g. a marketing team member) can:

- Add/edit products, prices, and photos (**Catalog → Products**)
- Add new scents with their "memory story" description (**Catalog → Scents**)
- Update which season each scent rotates in (**Catalog → Scents**)
- Add/edit quiz questions and answer options (**Quiz → Quiz questions**)
- Publish new journal/blog posts (**Journal → Posts**)
- View and respond to contact form submissions (**Core → Contact messages**)

No code deploy is needed for any of this.

## Changing a URL later without breaking SEO

If you ever rename or move a page (e.g. a product's slug changes), add a
redirect so old links and search rankings aren't lost: go to **Admin →
Redirects → Add redirect**, enter the old path (e.g. `/shop/product/old-name/`)
and the new path. Django will automatically 301-redirect visitors and search
engines from the old URL to the new one — no code changes needed.

## Scaling this site later

You won't need any of this at launch — but as the site grows, here's when to
reach for each upgrade (all are config changes on Render, not code rewrites):

| When you notice...                                  | Do this                                                             |
|-------------------------------------------------------|----------------------------------------------------------------------|
| The database plan is near its connection/storage limit | Upgrade the Postgres plan in the Render dashboard                    |
| Product photo storage is filling up the web service's disk | Switch `MEDIA` storage to Cloudflare R2 or AWS S3 via `django-storages` (the code already uses Django's storage abstraction, so this is a settings change, not a rewrite) |
| Pages feel slow under real traffic                    | Add Render's Redis add-on + `django-redis` for page/fragment caching |
| Emails, webhook processing, or image resizing start blocking requests | Add Celery (or `django-q2`) + Redis for background tasks |
| Asset delivery feels slow to visitors far from your server | Put Cloudflare (or Render's edge caching) in front of the site |
| Traffic outgrows a single web service instance          | Scale to multiple instances in Render (the app already uses database-backed sessions, so it's stateless-ready) |

## Common issues

- **"relation does not exist" errors right after deploy:** Make sure the
  release step (`python manage.py migrate`) actually ran — check the
  deploy logs in the Render dashboard.
- **Static files (CSS) not loading in production:** Make sure
  `collectstatic` ran during the build step (check the build logs), and
  that `DEBUG=False` in your production environment variables.
- **Checkout redirects to Stripe but nothing happens after payment:** Double
  check your Stripe webhook is pointed at
  `https://yourdomain.com/cart/stripe/webhook/` and that
  `STRIPE_WEBHOOK_SECRET` matches the one Stripe shows you for that
  specific endpoint.
