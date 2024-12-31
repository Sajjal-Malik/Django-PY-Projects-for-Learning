from django.urls import path
from . import views

urlpatterns = [
    path("blogpostslist/", views.BlogPostList.as_view(), name="blogpost-view"),
    path("blogposts/", views.BlogPostListCreate.as_view(), name="blogpost-view-create"),
    path("blogposts/<int:pk>", views.BlogPostRetrieveUpdateDestroy.as_view(), name="blogpost-retrive-update-delete"),
]
