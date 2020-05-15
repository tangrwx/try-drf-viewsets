from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from rest_framework.viewsets import ViewSet


@method_decorator(login_required, name='dispatch')
class CommonViewSet(ViewSet):
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

    def get_permissions(self):
        if self.action in ('new', 'edit'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request):
        return HttpResponse('LIST')

    @action(detail=True)
    def view(self, request, name):
        return HttpResponse('VIEW')

    @action(detail=True)
    def edit(self, request, name):
        return HttpResponse('EDIT')

    @action(detail=False)
    def new(self, request):
        return HttpResponse('NEW')


class CommonRFRouter(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}/{lookup}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


router = CommonRFRouter()
router.register('common', CommonViewSet, 'common')
