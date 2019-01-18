from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import SignUpForm


def home(request):
    context = {}
    return render(request, 'home.html', context=context)

class GetAccess(TemplateView):
    
    def post(self, *args, **kwargs):
        data = {}
        if self.request.is_ajax():
            details = self.request.POST
            username = details.get('username')
            password = details.get('password')
            _auth = authenticate(username=username, password=password)
            print(username)
            print(password)
            print(_auth)

            if _auth in User.objects.all():
                login(request=self.request, user=_auth)
                data['authentication'] = 'passed'
            else:
                data['authentication'] = 'failed'
                data['message'] = 'Either your username or password is incorrect'

        return JsonResponse(data)

class Memberiser(TemplateView):

    def post(self, *args, **kwargs):
        data = {}
        form = SignUpForm(self.request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(self.request, user)
            data['success'] = "Member added Sucessfully"

        return JsonResponse(data)

class Memberise(TemplateView):

    def post(self, *args, **kwargs):
        data = {}
        if self.request.is_ajax():
            details = self.request.POST
            password = details.get('password1')
            confirm = details.get('password2')
            username = details.get('username')
            email = details.get('email')

            data['creation'] = "passed"
            if password and password == confirm:
                if email:
                    if username:
                        users = User.objects.filter(username__exact=username)
                        if users.count() == 0:
                            User.objects.create_user(
                                username=username,
                                email=email,
                                password=password,
                            )
                            user = authenticate(username=username, password=password)
                            login(self.request, user)
                            data['creation'] = "passed"
                            data['message'] = "Member was successfully added"
                        else:
                            data['creation'] = "failed"
                            data['message'] = "Username is already taken"
                    else:
                        data['creation'] = "failed"
                        data['message'] = "Provide a username"
                else:
                    data['creation'] = "failed"
                    data['message'] = "Provide a valid email"
            else:
                data['creation'] = "failed"
                data['message'] = "Passwords don't match"

        return JsonResponse(data)
