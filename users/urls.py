from django.urls import path 



from .views import(
    UserRegistrationView, 
    UserLoginView, 
    UserListView, 
    CustomTokenRefreshView,
    ProfileListView,
    PasswordUpdateView,
    approve_user, 
    reject_user,
    user_logout_view,
    
)



urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('list/', UserListView.as_view()),
    path('profile/', ProfileListView.as_view()),
    path('password-change/<int:pk>/', PasswordUpdateView.as_view()),
    path('approve-user/<int:pk>/', approve_user),
    path('reject-user/<int:pk>/', reject_user),
    path('logout/', user_logout_view),


    path('token/refresh/', CustomTokenRefreshView.as_view()),
    
]

