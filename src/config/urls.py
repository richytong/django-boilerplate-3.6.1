from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views

'''
urls for the project
any apps you create should be included here
'''

urlpatterns = [
    # url(r'^customapp/', include('customapp.urls')),
    url(r'^admin/', admin.site.urls),
]