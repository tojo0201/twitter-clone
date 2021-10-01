from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Tweet,Follow
from .forms import TweetForm

# Create your views here.
#ツイートの一覧表示
def top(request):
    follow_list = Follow.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tweet_list = Tweet.objects.filter(Q(user=request.user) | Q(user__in=follow_list))
    tweet_list = tweet_list.order_by('created_time').reverse()[:20]
    return render(request, 'twitter/top.html', {'tweet_list': tweet_list})

#ツイートする画面
def tweet(request):
    form = TweetForm
    return render(request, 'twitter/tweet.html', {'form': form})

#他の人のツイート（自分含む）
def other_user(request, other_user_id):
    other_user = User.objects.get(id=other_user_id)
    tweet_list = Tweet.objects.filter(user=other_user)
    tweet_list = tweet_list.order_by('created_time').reverse()[:20]
    follow = Follow.objects.filter(user=request.user, followed_user=other_user_id).exists()
    return render(request, 'twitter/other_tweet.html', {'other_user': other_user, 'tweet_list': tweet_list, 'follow': follow})

#フォロー機能
def user_followed(request, other_user_id):
    other_user = User.objects.get(id=other_user_id)
    follow, created = Follow.objects.get_or_create(
        user=request.user,
        followed_user=other_user_id
        )
    if created is True:
        follow.save()
    return redirect(request.META.get('HTTP_REFERER'))

#フォロー削除機能
def follow_deleted(request, other_user_id):
    other_user = User.objects.get(id=other_user_id)
    follow = Follow.objects.filter(user=request.user, followed_user=other_user_id)
    follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))

#ツイート処理
class TweetInputView(generic.CreateView):
    def post(self, request, *args, **kwargs):
        form = TweetForm(data=request.POST)
        if form.is_valid():
            tweet_contents = form.save(commit=False)
            user_contents = self.request.user
            tweet_contents.user = user_contents
            tweet_contents.save()
            return redirect('/twitter/top')
        return render(request, 'twitter/tweet.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = TweetForm(request.POST)
        return render(request, 'twitter/tweet.html', {'form': form,})

#全ユーザーリスト
class UserListView(generic.ListView):
    template_name = 'twitter/user_list.html'
    context_object_name = 'all_user_list'

    def get_queryset(self):
        return User.objects.all().order_by('username')
