from django.urls import path

from . import views

urlpatterns = [
    path('auth/sign-up', views.sign_up, name="sign-up"),
    path('auth/sign-in', views.sign_in, name="sign-in"),
    path('users', views.user_list, name="user-list"),
    path('ai/ask', views.ai_helper, name="ai-helper"),
    path('hoots', views.hoot_list_create, name="hoot-list-create"),
    path('hoots/<int:hoot_id>', views.hoot_detail, name="hoot-detail"),
    path('hoots/<int:hoot_id>/comments', views.comment_create, name="comment-create"),
    path('hoots/<int:hoot_id>/comments/<int:comment_id>', views.comment_detail, name="comment-detail"),
]
