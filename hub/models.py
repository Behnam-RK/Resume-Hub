from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    '''
    for detecting user directory path
    '''
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    ''' 
    Model for storing resume of user and profile picture and other data...!
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # For detect special users (for example teacher user)
    is_special = models.BooleanField(default=False)

    picture = models.ImageField(upload_to=user_directory_path, blank=True)

    resume_file = models.FileField(upload_to=user_directory_path, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    ''' 
    Model for storing comments on resumes!
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def init_users():
    '''
    Function for insert specific users in User Model
    '''
    try:
        # Admin User
        admin = User.objects.create_superuser(username='admin', email='admin@resume-hub.com', password='changeit', first_name='Admin')
        admin_user_profile = UserProfile(user=admin, is_special=True)
        admin_user_profile.save()

        # Teacher User
        teacher_user = User.objects.create_user(username='teacher', email='habiballah_khosravi@yahoo.com', password='changeit', first_name='Habiballah', last_name='Khosravi')
        teacher_user_profile = UserProfile(user=teacher_user, is_special=True)
        teacher_user_profile.save()

    except:
        pass

init_users()
