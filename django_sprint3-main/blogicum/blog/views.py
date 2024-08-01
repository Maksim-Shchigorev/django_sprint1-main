from django.shortcuts import render
from blog.models import Post, Category
from django.utils import timezone
from django.http import Http404


def index(request):
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-created_at')[:5]

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if not post.is_published or post.pub_date > timezone.now():
            raise Http404("Post not found")
        if not post.category.is_published:
            raise Http404("Post not found")
    except Post.DoesNotExist:
        raise Http404("Post not found")
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        if not category.is_published:
            raise Http404("Category not found")
        post_list = Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now()
            # published_at__lte=timezone.now()
        ).order_by('-created_at')
    except Category.DoesNotExist:
        raise Http404("Category not found")
    return render(request, 'blog/category.html', {'post_list': post_list,
                                                  'category': category})
