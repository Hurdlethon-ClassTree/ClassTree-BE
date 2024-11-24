from django.contrib.auth import logout
from django.shortcuts import redirect

def Logout_view(request):
    logout(request)  # 세션을 종료하여 로그아웃 처리
    return redirect('/')  # 로그아웃 후 리디렉션할 URL (예: 홈 화면)