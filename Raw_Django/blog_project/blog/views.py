from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3) 
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
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