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

    Thanks to @Rahul Gupta's answer:
    > Since DRF needs to support both session and non-session based authentication to the same views, it enforces CSRF check for only authenticated users.

    And [the source code of DRF](https://github.com/encode/django-rest-framework/blob/3.11.0/rest_framework/authentication.py#L113) says everything:
    ```python
    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)
    ```

    References:
    1. https://stackoverflow.com/a/30875830/11200758
    2. https://www.django-rest-framework.org/topics/ajax-csrf-cors/#csrf-protection
