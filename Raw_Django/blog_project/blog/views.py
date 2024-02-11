from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger)
from django.views.generic import ListView


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3) 
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts}
    return render(request, 'blog/post/list.html', context=context)

def post_detail(request, year, month, day, post):
    #Using get_object_or_404 is neater than using the try/except method
    post = get_object_or_404(Post, 
                             slug=post, 
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context=context)

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'