from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm, CommentForm, UserProfileForm
from .models import Category, Post, Comment


N_PER_PAGE = 10


def get_published_posts():
    """Возвращает посты, отфильтрованные по условиям публикации."""
    now = timezone.now()
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
    )


def paginate(request, queryset):
    paginator = Paginator(queryset, N_PER_PAGE)
    return paginator.get_page(request.GET.get('page'))


def index(request):
    """Главная страница со всеми постами."""
    page_obj = paginate(request, get_published_posts().order_by('-pub_date'))

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def profile(request, username):
    """Страница пользователя с его публикациями."""
    user = get_object_or_404(get_user_model(), username=username)
    if request.user == user:
        post_qs = Post.objects.filter(author=user).order_by('-pub_date')
    else:
        post_qs = get_published_posts().filter(author=user).order_by('-pub_date')

    context = {
        'profile': user,
        'page_obj': paginate(request, post_qs),
    }
    return render(request, 'blog/profile.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_qs = get_published_posts().filter(category=category).order_by('-pub_date')
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': paginate(request, post_qs),
    })


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'blog/user.html', {'form': form})


def post_detail(request, id):
    """Страница отдельного поста."""
    post = get_object_or_404(Post, pk=id)

    can_view = (
        (post.is_published and post.pub_date <= timezone.now() and post.category and post.category.is_published)
        or (request.user.is_authenticated and request.user == post.author)
    )
    if not can_view:
        raise Http404

    comments = post.comments.order_by('created_at')
    form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        username = post.author.username
        post.delete()
        return redirect('blog:profile', username=username)

    form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method != 'POST':
        return redirect('blog:post_detail', id=post.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('blog:post_detail', id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'blog/comment.html',
        {
            'form': form,
            'comment': comment,
        },
    )


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post.id)

    return render(
        request,
        'blog/comment.html',
        {
            'comment': comment,
        },
    )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': form})

