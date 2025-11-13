# Django Tree Menu

A production-ready Django application for hierarchical navigation with efficient database queries,
flexible rendering modes with demo pages.

### Live Website

Interact with the tree menu in a live environment on the deployed demo site.

Switch between flat and dropdown navigation modes

Observe automatic active-branch expansion

Click through sample pages powered by this backend
http://13.53.73.97:8009

Here is the admin panel link for that website:
- http://13.53.73.97:8009/admin
- email: admin@admin.com
- password: 12

## Watch Video Overview

For a quick walkthrough of the project features and behavior, watch the video overview:

▶️ Watch the Django Tree Menu overview on YouTube: https://youtu.be/K4NHN2cgDC0

## Overview

This project implements a reusable tree menu system that addresses common navigation requirements in
Django applications:

- Single database query per menu render
- Automatic active branch detection and expansion
- Support for both flat and dropdown menu layouts
- Named URL resolution with fallback handling

## Key Features

### Core Functionality

- **Template tag rendering** — `{% draw_menu 'menu_name' %}` generates complete menu trees
- **URL-aware activation** — Automatic detection of active pages via request path matching
- **Dual URL support** — Named URLs (Django's `reverse()`) with explicit URL fallback
- **Multiple menu instances** — Render independent menus on the same page
- **Configurable display modes** — Flat lists or dropdown wrappers per menu

### Admin Interface

- **URL selection dropdowns** — Auto-populated list of available named URLs
- **Inline editing** — Manage menu items directly from menu edit pages

### Performance

- **Optimized queries** — One query per menu using `select_related()` and `prefetch_related()`
- **Tree building** — In-memory tree construction from flat queryset
- **Minimal template logic** — Active state calculation happens in Python

## Technical Architecture

```
apps/tree_menu/
├── models/
│   ├── menu.py              # Menu container with display settings
│   └── menu_item.py         # Hierarchical menu items
├── templatetags/
│   └── tree_menu_tags.py    # Template tag and tree builder
├── templates/tree_menu/
│   ├── menu.html            # Root template with mode selection
│   └── menu_node.html       # Recursive node renderer
├── admin.py                 # admin classes
├── utils.py                 # utility functions
└── views.py                 # Demo views
```

### Data Model

**Menu**

- `name` (CharField, unique) — Template tag identifier
- `verbose_name` (CharField) — Admin display name
- `render_as_dropdown` (BooleanField) — Display mode flag
- `dropdown_title` (CharField) — Parent element text for dropdown mode

**MenuItem**

- `menu` (ForeignKey) — Parent menu
- `parent` (ForeignKey, self-referential) — Hierarchy support
- `title` (CharField) — Display text
- `named_url` (CharField) — Django URL name
- `url` (CharField) — Explicit URL fallback
- `order` (PositiveIntegerField) — Sort order

### Rendering Logic

1. Template tag fetches all items for menu (single query)
2. Tree builder constructs node hierarchy with active state flags
3. Active detection uses exact match or longest prefix match
4. Template recursively renders nodes, expanding active branches

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (for containerized deployment)

### Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/bahodir0902/TreeMenuBackend.git
cd TreeMenuBackend

# Start services
docker compose up --build

# Access application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
```

Default admin credentials are created via `entrypoint.sh`.

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (pip)
pip install -r requirements.txt

# Or with Poetry
poetry install
poetry shell

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Environment Configuration

Required variables in `.env`:

```env
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=db_port (or host.docker.internal) if deploying
SECRET_KEY=your-secret-key
DEBUG=True
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Usage

### Template Integration

```django
{% load tree_menu_tags %}

<!DOCTYPE html>
<html>
<body>
    <header>
        <!-- Flat navigation menu -->
        {% draw_menu 'main_menu' %}
    </header>

    <aside>
        <!-- Sidebar menu -->
        {% draw_menu 'sidebar_menu' %}
    </aside>

    <nav>
        <!-- Dropdown footer menu -->
        {% draw_menu 'footer_menu' %}
    </nav>
</body>
</html>
```

### Admin Configuration

#### Creating a Menu

1. Navigate to Admin → Menus → Add Menu
2. Set system name (e.g., `main_menu`)
3. Choose display mode:
    - Flat: Items render as siblings
    - Dropdown: Items wrap in parent element
4. Add menu items with hierarchy

#### URL Configuration

Menu items support two URL types with automatic fallback:

- **Named URL** (recommended): Select from dropdown of available URLs
- **Explicit URL**: Manual path entry (e.g., `/contact/`)

Named URLs are resolved at render time. If resolution fails, explicit URL is used.

### Menu Display Modes

**Flat Mode** (default)

```
[Главная] [Каталог...] [О проекте] [Контакты]
```

Use for: Main navigation, footer links, breadcrumbs

**Dropdown Mode**

```
[Профиль ▼]
  └─ Аккаунт
  └─ Настройки
  └─ Выйти
```

Use for: User menus, language selectors, admin actions

## Development

### Project Structure

```
.
├── apps/
│   └── tree_menu/          # Main application
├── core/                   # Django settings
├── templates/              # Global templates
├── static/                 # Static assets
├──
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container configuration
└── entrypoint.sh
├── .github/
│   └── workflows/          # CI/CD pipelines
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # Pip dependencies (old)
└── .pre-commit-config.yaml # Pre-commit hooks
```

### Code Quality

The project uses:

- **Black** — Code formatting
- **isort** — Import sorting
- **flake8** — Linting
- **mypy** — Type checking (optional)

Configuration is defined in `pyproject.toml` and `.pre-commit-config.yaml`.

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration plan
python manage.py showmigrations
```

## Deployment

### Docker Production Build

```bash
# Run with compose
docker compose up --build -d
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic --no-input

# Configure web server to serve /static/ and /media/
```

### Environment Variables for Production

## Performance Considerations

### Query Optimization

Each `draw_menu` call executes exactly one query:

```python
items = MenuItem.objects.filter(menu__name=menu_name)
    .select_related('parent', 'menu')
    .order_by('order', 'id')
```

Tree construction happens in Python, not database.

### Scaling

- Menu items are prefetched in single query
- No N+1 query problems
- Tree building is O(n) where n = item count
- Template rendering is O(n) with early termination for collapsed branches

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## License

This project is provided as-is for demonstration and educational purposes.
That is, you can use this project as you wish.

## Requirements

See `requirements.txt` or `pyproject.toml` for complete dependency list.
