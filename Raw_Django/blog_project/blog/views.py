from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.published.all()
    context = {'posts': posts}
    return render(request, 'blog/post/list.html', context=context)

def post_detail(request, id):
    #Using get_object_or_404 is neater than using the try/except method
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context=context)