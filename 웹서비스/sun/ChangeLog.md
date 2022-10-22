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

이전 페이지로 돌아가는 버튼을 누르면 다시 선택했던 파라미터가 리셋되는 문제가 발생했다.

이를 해결하기 위해서는 특정 기간동안 저장할 수 있는 쿠키를 이용해야한다.
이번엔 파라미터로 넘기는 방법을 알아보고, 다음에 쿠키를 이용하는 방법을 알아보자.

index.html , javascript로 

<form action="{% url 'webtoonitda:webtoon_summary' %}" method="POST">
	....
 	<button a href="{% url 'webtoonitda:webtoon_summary' %}" onclick="clickStartAnalysis()">Go!</button>

def webtoon_summary(request):
    if request.method == 'POST':
        lang = request.POST.get('lang')
        platform = request.POST.get('platform')
        webtoon = request.POST.get('webtoon') 	

request.POST.get('name') 와 같은 형태로
request.POST.get을 활용해 name에 해당하는 입력 값을 받아온다.      


create() 같은 경우, 쿼리를 만들어서 바로 실행까지 넘어간다.  

form을 post로 전송한 후 뒤로가기시 아래와 같은 오류 내용이 표시
출처: https://yy8305.tistory.com/20 [인생을 바꾸는 기록:티스토리]
 

<a href="javascript:history.back();">뒤로가기</a>


DEFAULT_FILE_STORAGE 추가 


import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

urls.py

urlpatterns += static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)