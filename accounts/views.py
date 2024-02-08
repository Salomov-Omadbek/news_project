from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,ProfileEditForm,UserEditForm
from .models import Profile
def user_login(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Muvafaqiyatli bajarildi')
                else:
                    return HttpResponse('Qaytadan urinib korin')
            else:
                return HttpResponse('Login paolda xatolik bor')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html',{form:'form'})


def dashboard(request):
    user = request.user
    context = {
        'user':user
    }

    return render(request, 'pages/dashboard.html', context)

def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user':new_user
            }
            return render(request,'account/register_done.html',context)
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form =UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
    return render(request,'account/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})
