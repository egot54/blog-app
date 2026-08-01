from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .models import Subscription

@csrf_protect
@login_required
def toggle_subscription(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user == target_user:
        messages.error(request, 'Нельзя подписаться на самого себя!')
        return redirect('home')
    
    subscription = Subscription.objects.filter(
        follower=request.user,
        following=target_user
    )
    
    if subscription.exists():
        subscription.delete()
        messages.success(request, f'Вы отписались от {target_user.username}')
    else:
        Subscription.objects.create(
            follower=request.user,
            following=target_user
        )
        messages.success(request, f'Вы подписались на {target_user.username}')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))