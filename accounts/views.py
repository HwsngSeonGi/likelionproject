from django.shortcuts import render,redirect
from django.contrib.auth.models import User  #회원 관리해주는 기능 끌어오기 
from django.contrib import auth              #회원 권한관리 기능 끌어오기

def signup(request):
    if request.method == 'POST':
        # POST 요청이 들어온다면
        if request.POST['password1'] == request.POST['password2']:
        # 입력한 password1과 password2를 비교 만약 같으면 
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
        #새로운 회원을 추가한다.
        auth.login(request, user)
        #성공적으로 추가되면 바로 로그인시켜주고
        return redirect('home')
        # 홈으로 돌아가기.
    return render(request, 'signup.html')
    
def login(request):
    if request.method == 'POST':
        #post 요청이 들어온다면
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        # 입력받은 아이디와 비밀번호가 데이터베이스에 존재하는지 확인.
        if user is not None: 
            # 데이터 베이스에 회원정보가 존재한다면 로그인 시키고 home으로 돌아가기.
            auth.login(request, user)
            return redirect('home')
        else:
            # 회원정보가 존재하지 않는다면, 에러인자와 함께 login 템플릿으로 돌아가기. 
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    #로그아웃 시키고 홈페이지로 보내기
    return redirect('home')
    