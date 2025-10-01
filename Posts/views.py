from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from Users.models import Follower
from .models import Posts, Likes
from .forms import PostForm


User = get_user_model()


def index(request):
    try:
        followed_users = Follower.objects.filter(user=request.user).values_list('follower_for__username', flat=True)
        posts = Posts.objects.filter(author__username__in=followed_users).order_by('-pub_time')
        following_count = Follower.objects.filter(user=request.user).count()
        
        for post in posts:
            post.likes_count = Likes.objects.filter(for_post=post).count()
            if request.user.is_authenticated:
                post.is_liked = Likes.objects.filter(maker=request.user, for_post=post).exists()
            else:
                post.is_liked = False
        
        return render(request, 'index.html', {
            'posts': posts,
            'following_count': following_count
        })
    except:
        return render(request, 'index.html')


@login_required
def show_my_posts(request):
    posts = Posts.objects.filter(author=request.user).order_by('-pub_time')
    
    # Добавляем информацию о лайках для каждого поста
    for post in posts:
        post.likes_count = Likes.objects.filter(for_post=post).count()
    
    return render(request,
                  'posts/my_posts.html',
                  context={'posts': posts})


@login_required
def create(request):
    form = PostForm(request.POST or None,
                    request.FILES)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('Posts:my_posts')
    return render(request, 'posts/create_post.html', context)



class EditPost(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = PostForm
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('Posts:my_posts')


@login_required
def delete(request, id):
    recipe = get_object_or_404(Posts,
                               id=id,
                               author=request.user)
    recipe.delete()
    return redirect('Posts:index')


@require_POST
@login_required
def like(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    like_exists = Likes.objects.filter(maker=request.user, for_post=post).exists()
    
    if like_exists:
        Likes.objects.filter(maker=request.user, for_post=post).delete()
        is_liked = False
    else:
        Likes.objects.create(maker=request.user, for_post=post)
        is_liked = True
    
    # Возвращаем JSON вместо редиректа
    likes_count = Likes.objects.filter(for_post=post).count()
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': likes_count,
        'post_id': post_id
    })


@login_required
def show_liked_posts(request):
    user_likes = Likes.objects.filter(maker=request.user)
    liked_posts = Posts.objects.filter(id__in=user_likes.values_list('for_post_id', flat=True))
    for post in liked_posts:
        likes_count = Likes.objects.filter(for_post=post).count()
    return render(request,
                  'posts/liked_posts.html',
                  {'posts': liked_posts,})