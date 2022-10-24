from django.urls import path

import webtoonitda
from webtoonitda.views import base_views

app_name = 'webtoonitda'

urlpatterns = [
    # base
    #path('', base_views.index, name='index'),

    path('index/', base_views.index, name='index'),  # http://127.0.0.1:8000/webtoonitda/index
    path('service_summary/', base_views.service_summary, name='service_summary'),

    path('show_num_reviews/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_num_reviews, name="show_num_reviews"),
    path('get_best_episodes_by_reviews/<str:lang>/<str:platform>/<str:webtoon>', base_views.get_best_episodes_by_reviews, name="get_best_episodes_by_reviews"),
    path('get_best_episodes/<str:lang>/<str:platform>/<str:webtoon>', base_views.get_best_episodes, name="get_best_episodes"),

    path('show_keywords/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_keywords, name="show_keywords"),

#윤지 작성
    path('ep_review', base_views.ep_review, name='ep_review')
]
