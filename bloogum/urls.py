"""bloogum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('post/<int:pk>/',views.PostCommentsListView.as_view(), name='post_detail'),
    path('post/<int:pk>/new-comment/',views.CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_pk>/comment/<int:pk>/update/',
         views.CommentUpdateView.as_view(), name='comment_update'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/',
         views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('user/<username>/', views.UserPostsListView.as_view(), name='user_posts'),
    path('myprofile/password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('myprofile/password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('myprofile/', views.ProfileView.as_view(), name='profile'),
    path('contactus/', views.ContactUsView.as_view(), name='contact_us'),
    path('about/', TemplateView.as_view(template_name="blog/about.html"), name='about'),
    path('', views.PostListView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
