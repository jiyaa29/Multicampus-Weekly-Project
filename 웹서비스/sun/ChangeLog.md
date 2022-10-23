# Base
--------------------------------------------------------------------------
+ superuser 생성완료(admin/admin1234)
+ auth, pybo DB 생성완료 
--------------------------------------------------------------------------

# sun 2022.10.21( home 페이지 webtoonitda용 index page로 변경 )
--------------------------------------------------------------------------
+ mysite\README.md
	mysite\ChangeLog.md로 이름 변경

+ mysite\templates
	    webtoonitda 폴더 생성

+ mysite\config\urls.py 
		webtoonitda app의 base_views.index로 변경 

+ webtoonitda\views\base_views.py
		views 디렉토리 생성
		index 함수 생성

		def index(request):
		    return render(request, 'webtoonitda/index.html')		
+ mysite\templates\webtoonitda
		index.html 생성

--------------------------------------------------------------------------


# sun 2022.10.21(pybo 링크명 변경)
--------------------------------------------------------------------------
+ navbar.html
	<a class="navbar-brand" href="{% url 'pybo:index' %}">Community</a>

+ webtoonitda link navbar에 home 으로 추가 

+ config/setting/base.py

	INSTALLED_APPS = [
	    'common.apps.CommonConfig',
	    'pybo.apps.PyboConfig',
	    'webtoonitda.apps.WebtoonitdaConfig', 추가 

+ namespace 생성을 위해 

	webtoonitda\urls.py 생성 


+ config\urls.py 수정
    #path('', base_views.index, name='index'),  # '/' 에 해당되는 path
    path('', base_views.index, name='index'),   # http://127.0.0.1:8000
    path('webtoonitda/', include('webtoonitda.urls')), # http://127.0.0.1:8000/webtoonitda/

+ templates\base.html
	<title>Hello, pybo!</title>
	-> Hello, webtoonitda! 로 수정 
--------------------------------------------------------------------------

<form action="{% url 'webtoonitda:webtoon_summary' %}" method="POST">
	....
 	<button onclick="clickStartAnalysis()">Go!</button>

def webtoon_summary(request):
    if request.method == 'POST':
        lang = request.POST.get('lang')
        platform = request.POST.get('platform')
        webtoon = request.POST.get('webtoon') 	

request.POST.get('name') 와 같은 형태로
request.POST.get을 활용해 name에 해당하는 입력 값을 받아온다.      

--------------------------------------------------------------------------
DB 생성
--------------------------------------------------------------------------
create() 같은 경우, 쿼리를 만들어서 바로 실행까지 넘어간다.  


--------------------------------------------------------------------------
뒤로가기
--------------------------------------------------------------------------
<a href="javascript:history.back();">뒤로가기</a>

--------------------------------------------------------------------------
MEDIA_URL 추가 
--------------------------------------------------------------------------
settings/base.py

	import os

	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

urls.py

	urlpatterns += static(
	    settings.MEDIA_URL, 
	    document_root = settings.MEDIA_ROOT
	)
--------------------------------------------------------------------------


--------------------------------------------------------------------------
# sun 2022.10.22( home 페이지를 다시 common 로그인 페이지로 변경)
--------------------------------------------------------------------------

http://127.0.0.1:8000/common/login/

def index(request):
    return render(request, 'common/login.html')
    #return render(request, 'webtoonitda/index.html')

--------------------------------------------------------------------------
common\urls.py

path('login/', auth_views.LoginView.as_view(), name="login"),
path('logout/', auth_views.LogoutView.as_view(), name="logout"),     

jango auth에 내장되어 있는 LoginView, LogoutView를 사용할 수 있다. 
따라서 앱 폴더의 views.py에서 따로 코드를 작성할 필요가 없다.

as auth_views로 alias(별칭)을 주는 이유는 
앱 폴더 내에 있는 views.py와 충돌하지 않도록 다른 이름을 사용한 것이다.


<input type="hidden" name="next" value="{{ next }}">  <!-- 로그인 성공후 이동되는 URL -->

[파일명: projects\mysite\config\settings.py]


# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'

->

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/webtoonitda/index/'

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'


[파일명: C:\projects\mysite\config\urls.py]

path('', views.index, name='index'),  # '/' 에 해당되는 path


<h1>로그인</h1>
 <form action="{% url 'login' %}" method="POST">
     {% csrf_token %}
     Username: <input type="text" name="username" id="">
     <br>
     Password: <input type="password" name="password" id="">
     <br>
     <input type="hidden" name="next" value="{{ next }}">
     <input type="submit" value="login" id="">
 </form>
로그인 페이지 내의 <form></form> 태그 안의 next input 주목 !
로그인을 하면 <input type="hidden" name="next" value="{{ next }}"> 로 redirect 되게 한다.
👉🏻 즉, 로그인 페이지로 들어올 때, login url 뒤에 붙어있던 next 변수 안에 담긴 path로 redirect 하는 것이다.

여기서 일반적인 로그인 구현에 더해서, 만약 'next'가 request.POST에 있다면 request.POST.get('next')로 redirect 하게끔 구현해주었다. 이를 통해 로그인을 하면 원하는 페이지로 바로 접근이 가능하게끔 구현을 해주었다.

--------------------------------------------------------------------------  

회원 가입 후에 다시 같은 로그인 페이지가 load됨 , 웹툰 페이지로 이동해야 함.
회원 가입 후  webtoonitda/index.html 로 이동함 


common/views.py

def signup(request):

            if user is not None:
                login(request, user)  # 로그인
                #return redirect('index')  <-------------------

                # 로그인 된 후 webtoonitda main page로 이동
                return render(request, 'webtoonitda/index.html')
            else:
                # Return an 'invalid login' error message.
                return redirect('index')
                # return render(request, 'common/login.html')
--------------------------------------------------------------------------

http://127.0.0.1:8000/ 에서 로그아웃 상태이면 common/login.html

http://127.0.0.1:8000/ 에서 로그인 상태라면  webtoonitda/index.html

--------------------------------------------------------------------------
로그인 후에 다시 같은 로그인 페이지가 load됨 , 웹툰 페이지로 이동해야 함.
로그인 이후 특정 페이지로 이동하기 (로그인 버튼을 클릭하면 webtoonitda/index.html 로 이동하기)

특정 페이지(A)에 들어가려고 한다
로그인이 되어 있지 않으므로 웹사이트에서 바로 로그인 페이지로 redirect한다.
로그인을 하면 로그인 후 원래 가려던 페이지(A)로 바로 redirect 된다.   


http://127.0.0.1:8000/webtoonitda/index/ 로 direct 접근하면 서비스 되는 문제가 있다.

-> 로그인이 되어 있지 않으므로 웹사이트에서 바로 로그인 페이지로 redirect한다.


webtoonitda/views/base_views.py

def index(request):
    if request.user.is_authenticated:
        return render(request, 'webtoonitda/index.html')
    else:
        return render(request, 'common/login.html')


--------------------------------------------------------------------------     
templates\pybo\question_list.html

<form id="searchForm" method="get" action="{% url 'index' %}">

<form id="searchForm" method="get" action="{% url 'pybo:index' %}">

로그아웃 상태인데 http://127.0.0.1:8000/pybo/	 접근시 서비스 되는 문제


pybo\views\base_views.py
def index(request):

    if request.user.is_authenticated:
    	.....
        return render(request, 'pybo/question_list.html', context)
    else:
        return render(request, 'common/login.html')
--------------------------------------------------------------------------     