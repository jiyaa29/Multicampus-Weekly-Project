import logging
import os

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import redirect, render

from webtoonitda.models import Webtoon
from webtoonitda.views.naver_webtoon import get_webtoon_titleId, get_top10_point_participants, get_top10_num_reviews, \
    get_titleId_num_episodes, show_iplot_best_episodes_by_points, show_best_by_points
from webtoonitda.views.review_webtoon import get_reviews

logger = logging.getLogger('webtoonitda')

def login(request):
    return render(request, 'common/login.html')

def index(request):
    if request.user.is_authenticated:
        return render(request, 'webtoonitda/index.html')
    else:
        return render(request, 'common/login.html')

def show_similarity(request):
    print("show_similarity")
    return render(request, 'webtoonitda/show_similarity.html')


def episode_page(request):
    if request.method == 'POST':
        episode = request.POST.get('episode')
        print("episode " + str(episode) + "를 분석합니다.")

        context = {
            'episode': str(episode)
        } # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트
        return render(request, 'webtoonitda/episode_page.html', context)

def service_summary(request):
    if request.method == 'POST':
        print("service_summary POST")

        lang = request.POST.get('lang')
        platform = request.POST.get('platform')
        webtoon = request.POST.get('webtoon')

        # db 생성
        # Webtoon.objects.create(lang=lang, platform=platform, webtoon=webtoon)

        context = {
            'lang': lang,
            'platform': platform,
            'webtoon': webtoon,
        } # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트
        return render(request, 'webtoonitda/service_summary.html', context)

def show_num_reviews(request, lang, platform, webtoon):
    context = {
        'lang': lang,
        'platform': platform,
        'webtoon': webtoon,
    }  # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트
    return render(request, 'webtoonitda/show_num_reviews.html', context)

def show_best_episodes_by_reviews(request, lang, platform, webtoon):

    print(os.getcwd())

    # 1. 동적으로 크롤링하여 결과 보여주기

    #chromedriver_path = '/media/kr/'  # 윤지 크롬드라이브 경로
    chromedriver_path = 'c:\python\chromedriver.exe' #윤지 크롬드라이브 경로
    #chromedriver_path = 'c:\Temp\chromedriver.exe' 선미님 크롬드라이브 경로
    # titleId = get_webtoon_titleId(chromedriver_path, platform, lang, webtoon)
    # print("titleId: " + str(titleId))

    DATA_DIR = os.getcwd() + "/media/kr/"
    USE_CSV_FILE = True

    title_id, num_episodes = get_titleId_num_episodes(chromedriver_path, platform, lang, webtoon, USE_CSV_FILE)

    df = get_top10_num_reviews(chromedriver_path, platform, lang, title_id, num_episodes, USE_CSV_FILE)

    print("Done")

    context = {
        'lang': lang,
        'platform': platform,
        'webtoon': webtoon,
        'df': df[:10].to_html(justify='center')
    }  # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트

    return render(request, 'webtoonitda/show_best_episodes_by_reviews.html', context)

def show_keywords(request, lang, platform, webtoon):

    print("show_keywords lang: " + lang)
    print("show_keywords platform: " + platform)
    print("show_keywords webtoon: " + webtoon)

    context = {
        'lang': lang,
        'platform': platform,
        'webtoon': webtoon,
    }  # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트

    return render(request, 'webtoonitda/show_keywords.html', context)

def show_topic_keywords(request, lang, platform, webtoon):

    print("show_topic_keywords lang: " + lang)
    print("show_topic_keywords platform: " + platform)
    print("show_topic_keywords webtoon: " + webtoon)

    context = {
        'lang': lang,
        'platform': platform,
        'webtoon': webtoon,
    }  # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트

    return render(request, 'webtoonitda/show_topic_keywords.html', context)

def show_participants(request, lang, platform, webtoon):

    print("show_topic_keywords lang: " + lang)
    print("show_topic_keywords platform: " + platform)
    print("show_topic_keywords webtoon: " + webtoon)

    context = {
        'lang': lang,
        'platform': platform,
        'webtoon': webtoon,
    }  # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트

    return render(request, 'webtoonitda/show_participants.html', context)
def show_best_episodes_by_points(request, lang, platform, webtoon):

    USE_CSV_FILE = False

    # 1. 동적으로 크롤링하여 결과 보여주기
    DATA_DIR = os.getcwd() + "/media/kr/"
    if USE_CSV_FILE:
        # 저장된  csv 파일을 읽어온다.
        df = pd.read_csv(DATA_DIR + 'kr_전지적 독자 시점_best_by_points.csv')
    else:
        # 크롤링 한다.
        chromedriver_path = 'c:\python\chromedriver.exe' #윤지 크롬드라이브 경로
        # chromedriver_path = 'c:\Temp\chromedriver.exe' 선미님 크롬드라이브 경로
        titleId = get_webtoon_titleId(chromedriver_path, platform, lang, webtoon)
        print("titleId: " + str(titleId))
        df = get_top10_point_participants(chromedriver_path, platform, lang, titleId)
        print("Done")

        # 결과를 저장한다
        df.to_csv(DATA_DIR + '{lang}_{webtoon}_best_by_points.csv'.format(lang=lang, webtoon=webtoon), index=False)
        print("Saved.")

    df = df.drop('Point', axis=1)
    df = df.sort_values(by=['Participant'], ascending=False)

    df_reverse = df.loc[::-1]

    # 시각화 파일을 저장한다.
    #filename = lang + '_'+ webtoon + '_best_episodes_by_points.png'
    filename = "generated.png"
    filepath = DATA_DIR + filename
    show_best_by_points(df_reverse[:10], filepath, webtoon)

    #filename = 'kr_iplot_best_episodes_by_points.png'
    #df = df.set_index('Title')
    #show_iplot_best_episodes_by_points(df_reverse, filename)

    context = {
        'df': df[:10].to_html(justify='center'),
        'filename': filename,
    }


    return render(request, 'webtoonitda/show_best_episodes_by_points.html', context)

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
    return render(request, 'webtoonitda/show_best_episodes_by_points.html', context)


#윤지
def ep_review(request):
  return render(request, 'webtoonitda/ep_review.html')


import pandas as pd
def ep_search(request):
    if request.method == 'POST':
          keyword = request.POST.get('keyword')
          print("ep_review POST" + keyword)
          DATA_DIR = os.getcwd() + "/media/kr/"

          print("Read csv file.")
          filepath = DATA_DIR + "omniscient-reader_Episode_kr_21.csv"
          df = pd.read_csv(filepath)

          test = df[df['Review'].str.contains(keyword)]  # df에 keyword파라미터 받음
          df = test.sample(10)  # 원하는 개수만큼 추출
          print(type(df))



          context = {
              'df': df[:10].to_html(justify='center')


          } # 템플릿에 전달할 데이터를 세팅할 수 있는 오브젝트

          # return HttpResponse("ep_search keyword:" + title)
    return render(request, 'webtoonitda/show_21_episodes.html', context)
# )

