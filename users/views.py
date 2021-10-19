from django.shortcuts import render

# Create your views here.
def login(request):
    title = 'GeekShop - Авторизация'
    return render(request, 'users/login.html', {'title': title})

def registration(request):
    title = 'GeekShop - Регистрация'
    return render(request, 'users/registration.html', {'title': title})
