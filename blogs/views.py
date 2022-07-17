from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



#Dummy Date
# posts=[{
#         'author' : 'User1',
#         'title'  : 'titile1',
#         'content' : 'content of first post',
#         'date_posted' : 'Jan 2022'
#     },
#     {
#         'author' : 'User2',
#         'title'  : 'titile2',
#         'content' : 'content of Second post',
#         'date_posted' : 'Feb 2022'
#     }
# ]

# Create your views here.
def home(request):
    context = {
        'posts' : Post.objects.all(),
        'title' : 'awesome'
    }
    return render(request, 'blogs/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blogs/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = '5'

class UserPostListView(ListView):
    model = Post
    template_name = 'blogs/user_posts.html'
    context_object_name = 'posts'
    # ordering = '-date_posted'
    paginate_by = '5'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(user)
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)  

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)  
    #test_func will run by userpassestextmixin to chk if user is deleting updating only his post not others
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url="/"
    #test_func will run by userpassestextmixin to chk if author is deleting updating only his post not others
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
    


def about(request):
    return render(request, 'blogs/about.html')
