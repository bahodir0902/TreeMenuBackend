from django.urls import path

from . import views

app_name = "tree_menu"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("catalog/", views.CatalogPageView.as_view(), name="catalog"),
    path("catalog/pricing/", views.PricingPageView.as_view(), name="pricing"),
    path("catalog/integrations/", views.IntegrationsPageView.as_view(), name="integrations"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
]
