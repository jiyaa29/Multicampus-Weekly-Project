import logging
import os

from django.http import HttpResponse
from django.shortcuts import redirect, render

from webtoonitda.models import Webtoon
from webtoonitda.views.naver_webtoon import get_webtoon_titleId, get_top10_point_participants, get_top10_num_reviews, \
    get_titleId_num_episodes

logger = logging.getLogger('webtoonitda')

def index(request):
    return render(request, 'webtoonitda/index.html')

def webtoon_summary(request):
    if request.method == 'POST':
        print("webtoon_summary POST")

        lang = request.POST.get('lang')
        platform = request.POST.get('platform')
        webtoon = request.POST.get('webtoon')

        print("webtoon_summary lang: " + lang)
        print("webtoon_summary platform: " + platform)
        print("webtoon_summary webtoon: " + webtoon)

        # db 생성
        # Webtoon.objects.create(lang=lang, platform=platform, webtoon=webtoon)

        context = {
            'lang': lang,
            'platform': platform,
            'webtoon': webtoon,
        } # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트
        return render(request, 'webtoonitda/webtoon_summary.html', context)

def show_num_reviews(request, lang, platform, webtoon):

    print("show_num_reviews lang: " + lang)
    print("show_num_reviews platform: " + platform)
    print("show_num_reviews webtoon: " + webtoon)

    context = {'df': 'num_reviews'}
    return render(request, 'webtoonitda/show_num_reviews.html', context)

def get_best_episodes_by_reviews(request, lang, platform, webtoon):

    print("get_best_episodes_by_reviews lang: " + lang)
    print("get_best_episodes_by_reviews platform: " + platform)
    print("get_best_episodes_by_reviews webtoon: " + webtoon)

    print(os.getcwd())

    # 1. 동적으로 크롤링하여 결과 보여주기
    chromedriver_path = 'c:\Temp\chromedriver.exe'
    # titleId = get_webtoon_titleId(chromedriver_path, platform, lang, webtoon)
    # print("titleId: " + str(titleId))

    DATA_DIR = os.getcwd() + "/media/"
    USE_CSV_FILE = True

    title_id, num_episodes = get_titleId_num_episodes(chromedriver_path, platform, lang, webtoon, USE_CSV_FILE)

    df = get_top10_num_reviews(chromedriver_path, platform, lang, title_id, num_episodes, USE_CSV_FILE)

    print("Done")

    context = {'df': df[:10].to_html(justify='center')}
    return render(request, 'webtoonitda/show_best_episodes_by_reviews.html', context)

def get_best_episodes(request, lang, platform, webtoon):

    print("get_best_episodes lang: " + lang)
    print("get_best_episodes platform: " + platform)
    print("get_best_episodes webtoon: " + webtoon)

    # 1. 동적으로 크롤링하여 결과 보여주기
    chromedriver_path = 'c:\Temp\chromedriver.exe'
    titleId = get_webtoon_titleId(chromedriver_path, platform, lang, webtoon)
    print("titleId: " + str(titleId))
    df = get_top10_point_participants(chromedriver_path, platform, lang, titleId)
    print("Done")

    context = {'df': df[:10].to_html(justify='center')}
    return render(request, 'webtoonitda/show_best_episodes.html', context)

    # 2. csv 저장된 csv 파일에서 가져와서 보여주기

    # 저장된 csv 파일에서 가져오기
    # df = pd.read_csv('C:\MyJupiter\삼성멀티캠\_Django\workspace\webtoonsite\webtoon1\전독시_인기_에피소드.csv', index_col = 0)

    # DB 에 data를 생성하기
    # for i in range(10):
    #     BestEpisodes.objects.create(title=df['Title'][i], point=df['Point'][i], participant=df['Participant'][i])
    #     print(df['Point'][i])
    #
    # # DB 에서 데이터 가져오기
    # all_episode = BestEpisodes.objects.all().order_by('-id')

    context = {'df': df[:10].to_html(justify='center')}
    return render(request, 'webtoonitda/show_best_episodes.html', context)

