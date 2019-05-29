from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
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

# def category(request, post_item_type):
#     category = Post.objects.all().select_related(post_item_type)
#     return render(request, 'blog/category.html', {'category': category} )

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
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('detail', post.pk)
    else:
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'post': post, 'form': form})

""" 
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


    def edit(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('detail', post.pk)
    else:
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'post': post, 'form': form}) """

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

def search(request):
    options = ['경영관', '공학원', '공A', '공B', '공C','과학관', '과학원', '광복관','교육과학관','대강당', '대우관', '무악1학사', '무악2학사', '무악3학사', '무악4학사', '미우관', '백양관', '백양누리', '백주년기념관', '빌링슬리관', '삼성관', '상남경영원', '성암관', '스팀슨관', '스포츠과학관', '신학관', '아펜젤러관', '알렌관', '언더우드관', '연희관', '외솔관', '우정원', '운동선수기숙사','위당관', '음악관', '중앙도서관', '청송대', '체육관', '학생회관', '학술정보원', '한경관']
    return render(request,'blog/search.html', {'options':options})

def result(request):
    if request.method =="GET":
        keyword1 = request.GET.get('keyword1')
        keyword2 = request.GET.get('keyword2')
        if ((keyword1 is not None) and (keyword2 is not None)):
            posts = Post.objects.filter(Q(item_type__icontains=keyword1) & Q(kept_place__icontains=keyword2))
            paginator = Paginator(posts, 3)
            page = request.GET.get('page')
            post_page = paginator.get_page(page)
            return render(request, 'blog/searchhome.html', {'posts': posts, 'post_page': post_page, 'keyword1':keyword1, 'keyword2':keyword2}) 
        else:
            return render(request,'blog/search.html')
    else:
        return render(request,'blog/search.html')