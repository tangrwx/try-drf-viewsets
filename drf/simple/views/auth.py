from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import action
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import ViewSet


# @method_decorator(csrf_protect, name='dispatch')
@method_decorator(csrf_protect, name='do_login')
class AuthViewSet(ViewSet):
    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        print(handler)
        print(dir(handler))
        print(handler.__name__)
        print(handler.__class__)
        print(handler.__wrapped__)

        return super().dispatch(request, *args, **kwargs)

    @action(detail=False)
    def login(self, request):
        return HttpResponse('''
            <form method="post">
                <input type="text" name="username">
                <input type="password" name="password">
                <input type="submit" value="Login">
            </form>
        ''')

    @login.mapping.post
    def do_login(self, request):
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.GET.get('next', '/')

        user = auth.authenticate(request, username=username, password=password)
        print(user)
        if user and user.is_active:
            auth.login(request, user)
            print('login successfully')
            return HttpResponseRedirect(next_url)
        else:
            print('login failed')
            return HttpResponseRedirect(reverse('auth-login'))

    @action(detail=False, methods=['get', 'post'])
    def logout(self, request):
        auth.logout(request)
        print('logout')
        return HttpResponseRedirect(reverse('auth-login'))


router = SimpleRouter()
router.register('', AuthViewSet, 'auth')
