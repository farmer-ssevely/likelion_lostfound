from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth 
######### auth User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['password']==request.POST['confirm-password']:
            user=User.objects.create_user(username=request.POST['username'], password=request.POST['confirm-password'], email=request.POST['email'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        return render(request, 'loginout/signup.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'loginout/login.html', {'error':'username or password is incorrect'})
    else:
        return render(request, 'loginout/login.html')
    return render(request, 'loginout/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

""" def home(request):
    return redirect('home') """

def findpassword(request):
    if request.method == 'POST':
        try:
            entered_email = request.POST['entered_email']
            query_set = auth.get_user_model().objects.get(email=entered_email)
            return redirect('loginout/changepassword', user.pk)
        except:
            return redirect('findpassword')
    else:
        return render(request, 'loginout/findpassword.html')
    
    """ if len(query_set) == 0:
            # no user
            return render(request, 'loginout/findpassword.html')
        else:
            # change password
            user = query_set[0]
            return redirect('loginout/changepassword', user.pk) """

def changepassword(request, pk):
    if request.method == 'POST':
        if request.POST['newpassword1'] == request.POST['newpassword2']:
            user_query = auth.get_user_model().objects.get(pk=pk)
            user_query.password = "newpassword1"
            user_query.save()
            return render(request, 'loginout/login.html')
        else:
            return render(request, 'loginout/changepassword.html')
    else:
        return render(request, 'loginout/changepassword.html')