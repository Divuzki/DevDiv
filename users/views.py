from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    DeleteView,
    View
)
from .forms import ConfirmPasswordForm
from .decorators import confirm_password
from .models import Post, Profile
from django.contrib.auth.models import User
import stripe

stripe.api_key = ""

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


class PostListView(ListView):
    model = Post
    template_name = 'index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserPostListView(ListView):
    model = Post
    template_name = 'users/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image_url', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def save(self):

    #     img = Image.open(request.FILES.get('image'))

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image_url', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def base_layout(request):
	template='base.html'
	return render(request,template)



class ConfirmPasswordView(UpdateView):
    form_class = ConfirmPasswordForm
    template_name = 'confirm_password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()


def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'You have successfully signed up as {user}!')
            return redirect('/login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


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


def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)


class SearchResultsView(ListView):
    model = Post
    template_name = 'search.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | 
            Q(date_posted__icontains=query) | Q(author__icontains=query) | 
            Q(image_url__icontains=query) | Q(category__icontains=query)
        )
        return object_list
