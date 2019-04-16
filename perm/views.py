from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Article
from .forms import RegisterationForm
from django.contrib.auth.hashers import make_password
from .decorators import group_required
# Create your views here.


@group_required('Super_visior', 'Tenant_Admin', 'Security_personal')
def my_view(request):
    data = {}
    if request.user.is_authenticated:
        if request.user.has_perm("perm.can_view_odd_ids"):
            data = Article.objects.all()[1::2]
        elif request.user.has_perm("perm.can_view_even_ids"):
            data = Article.objects.all()[0::2]
    return render(request, 'index.html', {'data': data})


def register_view(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.password = make_password(user.password)
            user.save()
        else:
            print(form.errors)
    else:
        form = RegisterationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view')
        else:
            return HttpResponse("Your username and password didn't match.")
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')
