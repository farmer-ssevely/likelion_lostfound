from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-updated_at')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    post_page = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts, 'post_page': post_page})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})

def category(request, post_item_type):
    category = Post.objects.all().select_related(post_item_type)
    return render(request, 'blog/category.html', {'category': category} )

""" def new(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.found_date = request.POST.get('found_date')
        post.found_place = request.POST.get('found_place')
        post.kept_place = request.POST.get('kept_place')
        post.item_type = request.POST.get('item_type')
        post.image = request.FILES['image']
        post.author = request.user
        post.save()
        return redirect('detail', post.pk)
    else:
        return render(request, 'blog/new.html') """

def new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) # commit은 데이터베이스의 모든 작업이 저장되었을 때 True가 되는데, 그러면 comment를 더이상 수정하지 못 하게 됨, 우선 commit = False를 해서 뒤에 작업들을 할 수 있게 해줌
            post.author = request.user
            post.save()  # 여기는 default가 commit = True라서 따로 설정 안 해줌
            return redirect('detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new.html')

def edit(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detail', post.pk)
    else:
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'post': post, 'form': form})

def remove(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, 'Post Successfully removed')
    return redirect('posthome')

def newcomment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('detail', post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/newcomment.html', {'form': form})

def removecomment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('detail', post_id = comment.post.pk)