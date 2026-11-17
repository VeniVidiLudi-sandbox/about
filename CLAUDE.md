# About

A public, unauthenticated showcase of the owner's personal projects and the tech stack each uses.
Visitors (friends, collaborators, employers) see project cards (name, summary, live link, tech tags);
clicking a tag filters by technology (`/?tech=<slug>`); each project has a detail page
(`/projects/<slug>/`: longer text, screenshot URL, repo link). Content is managed only by the owner in
the Django admin (`Project`, `Technology`); there is no visitor login. A data migration adds the example
project "shopping". The brief's first line is in `app/description.txt`, which the home page shows.

## How this repo works
- Django 5.2 + Postgres, started from the platform's Django template. The platform's rules are in
  `/etc/claude-code/CLAUDE.md`; `platform.yaml` and `compose.yaml` say how the platform runs it.
- Settings come only from environment variables (`config/settings.py`).
- Login is the platform's login service (OIDC, `app/auth.py`). Members of `superadmin` are Django
  superusers. Apps keep no passwords.
- Dependencies: edit `pyproject.toml`, then `uv lock`. The image installs exactly what `uv.lock` says.
- Tests: `DJANGO_TEST_SQLITE=1 SECRET_KEY=test uv run pytest`.
- Migrations must also work with the previous release's code (add now, remove later).

## Next steps
- Add the rest of the projects in `/admin/` (sign in via the platform login as a `superadmin` member).
- Screenshots are plain image URLs (`screenshot_url`); upload support would need media storage in `DATA_DIR`.
- The sign-in link was removed from the home page; admin is reached at `/admin/` (check it triggers OIDC login).
- Possible: Open Graph tags, a short "about me" intro block.
