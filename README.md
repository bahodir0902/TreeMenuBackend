# Tree Menu Demo — Django Showcase

An end-to-end demonstration of a hierarchical navigation system, implemented as a reusable Django app. The project highlights how to build, store, render, and manage tree menus entirely with native Django components while keeping database access efficient—one query per menu.

---

## Feature Highlights

- **Template tag rendering** — Drop-in `{% draw_menu "main_menu" %}` tag prepares a fully hydrated tree without leaking ORM calls into templates.
- **URL-aware activation** — Current page is detected from the request path (exact match or longest prefix), so the active branch is expanded and highlighted automatically.
- **Flexible linking** — Supports both named URLs (`reverse`) and raw URLs, with fallback logic to keep links valid.
- **Multiple menus per page** — Any number of independent menus can be rendered on the same template; each triggers exactly one query thanks to prefetching strategy.
- **Admin-first content workflow** — All menus and items are stored in the database and editable via Django Admin with inline editing.
- **Demo-ready data** — A data migration seeds three menus (main, sidebar, footer) covering nested and flat navigation patterns.
- **Composable views** — A suite of `TemplateView` subclasses powers a multi-page “portal” that demonstrates menu behaviour in various contexts.

---

## Architecture Overview

```
core/
  settings.py          # project configuration (PostgreSQL, template dirs, apps)
  urls.py              # routes admin + tree_menu demo pages
apps/
  tree_menu/           # reusable tree menu app
    models/
      menu.py          # Menu (container)
      menu_item.py     # MenuItem with hierarchy + URL resolution logic
    templatetags/
      tree_menu_tags.py# draw_menu inclusion tag and tree-building helpers
    templates/tree_menu/
      menu.html        # top-level UL wrapper
      menu_node.html   # recursive LI renderer with active state handling
    views.py           # DemoPageView + concrete pages (home, catalog, etc.)
    urls.py            # Named routes for demo pages
    migrations/
      0001_initial.py  # schema definition
      0002_create_demo_menus.py  # demo content seeding
templates/
  base.html            # shared layout with header/sidebar/footer menus
  demo/page.html       # content placeholder for individual demo pages
```

### Data Model

- `Menu`
  - `name` – unique system identifier, used in the template tag.
  - `verbose_name` – friendly label for admins.
- `MenuItem`
  - `menu` – foreign key to `Menu`.
  - `parent` – self-referential foreign key (nullable) enabling arbitrary depth.
  - `title`, `named_url`, `url`, `order`.
  - `get_url()` prefers `named_url` via `reverse`; falls back to explicit URL or `#`.

### Rendering Pipeline

1. `draw_menu` inclusion tag fetches all items for a given menu name (one query).
2. `build_menu_tree` transforms the flat queryset into `Node` objects with `children`, `is_active`, and `is_ancestor` flags.
3. Active node detection:
   - Exact match with the current request path.
   - Fallback to the longest prefix (e.g. `/catalog/` for `/catalog/item/`).
4. Recursive template (`menu_node.html`) renders nested `<ul>` and `<li>` elements, expanding only the active branch and its ancestors.

---

## Project Structure Deep Dive

- `apps/tree_menu/views.py` — Contains `DemoPageView` and six derived views representing different sections (home, catalog, pricing, integrations, about, contact). Each view injects structured content (title, lead paragraph, sections) into the shared template.
- `templates/base.html` — Establishes the UI shell with CSS styling and renders three separate menus to illustrate independent invocations of `draw_menu`.
- `apps/tree_menu/migrations/0002_create_demo_menus.py` — Populates demo menus with nested items and named URL references. Running `python manage.py migrate` drops you into a fully functional showcase.
- `core/urls.py` — Wires project root to `apps.tree_menu.urls`, exposing the demo pages at `/`, `/catalog/`, `/catalog/pricing/`, etc.

---

## Getting Started

### Requirements

- Python 3.11+
- PostgreSQL (or compatible Postgres service)
- `pip`, `virtualenv` (recommended)

### Environment Variables

Configure database credentials via `.env` (loaded by `python-decouple`):

```
DB_NAME=template_task
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate        # applies schema + demo menu migration
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to explore the demo UI. The Django admin is available at `/admin/`.

---

## Demo Tour

- **Header menu (`main_menu`)** — Highlights top-level navigation and nested catalog branch. Observe automatic expansion when visiting `/catalog/`, `/catalog/pricing/`, etc.
- **Sidebar menu (`sidebar_menu`)** — Demonstrates calling the tag multiple times on a single page and mixing named URLs with anchor links.
- **Footer links (`footer_menu`)** — Shows a shallow menu that still benefits from activation logic (e.g. “Support” active on the contact page).

The content pages themselves use purely declarative data from `DEMO_PAGES`, proving that the menu logic is entirely decoupled from view code.

---

## Working in the Admin

1. Log into `/admin/` with the superuser credentials you created.
2. Add or edit `Menu` records (inline editing of `MenuItem` is enabled).
3. Rearrange items by adjusting the `order` field; set hierarchical relationships via the `parent` dropdown.
4. Use either `named_url` (preferred for internal links) or explicit `url`. If `named_url` cannot be reversed, the system automatically falls back to the provided URL.

All changes are reflected immediately in the rendered menus thanks to the template tag abstraction.

---

## Extending the Project

- **Custom menu placement** — Include `{% load tree_menu_tags %}` in any template and call `{% draw_menu "your_menu_name" %}` wherever needed.
- **Alternate activation rules** — Extend `build_menu_tree` to support custom logic (e.g. regex matching, query parameters).
- **Caching** — Wrap the template tag output in Django’s template fragment cache if your menu data is large and seldom changes.
- **Styling** — Replace `base.html` with your design system; the markup structure is lightweight and predictable.

---

## Testing & Quality

While the project focuses on demonstrative code, the components are structured for easy test coverage:

- Unit tests can target `build_menu_tree` to validate active node detection and expansion rules.
- Template tests (via `django.test.Client`) can assert rendered HTML for various URL scenarios.

Linting passes with the default Django checks; integrate your preferred tools (e.g. `flake8`, `black`) as needed.

---

## Summary

This repository delivers a polished reference implementation for tree-based navigation in Django:

- Clean separation between data, rendering, and presentation.
- Zero third-party dependencies beyond Django and the standard library.
- Ready-made demo pages and content to illustrate every feature point.

Clone, run, explore, and adapt it to your own projects. Happy coding!
