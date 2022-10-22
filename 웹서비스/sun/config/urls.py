from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from pybo.views import base_views
from webtoonitda.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),   # http://127.0.0.1:8000
    path('webtoonitda/', include('webtoonitda.urls')), # http://127.0.0.1:8000/webtoonitda/
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

handler404 = 'common.views.page_not_found'
