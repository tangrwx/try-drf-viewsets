from .views import auth, common, simple

urlpatterns = auth.router.urls + common.router.urls + simple.router.urls
