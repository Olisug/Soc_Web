from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Friend, Follower

User = get_user_model()


def registration(request):
    '''Регистрация'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None,
                                request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request,
                  'users/registration.html',
                  {'form': form})


class CustomLoginView(LoginView):
    '''Вход в аккаунт'''
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return '/'


class CustomLogoutView(LogoutView):
    '''Выход из аккаунта'''
    template_name = 'users/logout.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return '/'


@login_required
def my_profile(request):
    user = request.user
    if Friend.objects.filter(user=request.user,
                             users_friend=user)|Friend.objects.filter(
                                 user=user,
                                 users_friend=request.user):
        is_friend = False
    else:
        is_friend = True
    if Follower.objects.filter(user=request.user,
                               follower_for=user):
        is_follower = False
    else:
        is_follower = True
    users_friends1 = Friend.objects.filter(user=user,
                                           confirmed=True)
    users_friends2 = Friend.objects.filter(users_friend=user,
                                           confirmed=True)
    user_following = Follower.objects.filter(user=user)
    follower = Follower.objects.filter(user=request.user, follower_for=user)
    context = {'user': user,
               'is_friend': is_friend,
               'friends1': users_friends1,
               'friends2': users_friends2,
               'is_follower': follower,
               'user_following': user_following}
    return render(request, 'users/my_profile.html', context)


def another_profile(request, user_id):
    another_user = get_object_or_404(User, id=user_id)
    try:
        is_subscribed = False
        # Проверяем каждый статус отдельно с обработкой исключений
        is_friend = Friend.objects.filter((Q(user=request.user, users_friend=another_user)|Q(user=another_user, users_friend=request.user)),confirmed=True).exists()
        friend_request_sent = False
        friend_request_received = False
        if not is_friend:
            friend_request_sent = Friend.objects.filter(user=request.user, users_friend=another_user, confirmed=False).exists()
            friend_request_received = Friend.objects.filter(user=another_user, users_friend=request.user, confirmed=False).exists()
        if not Follower.objects.filter(user=request.user, follower_for=another_user).exists():
            is_subscribed = False
        else:
            is_subscribed = True
        return render(request,
                    'users/another_profile.html',
                    {'another_user': another_user,
                    'is_friend': is_friend,
                    'friend_request_sent': friend_request_sent,
                    'friend_request_received': friend_request_received,
                    'is_subscribed': is_subscribed})
    except:
        return render(request,
                    'users/another_profile.html',
                    {'another_user': another_user})


def search_users(request):
    try:
        query = request.GET.get('q', '').strip()
        if query:
            object_list = User.objects.filter(Q(username__icontains=query))
        else:
            object_list = User.objects.none()
    except Exception as e:
        # Логируем ошибку на случай проблем с базой данных
        print(f"Search error: {e}")
        object_list = User.objects.none()
        query = ''
    return render(request,
                  'users/find_users.html',
                  {'object_list': object_list,
                   'search_query': query})


@login_required
def send_request(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        is_friend = Friend.objects.filter(user=request.user, users_friend=user)|Friend.objects.filter(user=user, users_friend=request.user)
        if not is_friend:
            add_friend = Friend(user=request.user, users_friend=user)
            add_friend.save()
    except:
        raise Http404("Пользователь не найден!")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def confirm_friend(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")
    new_friend = Friend.objects.get(user=user,
                                    users_friend=request.user)
    new_friend.confirmed = True
    new_friend.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_friend(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")
    del_friend = Friend.objects.filter(user=user,
                                       users_friend=request.user)|Friend.objects.filter(user=request.user, users_friend=user)
    del_friend.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def subscribe(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")
    is_follower = Follower.objects.filter(user=request.user, follower_for=user)
    if not is_follower:
        add_follower = Follower(user=request.user,
                                follower_for=user)
        add_follower.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def cancel_subscribe(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")
    follower = Follower.objects.filter(user=request.user, follower_for=user)
    follower.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def show_my_friends(request):
    user = request.user
    users_friends1 = Friend.objects.filter(user=user,
                                           confirmed=True)
    users_friends2 = Friend.objects.filter(users_friend=user,
                                           confirmed=True)
    total_number = users_friends1.count() + users_friends2.count()
    context = {'friends1': users_friends1,
               'friends2': users_friends2,
               'total_number': total_number}
    return render(request, 'users/my_friends.html', context)


@login_required
def show_my_subscribes(request):
    subscribes = Follower.objects.filter(user=request.user)
    subscribes_count = subscribes.count()
    context = {'subscribes': subscribes,
               'subscribes_count': subscribes_count}
    return render(request,
                  'users/my_subscribes.html',
                  context)


@login_required
def show_my_subscribers(request):
    subscribes = Follower.objects.filter(follower_for=request.user)
    return render(request,
                  'users/my_subscribers.html',
                  {'subscribes': subscribes})


@login_required
def show_my_dialogs(request):
    return (request, 'users/my_dialogs.html')


@login_required
def show_my_apps(request):
    return (request, 'users/my_apps.html')
