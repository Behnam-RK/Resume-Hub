from django.urls import path
from hub.views import *


app_name = 'hub'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('dashboard/', dashboard, name='dashboard'),
    path('change_profile_pic/', change_profile_pic, name='change_profile_pic'),
    path('resume/<int:user_profile_id>/', resume, name='resume'),
    path('comment/', comment, name='comment'),
    path('doc/', doc, name='doc'),
    path('about/', about, name='about'),
    path('error/<error_title>', error, name='error')
]