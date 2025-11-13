from django.urls import get_resolver


def get_url_choices():
    """Получить список всех доступных named URLs из проекта"""
    choices = [('', '--- Выберите URL ---')]
    resolver = get_resolver()

    def extract_urls(urlpatterns, namespace=''):
        urls = []
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                ns = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                urls.extend(extract_urls(pattern.url_patterns, ns or namespace))
            elif hasattr(pattern, 'name') and pattern.name:
                name = f"{namespace}:{pattern.name}" if namespace else pattern.name
                urls.append((name, name))
        return urls

    choices.extend(sorted(extract_urls(resolver.url_patterns)))
    return choices


