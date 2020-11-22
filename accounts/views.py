from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout


'''registration'''
def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    #if they are not logged in
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST or None)

            '''check if form is valid'''
            if form.is_valid():
                user = form.save()

                '''get the row password'''
                row_password = form.cleaned_data.get('password1')

                '''authenticate the user'''
                user = authenticate(username=user.username, password=row_password)

                '''user login'''
                login(request, user)

                return redirect('main:home')
        else:
            form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


'''login'''
def login_user(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            '''check the credentials'''
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main:home')
                else:
                    return render(request, 'accounts/login.html', {'error': 'Your account has been disabled.'})
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid Username or Password. Try again.'})
        return render(request, 'accounts/login.html')


'''logout'''
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print('Logged out succesfully')
        return redirect('accounts:login')
    else:
        return redirect('accounts:login')