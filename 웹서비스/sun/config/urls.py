from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from pybo.views import base_views
from webtoonitda.views import base_views


urlpatterns = [
    path('', base_views.login, name='login'),  # http://127.0.0.1:8000

    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('webtoonitda/', include('webtoonitda.urls')), # http://127.0.0.1:8000/webtoonitda/
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

handler404 = 'common.views.page_not_found'
