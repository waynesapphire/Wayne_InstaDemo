from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Insta.models import UserConnection

from .forms import CustomUserCreationForm
from .models import InstaUser, Post, UserConnection, Like, Comment

class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'
    login_url = 'login'
    
    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'
    
    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

class PostCreateView(CreateView):
    model = Post
    template_name = 'make_post.html'
    fields = '__all__'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ('title',)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

class Signup(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class UserDetail(LoginRequiredMixin,DetailView):
    model = InstaUser
    template_name = "user_profile.html"
    login_url = 'login'

class EditProfile(LoginRequiredMixin,UpdateView):
    model = InstaUser
    template_name = "edit_profile.html"
    fields = ('username', 'profile_pic',)
    login_url = 'login'