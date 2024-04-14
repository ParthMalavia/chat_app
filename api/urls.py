
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", views.RegisterView.as_view()),

    # Chat app Urls
    path("my-inbox/<user_id>/", views.MyInbox.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetMessages.as_view()),
    path("send-message/", views.SendMessage.as_view()),

    path("profile/<int:pk>/", views.ProfileDetails.as_view()),
    path("search-user/<username>/", views.SearchUser.as_view()),
]
