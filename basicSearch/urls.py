from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_restaurants, name="search_restaurants"),
    path("populate/", views.populate_sample_data, name="populate_sample_data"),
    path("restaurant/<uuid:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("cache/clear/", views.clear_search_cache, name="clear_search_cache"),
    path("cache/stats/", views.get_cache_stats, name="get_cache_stats"),
]