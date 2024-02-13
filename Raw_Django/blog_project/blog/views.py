from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from .models import Post, Comment
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger)
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count


# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    #Using get_object_or_404 is neater than using the try/except method
    post = get_object_or_404(Post, 
                             slug=post, 
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blog/post/detail.html', context)

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status = Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                  f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
            # ... send email
        else:
            form = EmailPostForm()
        context = {'form': form, 'post': post, 'sent': sent}
        return render(request, 'blog/post/share.html', context)
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post, id=post_id, status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    context = {'comment': comment, 'post': post, 'form': form}
    return render(request, 'blog/post/comment.html', context)