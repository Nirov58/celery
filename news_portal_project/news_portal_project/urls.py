from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('protection_app.urls')),
    path('sign/', include('sign_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news_portal_app.urls')),
    path('article/', include('news_portal_app.urls'))
]
