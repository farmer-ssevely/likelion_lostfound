from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
######### auth User

# Create your views here.
def checkuser(getusername):
    try: 
        checkuser = User.objects.get(username=getusername)
        if checkuser is not None:
            return True
    except:
        return False

def checkemail(getemail):
    try:
        checkemail = User.objects.get(email=getemail)
        if checkemail is not None:
            return True
    except:
        return False

def signup(request):
    if request.method == 'POST':
        if request.POST['password']==request.POST['confirm-password']:
            if checkuser(request.POST['username']):
                messages.error(request, '이미 존재하는 유저 이름입니다.')
                return render(request, 'loginout/signup.html')
            if checkemail(request.POST['email']):
                messages.error(request, '이미 사용 중인 이메일 주소입니다.')
                return render(request, 'loginout/signup.html')
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['confirm-password'], email=request.POST['email'])
            auth.login(request, user, backend ='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다. 다시 입력해주세요.')
            return render(request, 'loginout/signup.html')
    else:
        return render(request, 'loginout/signup.html')
            # try: 
            #     checkuser = User.objects.get(username=request.POST['username'])
            #     if checkuser is not None:
            #         messages.error(request, '이미 존재하는 유저 이름입니다.')
            #         return render(request, 'loginout/signup.html')
            # except:
            #     user=User.objects.create_user(username=request.POST['username'], password=request.POST['confirm-password'], email=request.POST['email'])
            #     auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #     return redirect('home')


def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
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
        entered_email = request.POST.get('entered_email')
        try:
            user= User.objects.get(email=entered_email)
            return redirect('changepassword', user.pk)
        except:
            messages.error(request, '존재하지 않는 아이디입니다.')
            return render(request, 'loginout/findpassword.html')
    else:
        return render(request, 'loginout/findpassword.html')
        # except:
        #     return redirect('findpassword')
    """ if len(query_set) == 0:
            # no user
            return render(request, 'loginout/findpassword.html')
        else:
            # change password
            user = query_set[0]
            return redirect('loginout/changepassword', user.pk) """

def changepassword(request, user_pk):
    if request.method == 'POST':
        user_query = User.objects.get(pk=user_pk)
        if request.POST.get('newpassword1') == request.POST.get('newpassword2'):
            newpassword = request.POST.get('newpassword1')
            user_query.set_password(newpassword)
            user_query.save()
            return redirect('login')
        else:
            messages.error(request, '비밀번호가 서로 다릅니다. 다시 입력해주세요.')
            return redirect('changepassword', user_query.pk)
    else:
        user_query = User.objects.get(pk=user_pk)
        return render(request, 'loginout/changepassword.html', {'user': user_query })