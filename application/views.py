from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Blog, AccessRequest
from subscriptions.models import Subscription

def homepage(request):
    blog_list = Blog.objects.filter(approve_status=True)
    
    # Фильтрация по тегам
    tag = request.GET.get('tag')
    if tag:
        blog_list = blog_list.filter(tags__name__icontains=tag)
    
    return render(request, "home.html", {"blog_qset": blog_list})

@login_required
def addblog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        thumbnail = request.POST.get('thumbnail')
        tags_input = request.POST.get('tags')
        is_private = request.POST.get('is_private') == 'on'
        
        if title and desc:
            blog = Blog.objects.create(
                author=request.user.username,
                title=title,
                desc=desc,
                category=category or 'general',
                thumbnail=thumbnail or 'https://via.placeholder.com/400x200',
                approve_status=True,
                is_private=is_private
            )
            # Сохраняем теги
            if tags_input:
                tag_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                for tag in tag_list:
                    blog.tags.add(tag)
            
            messages.success(request, 'Пост создан!')
            return redirect('home')
        else:
            messages.error(request, 'Заполните все поля')
    
    return render(request, 'addblog.html')

def blogcontent(request, title):
    post = get_object_or_404(Blog, title=title, approve_status=True)
    
    # Проверка приватности
    if post.is_private:
        if not request.user.is_authenticated:
            messages.warning(request, 'Этот пост приватный. Войдите, чтобы запросить доступ.')
            return redirect('login')
        
        if request.user.username != post.author:
            access = AccessRequest.objects.filter(post=post, user=request.user, is_approved=True)
            if not access.exists():
                has_request = AccessRequest.objects.filter(post=post, user=request.user).exists()
                return render(request, 'blogcontent.html', {
                    'post': post,
                    'is_private': True,
                    'has_request': has_request,
                    'is_author': False
                })
    
    return render(request, 'blogcontent.html', {
        'post': post,
        'is_private': False,
        'is_author': request.user.username == post.author if request.user.is_authenticated else False
    })

@login_required
def request_access(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    
    if request.user.username == post.author:
        messages.warning(request, 'Вы автор этого поста!')
        return redirect('blogcontent', title=post.title)
    
    access_request, created = AccessRequest.objects.get_or_create(
        post=post,
        user=request.user
    )
    
    if created:
        messages.success(request, 'Запрос на доступ отправлен автору!')
    else:
        messages.info(request, 'Вы уже запрашивали доступ к этому посту.')
    
    return redirect('blogcontent', title=post.title)

@login_required
def approve_access(request, request_id):
    access_request = get_object_or_404(AccessRequest, id=request_id)
    
    if request.user.username != access_request.post.author:
        messages.error(request, 'Вы не автор этого поста!')
        return redirect('home')
    
    access_request.is_approved = True
    access_request.save()
    messages.success(request, f'Доступ одобрен для {access_request.user.username}')
    return redirect('blogcontent', title=access_request.post.title)

@login_required
def my_requests(request):
    requests = AccessRequest.objects.filter(post__author=request.user.username, is_approved=False)
    return render(request, 'my_requests.html', {'requests': requests})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id, author=request.user.username)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.desc = request.POST.get('desc')
        post.category = request.POST.get('category')
        post.thumbnail = request.POST.get('thumbnail')
        post.save()
        messages.success(request, 'Пост обновлен!')
        return redirect('home')
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id, author=request.user.username)
    post.delete()
    messages.success(request, 'Пост удален!')
    return redirect('home')

@login_required
def feed(request):
    subscribed_user_ids = Subscription.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)
    
    subscribed_usernames = User.objects.filter(id__in=subscribed_user_ids).values_list('username', flat=True)
    
    posts = Blog.objects.filter(
        author__in=subscribed_usernames,
        approve_status=True,
        is_private=False
    ).order_by('-created')
    
    return render(request, 'feed.html', {'posts': posts})