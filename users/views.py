from django.template.loader import get_template
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import CreateUserForm, ProfileUpdateForm, ConfirmPasswordForm, FlagForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView
)
from django.http import JsonResponse, HttpResponse
from .models import Post, Comment, HashTag
from posts.models import PostFlag
from django.contrib.auth.models import User
from history.mixins import ObjectViewMixin
from django.core.mail import mail_admins
import stripe
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from .decorators import confirm_password
from django.utils.decorators import method_decorator

# HashTag View


def hashtag_view(request, tags):
    tags = '#'+tags  # adding hashtag symbol '#' to query

    # getting all the hashtags in django
    hashtag_posts = Post.objects.filter(hashtag=tags)
    hashtag_count = hashtag_posts.count()

    # Getting the first user to use the hashtag
    hashtag_user = HashTag.objects.filter(name=tags).first().user
    # double checking if the user is in my post user
    hashtag_user = Post.objects.filter(author=hashtag_user).first().author

    # Checking if the hashtag_count is in thousands or millions
    if hashtag_count >= 1000:
        hashtag_count = str(f"{hashtag_posts.count()}")
        if not hashtag_count[1] == "0":
            hashtag_count = f"{hashtag_count[0]}.{hashtag_count[1]}k"
        else:
            hashtag_count = f"{hashtag_count[0]}k"
    elif hashtag_count >= 1000000:
        hashtag_count = str(f"{hashtag_posts.count()}")
        if len(hashtag_count) >= 2:
            hashtag_count = f"{hashtag_count[0]+hashtag_count[1]}M"
        else:
            hashtag_count = f"{hashtag_count[0]}M"

    return render(request, 'hashtags.html', {
        'tags': tags,
        'first_user': hashtag_user,
        'posts': hashtag_posts,
        'total_tags': hashtag_count,  # getting how many tags that match the 'tags' query
    })


def category_view(request, cats):
    category_posts = Post.objects.filter(
        category=cats).order_by('-date_posted')
    print(category_posts)
    first_tag = Post.objects.filter(category=cats)
    if first_tag.exists():
        print(first_tag)
    first_tag = HashTag.objects.filter(name=first_tag)
    return render(request, 'categories.html', {
        'cats': cats,
        'posts': category_posts,
        'first_tag': first_tag,
    })


def donate(request):
    return render(request, 'users/donate.html')


def donate_charge(request):
    amount = 5
    if request.method == 'POST':
        print('Data:', request.POST)

        stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname']
        )

    return redirect(reverse('donate_success', args=[amount]))


def donate_successMsg(request, args):
    amount = args
    return render(request, 'users/donated-success.html', {'amount': amount})


@login_required  # checking if the user is logged in
@require_POST  # indicating dat POST request is required
def comment_create_view(request, pk):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, id=pk)
        body = request.POST['body']

        qs = Comment.objects.create(
            user=user,
            post=post(),
            name=request.user,
            body=body,
        )
        qs.save()
        print(qs)
        qs = Comment.objects.filter(id=qs.id).all()
        ctx = {
            "id": qs.id,
            "user": qs.user.username,
            "img": qs.user.profile.image_url,
            "body": qs.body,
            "likes": qs.likes.count(),
            "date": qs.date_added,
        }  # add it to an object
        # use mimetype instead of content_type if django < 5
        # convert it to json data
        return JsonResponse(ctx, safe=False, content_type='application/json')


def comment_list_view(request, post):
    if request.method == 'GET':
        qs = Comment.objects.filter(post=post).all().order_by('-date_added')
        qs = [x.serialize() for x in qs]
        # use mimetype instead of content_type if django < 5
        # convert it to json data
        return JsonResponse(qs, safe=False, content_type='application/json')


@login_required  # checking if the user is logged in
@require_POST  # indicating dat POST request is required
def LikeView(request, pk, *args, **kwargs):
    try:
        if request.method == 'POST':  # double checking if it a POST request
            user = request.user  # requesting for user
            # getting post_id from like btn
            post_id = request.POST.get('post_id', None)
            # getting the Post Model from models.py an still checking for 404 error
            post = get_object_or_404(Post, id=post_id)

            # if user click on like btn and it does not exists in db
            if not post.likes.filter(id=user.id).exists():
                post.dislikes.remove(user)  # remove dislike from db
                post.likes.add(user)  # add like to db
                message = 'You liked this'
            # if user click on like btn again then
            elif not post.dislikes.filter(id=user.id).exists():
                # remove like & dislike
                post.dislikes.remove(user)
                post.likes.remove(user)
                message = 'Like has been removed'  # Msg of confirmation

        ctx = {
            'likes_count': post.total_likes(),  # total count of likes
            'dislikes_count': post.total_dislikes(),  # total count of dislikes
            'message': message,
        }  # add it to an object
        # use mimetype instead of content_type if django < 5
        # convert it to json data
        return JsonResponse(ctx, content_type='application/json')
    except:
        ctx = {
            'error': "There is an error, try again later",
        }  # add it to an object
        # convert it to json data
        return JsonResponse(ctx, content_type='application/json')


@login_required
@require_POST
def DislikeView(request, pk, *args, **kwargs):
    try:
        if request.method == 'POST':
            user = request.user
            post_id = request.POST.get('post_id', None)
            post = get_object_or_404(Post, id=post_id)

            # if user click on dislike btn and it does not exists in db
            if not post.dislikes.filter(id=user.id).exists():
                # add a new like for a post
                post.likes.remove(user)  # remove like to db
                post.dislikes.add(user)  # add dislike from db
                message = 'You disliked this post'
            # if user click on dislike btn again then
            elif not post.likes.filter(id=user.id).exists():
                # remove dislike
                post.dislikes.remove(user)
                message = 'Dislike has been removed'

        ctx = {
            'likes_count': post.total_likes(),  # total count of likes
            'dislikes_count': post.total_dislikes(),  # total count of likes
            'message': message,  # success msg
        }  # add it to an object
        # use mimetype instead of content_type if django < 5
        # convert it to json data
        return JsonResponse(ctx, content_type='application/json')
    except:
        ctx = {
            'error': "There is an error, try again later",
        }  # add it to an object
        # convert it to json data
        return JsonResponse(ctx, content_type='application/json')


# Autocompleting hashtag
@csrf_exempt
def hashtag_autocomplete(request, *args, **kwargs):
    # Looking for data that
    if 'term' in request.GET:
        qs = HashTag.objects.filter(name__istartswith=request.GET.get(
            'term'))  # stat with the 'term' in the GET request
        names = []
        names = list(dict.fromkeys(names))
        for name in qs:
            names.append(name.name)


        names = list(dict.fromkeys(names))
        return JsonResponse(names, safe=False)

    # if the user type it will automatically save to db for vase dict
    if request.method == 'POST':
        user = request.user
        hashtag = request.POST['name']
        post = request.POST['post']
        hashtag = hashtag.split(",")
        hashtag.sort()
        for hashtags in hashtag:
                if hashtags[0] == "#":  # Checking if the hashtag text contains the '#' symbol at the begin
                    # checking if the hashtag exists to avoid double hashtag in db
                    if not HashTag.objects.filter(name__iexact=hashtags).exists():
                        # returning it as json data for js to proccess
                        HashTag.objects.create(
                            user=user,
                            post=post,
                            name=hashtags
                        ) # Add it to db
                        ctx = {
                            "data":
                                {
                                "tag":hashtag,
                                "post": post
                                }
                        }
                        return JsonResponse(ctx, safe=False)
                        # then return as json data
                elif not hashtags[0] == "#": # else error
                    return JsonResponse({"data": {"error": f"This is a hashtag, You need to add the symbol '#' in {hashtags}"}}, safe=False)
        return JsonResponse(hashtag, safe=False)


# listing out all the post in desc order for home page
class PostListView(ListView):
    model = Post  # Getting Model from models.py
    template_name = 'index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # the context name
    ordering = ['-date_posted']  # start post in desc order
    paginate_by = 9  # dividing the page into 9 posts per page

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Creating a new Post
@method_decorator(confirm_password, name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # Getting Post Model in models.py
    fields = ['title', 'description', 'upload_image', 'image_url', 'image_caption', 'video_url',
              'hashtag', 'content', 'category']  # fields in the Form
    # Validating the form

    def form_valid(self, form):
        # checking if the author is equals to the logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        qs = Post.objects.filter(title__iexact=post.title)
        if qs.exists():
            raise serializers.ValidationError("The title must be unique")
            return False
        else:
            return True


# Showing a single post with it contents in a page -> Post Details
class PostDetailView(ObjectViewMixin, DetailView):
    model = Post  # Getting Post Model in models.py

    def get_context_data(self, *args, **kwargs):
        cat_menu = Post.objects.all()
        context = super(PostDetailView, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_dislikes = stuff.total_dislikes()
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes  # total likes
        context["total_dislikes"] = total_dislikes  # total dislikes
        return context


# Updating Post Using pk to Confirm
@method_decorator(confirm_password, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'hashtag', 'image_url',
              'video_url', 'content']  # fields in the Form
    # Validating the form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # test if it is actually the owner of the post updating it

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Deleting Post
@method_decorator(confirm_password, name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # Url to redirect afther you delete a post

    # checking if it is the author of the post deleting it
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Showing all the post of a particular author
class UserPostListView(ListView):
    model = Post
    template_name = 'users/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6  # dividing the page into 6 post per page

    # Getting qs of all the post by the username -> author
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Confirming Password
class ConfirmPasswordView(UpdateView):
    form_class = ConfirmPasswordForm
    template_name = 'confirm_password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path() # Getting the full url


# Creating a new user
def signup(request):
    form = CreateUserForm()  # Django User Creation Form

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request, f'You have successfully signed up as {user}!')
            return redirect('/login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# Logging user into website
def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


# Search View
def search_result_view(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(author__username__icontains=query) |
        Q(description__icontains=query) |
        Q(image_caption__icontains=query) |
        Q(content__icontains=query) |
        Q(hashtag__icontains=query)
    ).order_by('-date_posted')
    # pages = pagination(request, result, num=1)

    context = {
        'items': results,
        'result_num': results.count(),
    }
    return render(request, "search.html", context)


# PWA
def devdiv_serviceworker(request, js):
    template = get_template('sw.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")


def profile(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        post_qs = Post.objects.filter(author=user)
        context = {
            'post_qs': post_qs
        }
        return render(request, 'accounts/profile.html', context)
    else:
        return redirect("/login")


# Profile Update View
@confirm_password
def profile_update_view(request, *args, **kwargs):
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    my_profile = user.profile
    form = ProfileUpdateForm(request.POST or None,
                             instance=my_profile, initial=user_data)

    if request.method == "POST":
        if form.is_valid():
            profile_qs = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            image = form.cleaned_data.get('image_url')
            status = form.cleaned_data.get('status')
            facebook = form.cleaned_data.get('facebook_link')
            twitter = form.cleaned_data.get('twitter_link')
            instagram = form.cleaned_data.get('status')
            location = form.cleaned_data.get('location')
            about_me = form.cleaned_data.get('about_me')

            # Saving Data From Form To Database
            user.username = username
            profile_qs.image_url = image
            profile_qs.status = status
            profile_qs.facebook_link = facebook
            profile_qs.twitter_link = twitter
            profile_qs.instagram_link = instagram
            profile_qs.location = location
            profile_qs.about_me = about_me
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            profile_qs.save()
            messages.success(
                request, f'Profile Updated')
            return redirect('/profile')

    context = {'form': form}
    return render(request, 'accounts/profile_update.html', context)


def post_flag_view(request, pk, *args, **kwargs):
    qs = Post.objects.filter(pk=pk)
    if not qs.exists():
        raise Http404
    else:
        qs = qs.first()
        qss = str(qs.id)
        context = {
            "post": qs,
            "form": FlagForm,
            "post_uuid": "DEVDIV0"+qss+"016",
        }
        return render(request, "users/post-flag.html", context)


# Flagging Post And Sending to admins
@confirm_password
def post_flagging_view(request, postuuid, *args, **kwargs):
    post_id = request.POST.get('post_id')
    category = request.POST.get('category')
    other = request.POST.get('other')
    try:
        pqs = Post.objects.filter(pk=post_id)
        pqs = pqs.first()
        PostFlag.objects.create(
            user=request.user,
            post=pqs,
            postUUID=postuuid,
            category=category
        )
        qs = PostFlag.objects.filter(postUUID=postuuid)
        qs = qs.first()
        mail_admins(
            "Flag Alert",
            "User :" + qs.user + " Has Flagged " + qs.post__author +
            " Post. And The Total Flags On This Post Is " + qs.count() + "",
            fail_silently=False,
            html_message="<h3 style='color:red'>This Flag Was Categorized under " +
            category+"</h3><br />Other:<br /><p>"+other+"</p>"
        )
        return render(request, "users/post-flag.html")
    except:
        messages.error(request, 'There was an error, try again later')
        return redirect('/profile')
# replace('-', '')
