from django import template

from apps.tree_menu.models import Menu, MenuItem

register = template.Library()


class Node:
    """
    Вспомогательный объект для дерева (чтобы не тянуть из БД в шаблоне).
    """

    __slots__ = ("id", "title", "url", "parent_id", "children", "is_active", "is_ancestor")

    def __init__(self, item):
        self.id = item.id
        self.title = item.title
        self.url = item.get_url()
        self.parent_id = item.parent_id
        self.children = []
        self.is_active = False
        self.is_ancestor = False


def build_menu_tree(items, current_path):
    """
    items — queryset/список пунктов одного меню.
    """
    nodes = {}
    for item in items:
        nodes[item.id] = Node(item)

    roots = []
    for node in nodes.values():
        if node.parent_id and node.parent_id in nodes:
            nodes[node.parent_id].children.append(node)
        else:
            roots.append(node)

    active = None

    for node in nodes.values():
        if node.url == current_path:
            active = node
            break

    if active is None:
        best_len = -1
        for node in nodes.values():
            if node.url and current_path.startswith(node.url) and len(node.url) > best_len:
                best_len = len(node.url)
                active = node if node.url != "#" else active

    if active:
        active.is_active = True
        parent_id = active.parent_id
        while parent_id:
            parent = nodes.get(parent_id)
            if not parent:
                break
            parent.is_ancestor = True
            parent_id = parent.parent_id

    return roots, active


@register.inclusion_tag("tree_menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """
    Использование: {% load tree_menu_tags %} и потом {% draw_menu 'main_menu' %}
    """
    request = context.get("request")
    current_path = getattr(request, "path", "/") if request else "/"

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        menu = None

    items = list(
        MenuItem.objects.filter(menu__name=menu_name)
        .select_related("parent", "menu")
        .order_by("menu", "parent__id", "order", "id")
    )

    roots, active = build_menu_tree(items, current_path)

    return {
        "menu_name": menu_name,
        "menu": menu,
        "roots": roots,
        "active_node": active,
        "render_as_dropdown": menu.render_as_dropdown if menu else False,
        "dropdown_title": menu.dropdown_title if menu else "",
    }
