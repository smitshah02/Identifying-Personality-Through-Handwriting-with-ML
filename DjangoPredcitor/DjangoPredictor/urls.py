"""
URL configuration for DjangoPredictor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path
from predictor import views  # Assuming your app is named 'predictor'

urlpatterns = [
    path('', views.index, name='index'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    #path('page4/', views.page4, name='page4'),
    path('predict/', views.predict, name='predict'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)