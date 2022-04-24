from collections import Counter
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
import numpy as np
from users.models import Post



# var
now = datetime.now().strftime("%Y-%m-%d %H:%M")
today = datetime.today()
long_ago = today + timedelta(days=7)

def trending(request):

    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    breaking = today + timedelta(days=3)

    top_week = Post.objects.filter(date_posted__gte=last_week).annotate(
        likes_count=Counter('likes')).order_by('-timestamp')[:5]
    trending = Post.objects.filter(date_posted__gte=breaking).annotate(
        likes_count=Counter('likes')).order_by('-timestamp')[:5]


def trendingpostfunction():
    rdata = Post.objects.filter(date_posted__gte=long_ago)
    likerate = []
    dislikerate = []
    viewrate = []
    for i in rdata:
        lr = i.likes.count() + 1
        vr = i.views + 1
        lr = lr / vr
        likerate.append(lr)
        dr = i.dislikes.count() + 1
        dr = dr / vr
        dislikerate.append(dr)
        u = User.objects.count()
        vrt = vr / u
        viewrate.append(vrt)
    lr1 = np.array(likerate)
    dr1 = np.array(dislikerate)
    vr1 = np.array(viewrate)
    lr = lr1.round(2)
    dr = dr1.round(2)
    vr = vr1.round(2)
    # results = []
    for i in lr, dr, vr:
        a = (lr - dr) + vr
        a = a * 50
    rdata = Post.objects.filter(date_posted__gte=long_ago)
    trendingdata = a
    j = 0
    trendingdict = {}
    for i in rdata:
        trendingdict[i.id] = trendingdata[j]
        j += 1
    trend = {k: v for k, v in sorted(
        trendingdict.items(), key=lambda item: item[1], reverse=True)}
    print('latest trending --', trend)
    trendlist = []
    for k in trend.keys():
        trendlist.append(k)
    #print('trendlist --', trendlist)
    return trendlist

def test(request):
    posts = trendingpostfunction()
    return render(request, 'test.html', {"posts":posts})