
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.log_and_reg), # main page that shows the form
    path('register', views.register), # Path hooked up to register form
    path('login',views.login), # path hooked up to Login Form
    path('index', views.index), # Path that generates a home page after you logged in.
    path('logout', views.logout), # path hooked up to the logout button.
    path('wall', views.wall),
    path('post_message', views.post_message),
    path('messages/<int:message_id>/post_comment', views.post_comment),
    path('users/<int:user_id>', views.user),
    path('users/<int:user_id>/deleteUser', views.deleteUser),
    path('messages/<int:message_id>/like', views.like),
    path('messages/<int:message_id>/dislike', views.dislike),
    path('messages/<int:message_id>/edit', views.edit),
    path('messages/<int:message_id>/update', views.update),
    path('users/<int:user_id>/update', views.update_user),
    path('messages/<int:message_id>/delete', views.delete),
    path('messages/<int:comment_id>/deleteComment', views.deleteComment)
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)