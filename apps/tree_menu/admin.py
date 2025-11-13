from django import forms
from django.contrib import admin

from .models import Menu, MenuItem
from .utils import get_url_choices


class MenuItemForm(forms.ModelForm):
    """Форма с выпадающим списком для named_url"""
    named_url = forms.ChoiceField(
        choices=get_url_choices,
        required=False,
        label="Named URL",
        help_text="Выберите URL из списка или оставьте пустым для явного URL"
    )

    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['named_url'].choices = get_url_choices()

        self.fields[
            'url'].help_text = "Явный URL (например, /catalog/). Используется только если Named URL пуст."
        self.fields[
            'parent'].help_text = "Родительский пункт меню (оставьте пустым для корневого уровня)"
        self.fields['order'].help_text = "Порядок сортировки (меньшее число = выше)"


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    form = MenuItemForm
    extra = 0
    fk_name = 'menu'
    fields = ('title', 'parent', 'named_url', 'url', 'order')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['parent'].queryset = MenuItem.objects.filter(menu=obj)
        return formset


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'verbose_name', 'render_as_dropdown', 'items_count')
    list_editable = ('render_as_dropdown',)
    search_fields = ('name', 'verbose_name')
    inlines = [MenuItemInline]

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = 'Количество пунктов'

    fieldsets = (
        ('Основные настройки', {
            'fields': ('name', 'verbose_name'),
            'description': 'Системное имя используется в шаблоне: {% draw_menu "имя" %}'
        }),
        ('Настройки отображения', {
            'fields': ('render_as_dropdown', 'dropdown_title'),
            'description': 'Dropdown режим: все пункты меню будут обернуты в родительский элемент'
        }),
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ('title', 'menu', 'parent', 'get_url_display', 'order')
    list_filter = ('menu',)
    list_editable = ('order',)
    search_fields = ('title', 'named_url', 'url')
    ordering = ('menu', 'order', 'id')

    fieldsets = (
        ('Основная информация', {
            'fields': ('menu', 'parent', 'title', 'order')
        }),
        ('URL настройки', {
            'fields': ('named_url', 'url'),
            'description': 'Выберите Named URL или укажите явный URL. Named URL имеет приоритет.'
        }),
    )

    def get_url_display(self, obj):
        url = obj.get_url()
        if obj.named_url:
            return f"→ {url} ({obj.named_url})"
        return url

    get_url_display.short_description = 'Итоговый URL'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.menu:
            form.base_fields['parent'].queryset = MenuItem.objects.filter(
                menu=obj.menu
            ).exclude(id=obj.id)
        return form
