from django.urls import path, include
from account.views import DeleteTableRow, SendPasswordResetEmailView, UpdateProfile, UpdateTable, UserChangePasswordView, UserPasswordResetView, UserProfileView, UserRegistrationView, UserLoginView, UserStudentListData, UserTeacherListData
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'register'),
    path('login/', UserLoginView.as_view(), name= 'login'),
    path('profile/', UserProfileView.as_view(), name= 'profile'),
    path('update-profile/<int:uid>/', UpdateProfile.as_view(), name= 'update-profile'),
    path('update-table/<int:uid>/', UpdateTable.as_view(), name= 'update-table'),
    path('delete-row/', DeleteTableRow.as_view(), name= 'delete'),
    path('teacherslist/', UserTeacherListData.as_view(), name= 'teacherslist'),
     path('studentslist/', UserStudentListData.as_view(), name= 'studentlist'),
    path('changepassword/', UserChangePasswordView.as_view(), name= 'changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name= 'send-reset-password-email'),
    # after resetpassword form submited then run this link Uod with token
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name= 'reset-password'),
    
   
]