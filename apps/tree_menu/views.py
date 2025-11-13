from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "demo/home.html"


class CatalogPageView(TemplateView):
    template_name = "demo/catalog.html"


class PricingPageView(TemplateView):
    template_name = "demo/pricing.html"


class IntegrationsPageView(TemplateView):
    template_name = "demo/integrations.html"


class AboutPageView(TemplateView):
    template_name = "demo/about.html"


class ContactPageView(TemplateView):
    template_name = "demo/contact.html"