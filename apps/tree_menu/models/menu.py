from django.db import models


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Системное имя меню, используется в шаблоне: {% draw_menu 'main_menu' %}",
    )
    render_as_dropdown = models.BooleanField(
        default=False,
        verbose_name="Отрисовать как dropdown",
        help_text="Если включено, все пункты меню будут обернуты в родительский dropdown элемент",
    )
    dropdown_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок dropdown",
        help_text="Текст для родительского элемента (например, 'Profile', 'Account')."
        " Используется только если 'Отрисовать как dropdown' включено",
    )

    verbose_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Человекочитаемое название (для админки).",
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.verbose_name or self.name
