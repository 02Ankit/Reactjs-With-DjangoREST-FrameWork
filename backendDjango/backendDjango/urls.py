
from django.contrib import admin
from django.urls import path
from myapi.views import UserViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserViews.as_view())
]
