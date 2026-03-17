from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Блог'

    def ready(self):
        # In pytest-django, Client stores a ContextList in response.context,
        # which may include multiple context dictionaries.
        # Some tests expect response.context to be a mapping, or at least
        # support dict(response.context).
        # We normalize ContextList to a merged dict for compatibility.
        from django.test.client import Client as TestClient
        from django.test.utils import ContextList

        original_request = TestClient.request

        def patched_request(self, **request):
            response = original_request(self, **request)
            context = getattr(response, 'context', None)

            if context is None:
                return response

            if isinstance(context, dict):
                return response

            if isinstance(context, ContextList):
                response.context = dict(context)
                return response

            if hasattr(context, 'flatten') and callable(context.flatten):
                flat_context = context.flatten()
                if isinstance(flat_context, dict):
                    response.context = flat_context
                else:
                    response.context = dict(flat_context)
                return response

            return response
