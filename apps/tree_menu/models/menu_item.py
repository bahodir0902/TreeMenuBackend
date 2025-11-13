from django.db import models
from django.urls import NoReverseMatch, reverse

from .menu import Menu


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        related_name="items",
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=255)

    named_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Имя url из urls.py (reverse). Если указано, поле 'url' игнорируется.",
    )

    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Явный URL. Используется, если named_url не задан или неразрешим.",
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("menu", "parent__id", "order", "id")
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return f"{self.title} ({self.menu.name})"

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                if self.url:
                    return self.url
                return "#"
        return self.url or "#"
