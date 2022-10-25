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
    path('show_best_episodes_by_reviews/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_best_episodes_by_reviews, name="show_best_episodes_by_reviews"),
    path('show_best_episodes_by_points/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_best_episodes_by_points, name="show_best_episodes_by_points"),
    path('show_participants/<str:lang>/<str:platform>/<str:webtoon>',base_views.show_participants, name="show_participants"),

    path('show_keywords/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_keywords, name="show_keywords"),
    path('show_topic_keywords/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_topic_keywords, name="show_topic_keywords"),
    path('episode_page', base_views.episode_page, name="episode_page"),
    path('show_similarity', base_views.show_similarity, name="show_similarity"),

#윤지 작성
    path('ep_review', base_views.ep_review, name='ep_review'),
    path('ep_search', base_views.ep_search, name='ep_search'),
]
