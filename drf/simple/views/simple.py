from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import ViewSet


class SimpleViewSet(ViewSet):
    def list(self, request):
        return HttpResponse('LIST')

    @action(detail=True)
    def view(self, request, pk):
        return HttpResponse('VIEW')

    @action(detail=True)
    def edit(self, request, pk):
        return HttpResponse('EDIT')

    @action(detail=False)
    def new(self, request):
        return HttpResponse('NEW')


router = SimpleRouter()
router.register('simple', SimpleViewSet, 'simple')
