from django.db import migrations


def create_menu(apps, schema_editor, name, verbose_name, items):
    Menu = apps.get_model("tree_menu", "Menu")
    MenuItem = apps.get_model("tree_menu", "MenuItem")

    menu, _ = Menu.objects.get_or_create(
        name=name,
        defaults={"verbose_name": verbose_name},
    )

    ref = {}
    for item in items:
        parent = ref.get(item.get("parent"))
        menu_item, created = MenuItem.objects.get_or_create(
            menu=menu,
            title=item["title"],
            defaults={
                "parent": parent,
                "named_url": item.get("named_url", ""),
                "url": item.get("url", ""),
                "order": item.get("order", 0),
            },
        )
        if not created:
            menu_item.parent = parent
            menu_item.named_url = item.get("named_url", "")
            menu_item.url = item.get("url", "")
            menu_item.order = item.get("order", 0)
            menu_item.save(update_fields=["parent", "named_url", "url", "order"])
        ref[item["key"]] = menu_item


def create_demo_menus(apps, schema_editor):
    main_menu_items = [
        {"key": "home", "title": "Главная", "named_url": "tree_menu:home", "order": 10},
        {"key": "catalog", "title": "Каталог", "named_url": "tree_menu:catalog", "order": 20},
        {"key": "pricing", "title": "Тарифы", "named_url": "tree_menu:pricing", "parent": "catalog", "order": 10},
        {"key": "integrations", "title": "Интеграции", "named_url": "tree_menu:integrations", "parent": "catalog", "order": 20},
        {"key": "about", "title": "О проекте", "named_url": "tree_menu:about", "order": 30},
        {"key": "contact", "title": "Контакты", "named_url": "tree_menu:contact", "order": 40},
    ]

    sidebar_menu_items = [
        {"key": "overview", "title": "Обзор проекта", "named_url": "tree_menu:home", "order": 10},
        {"key": "architecture", "title": "Архитектура", "named_url": "tree_menu:about", "order": 20},
        {"key": "guides", "title": "Руководства", "order": 30, "url": "#"},
        {"key": "guide-setup", "title": "Установка", "parent": "guides", "order": 10, "url": "#setup"},
        {"key": "guide-admin", "title": "Работа с админкой", "parent": "guides", "order": 20, "url": "#admin"},
    ]

    footer_menu_items = [
        {"key": "privacy", "title": "Политика", "url": "#privacy", "order": 10},
        {"key": "terms", "title": "Условия", "url": "#terms", "order": 20},
        {"key": "support", "title": "Поддержка", "named_url": "tree_menu:contact", "order": 30},
    ]

    create_menu(apps, schema_editor, "main_menu", "Главное меню", main_menu_items)
    create_menu(apps, schema_editor, "sidebar_menu", "Меню раздела", sidebar_menu_items)
    create_menu(apps, schema_editor, "footer_menu", "Меню в подвале", footer_menu_items)


def remove_demo_menus(apps, schema_editor):
    Menu = apps.get_model("tree_menu", "Menu")
    Menu.objects.filter(name__in=["main_menu", "sidebar_menu", "footer_menu"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tree_menu", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_demo_menus, remove_demo_menus),
    ]

