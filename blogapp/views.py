from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from django.contrib.auth.decorators import login_required
	
def home(request):
    blogs = Blog.objects
    return render(request, 'home.html', {'blogs': blogs})

def detail(request, blog_id): 
	details = get_object_or_404(Blog, pk=blog_id)
	return render(request, 'detail.html', {'details':details})

def new(request):
    if request.user.is_authenticated: 
        # 로그인 한 상태라면 new포스트 html로 보내기.
        return render(request, 'new.html')
    else:
        # 회원정보가 존재하지 않는다면, 에러인자와 함께 home 템플릿으로 돌아가기.     
        blogs = Blog.objects
        return render(request, 'home.html', {'blogs': blogs, 'error': 'You have to login to make newpost'})
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.author = request.user
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+str(blog.id)) 

def delete(request, blog_id):
    destroy = get_object_or_404(Blog, pk=blog_id)
    destroy.delete()
    return redirect('home')

def update(request, blog_id):
    updates= get_object_or_404(Blog, pk=blog_id)
    return render(request, 'update.html', {'updates': updates})

def edit(request, blog_id):
    edit = Blog.objects.get(pk=blog_id)
    edit.title = request.POST['title']
    edit.body = request.POST['body']
    edit.pub_date = timezone.datetime.now()
    edit.save()
    return redirect('home')

@login_required
def post_like(request, blog_id):
    post = get_object_or_404(Blog, pk=blog_id)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()
        return redirect('/blog/'+str(post.id))
    return redirect('/blog/'+str(post.id))