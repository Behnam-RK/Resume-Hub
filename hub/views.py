from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
import re
from .models import *
from .forms import *


ERRORS = {
    'invalid_username_or_password': 'Invalid username or password!',
    'account_is_not_activated': 'Your account is not activated!',
    'wrong_current_password': 'Wrong current password!',
    'restricted_section': 'Sorry, You can\'t have access to this section!',
    'not_same_passwords': 'oops! the two passwords you entered are different!'
}

def index(request):
    data = dict()

    resumes = UserProfile.objects.order_by('updated_at')
    resumes = resumes.reverse()
    if len(resumes) > 20:
        resumes = resumes[:20]

    resumes = [to_dict(resume) for resume in resumes]
    data['resumes'] = resumes

    return render(request, 'hub/index.html', context=data)

def register(request):
    data = dict()

    registered = False

    if request.user.is_authenticated:
        return redirect(reverse('hub:index'))

    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)

        if register_form.is_valid():
            password = request.POST['password']
            repeat_password = request.POST['repeat_password']
            if password != repeat_password:
                return redirect(
                    reverse(
                        'hub:error',
                        kwargs={
                            'error_title': 'not_same_passwords'
                        }
                    )
                )

            user = register_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

            login_user(request, user)

        else:
            error_data = {
                'error_message_alter': register_form.errors.as_ul()
            }
            return render(request, 'hub/error.html', context=error_data)

    else:
        register_form = RegisterForm()

    data['register_form'] = register_form
    data['registered'] = registered

    return render(request, 'hub/register.html', context=data)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login_user(request, user)
                return redirect(reverse('hub:index'))
                
            else:
                return redirect(
                    reverse(
                        'hub:error',
                        kwargs={
                            'error_title': 'account_is_not_activated'
                        }
                    )
                )

        else:
            return redirect(
                reverse(
                    'hub:error',
                    kwargs={
                        'error_title': 'invalid_username_or_password'
                    }
                )
            )

    else:
        return redirect(reverse('hub:index'))

@login_required
def logout(request):
    logout_user(request)
    return redirect(reverse('hub:index'))

@login_required
def dashboard(request):
    data = dict()

    if request.method == 'POST':
        resume_form = ResumeForm(data=request.POST)

        if resume_form.is_valid():
            profile = getattr(request.user, 'userprofile', None)
            if profile:
                profile.description = resume_form.cleaned_data['description']

                if 'resume_file' in request.FILES:
                    profile.resume_file = request.FILES['resume_file']

                profile.save()

                data['current_file'] = profile.resume_file

            else:
                profile = resume_form.save(commit=False)
                profile.user = request.user

                if 'resume_file' in request.FILES:
                    profile.resume_file = request.FILES['resume_file']

                profile.save()

                data['current_file'] = profile.resume_file

        else:
            error_data = {
                'error_message_alter': resume_form.errors.as_ul()
            }
            return render(request, 'hub/error.html', context=error_data)

    else:
        profile = getattr(request.user, 'userprofile', None)
        if profile:
            d = {
                'description': profile.description,
                'resume_file': profile.resume_file
            }
            resume_form = ResumeForm(data=d)

            data['current_file'] = profile.resume_file

        else: 
            resume_form = ResumeForm()

    data['resume_form'] = resume_form

    return render(request, 'hub/dashboard.html', context=data)

@login_required
def change_password(request):
    data = dict()

    password_changed = False

    if request.method == 'POST':
        change_password_form = ChangePasswordForm(data=request.POST)
        
        if change_password_form.is_valid():
            
            change_password_form = change_password_form.cleaned_data
            
            user = request.user

            if user.check_password(change_password_form['current_password']):
                new_password = request.POST['new_password']
                repeat_new_password = request.POST['repeat_new_password']
                if new_password != repeat_new_password:
                    return redirect(
                        reverse(
                            'hub:error',
                            kwargs={
                                'error_title': 'not_same_passwords'
                            }
                        )
                    )

                user.set_password(change_password_form['new_password'])
                user.save()

                password_changed = True

            else:
                return redirect(
                    reverse(
                        'hub:error',
                        kwargs={
                            'error_title': 'wrong_current_password'
                        }
                    )
                )

        else:
            error_data = {
                'error_message_alter': change_password_form.errors.as_ul()
            }
            return render(request, 'hub/error.html', context=error_data)

    else:
        change_password_form = ChangePasswordForm()

    data['change_password_form'] = change_password_form
    data['password_changed'] = password_changed

    return render(request, 'hub/change_password.html', context=data)

@login_required
def change_profile_pic(request):
    data = dict()

    user = request.user

    profile_pic_changed = False

    if request.method == 'POST':
        change_profile_pic_form = ChangeProfilePicForm(data=request.POST)
        
        if change_profile_pic_form.is_valid():
            profile = getattr(user, 'userprofile', None)
            if profile:
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                profile.save()

                data['current_picture'] = profile.resume_file

            else:
                profile = change_profile_pic_form.save(commit=False)
                profile.user = user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                profile.save()

                data['current_picture'] = profile.picture

            profile_pic_changed = True

        else:
            error_data = {
                'error_message_alter': change_profile_pic_form.errors.as_ul()
            }
            return render(request, 'hub/error.html', context=error_data)

    else:
        profile = getattr(user, 'userprofile', None)
        if profile and profile.picture:
            d = {
                'picture': profile.picture
            }
            change_profile_pic_form = ChangeProfilePicForm(data=d)

            data['current_picture'] = profile.picture

        else:
            change_profile_pic_form = ChangeProfilePicForm()

    data['change_profile_pic_form'] = change_profile_pic_form
    data['profile_pic_changed'] = profile_pic_changed

    return render(request, 'hub/change_profile_pic.html', context=data)

def resume(request, user_profile_id):
    data = dict()

    resume = UserProfile.objects.get(pk=user_profile_id)
    data['resume'] = to_dict(resume)

    comments = Comment.objects.filter(resume=resume).order_by('created_at')
    data['comments'] = comments.reverse()

    data['comment_form'] = CommentForm()

    return render(request, 'hub/resume.html', context=data)

@login_required
def comment(request):
    user = request.user

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            resume_id = request.POST['resume_id']
            resume = UserProfile.objects.get(pk=resume_id)
            comment.resume = resume
            comment.save()
            
            return redirect(
                reverse(
                    'hub:resume',
                    kwargs={
                        'user_profile_id': resume_id
                    }
                )
            )

        else:
            error_data = {
                'error_message_alter': comment_form.errors.as_ul()
            }
            return render(request, 'hub/error.html', context=error_data)

    else:
        return redirect(reverse('hub:index'))

def doc(request):
    data = dict()

    user = request.user

    if not user.is_anonymous:
        profile = getattr(request.user, 'userprofile', None)
        if profile:
            if profile.is_special:
                return render(request, 'hub/doc.html', context=data)

            else:
                return redirect(
                    reverse(
                        'hub:error',
                        kwargs={
                            'error_title': 'restricted_section'
                        }
                    )
                )

        else:
            return redirect(
                reverse(
                    'hub:error',
                    kwargs={
                        'error_title': 'restricted_section'
                    }
                )
            )

    else:
        return redirect(
            reverse(
                'hub:error',
                kwargs={
                    'error_title': 'restricted_section'
                }
            )
        )

def about(request):
    data = dict()

    return render(request, 'hub/about.html', context=data)

def error(request, error_title):
    data = dict()

    data['error_message'] = ERRORS.get(error_title)

    return render(request, 'hub/error.html', context=data)


def summary(post_body):
    return re.search(r'^.{0,200}[\s]', post_body).group()

def to_dict(resume):
    return {
        'id': resume.id,
        'fullname': resume.user.get_full_name(),
        'picture': resume.picture,
        'resume_file': resume.resume_file,
        'summary': summary(resume.description + ' '),
        'description': resume.description,
    }
