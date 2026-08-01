from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from application.models import Blog
from .forms import CommentForm

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
    return redirect('blogcontent', title=post.title)