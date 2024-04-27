"""
URL configuration for gamestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path
from games.views import HomeView, GameUpdateView, GameCreateView, GameDetailView, GameDeleteView, \
    PublisherDetailView, PublisherDeleteView, PublisherUpdateView, PublisherListView, PublisherCreateView, \
    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryDeleteView, CategoryUpdateView
from django.conf.urls.static import static

from gamestore import settings



urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('admin/', admin.site.urls),
                  path('add_publisher/', PublisherCreateView.as_view(), name='add_publisher'),
                  path('add_game/', GameCreateView.as_view(), name='add_game'),
                  path('game/<int:game_id>/', GameDetailView.as_view(), name='game_detail'),
                  path('game/<int:game_id>/delete/', GameDeleteView.as_view(), name='delete_game'),
                  path('game/<int:game_id>/update/', GameUpdateView.as_view(), name='update_game'),
                  path('publisher/<int:publisher_id>/', PublisherDetailView.as_view(), name='publisher_detail'),
                  path('publisher/<int:publisher_id>/delete/', PublisherDeleteView.as_view(), name='delete_publisher'),
                  path('publisher/<int:publisher_id>/update/', PublisherUpdateView.as_view(), name='update_publisher'),
                  path('publishers/', PublisherListView.as_view(), name='publishers'),
                  path('add_category/', CategoryCreateView.as_view(), name='add_category'),
                  path('categories/', CategoryListView.as_view(), name='categories'),
                  path('category/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
                  path('category/<int:category_id>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
                  path('category/<int:category_id>/update/', CategoryUpdateView.as_view(), name='update_category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Адміністрування ігрового магазину'
admin.site.index_title = 'Моделі застосунку'
admin.site.site_title = 'Ігровий магазин'
