from django.urls import path

import webtoonitda
from webtoonitda.views import base_views

app_name = 'webtoonitda'

urlpatterns = [
    # base
    path('', base_views.index, name='index'),
    path('webtoon_summary/', base_views.webtoon_summary, name='webtoon_summary'),

    path('show_num_reviews/<str:lang>/<str:platform>/<str:webtoon>', base_views.show_num_reviews, name="show_num_reviews"),
    path('get_best_episodes_by_reviews/<str:lang>/<str:platform>/<str:webtoon>', base_views.get_best_episodes_by_reviews, name="get_best_episodes_by_reviews"),
    path('get_best_episodes/<str:lang>/<str:platform>/<str:webtoon>', base_views.get_best_episodes, name="get_best_episodes"),
  ]
