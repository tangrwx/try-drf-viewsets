# README

In order to organize CRUD-related views more efficiently and concisely, I tried to use [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/) instead of [the official class-based views of Django](https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/).

It turned out to be good, or at least a good fit for my needs.

## UseCases

1. Authentication & Permission

    ```python
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from rest_framework.permissions import IsAuthenticated, IsAdminUser

    @method_decorator(login_required, name='dispatch')
    class CommonViewSet(ViewSet):
        def get_permissions(self):
            if self.action in ('new', 'edit'):
                permission_classes = [IsAdminUser]
            else:
                permission_classes = [IsAuthenticated]

            return [permission() for permission in permission_classes]
    ```

2. Security: CSRF

    ```python
    from django.utils.decorators import method_decorator

    @method_decorator(csrf_protect, name='dispatch')
    # @method_decorator(csrf_protect, name='do_login')
    class AuthViewSet(ViewSet):
        pass
    ```
