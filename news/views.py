from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from .models import Article, Category, Comment
from .forms import UserRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


def home(request):
    # Берем все статьи и сортируем: новые сверху
    articles = Article.objects.all().order_by('-created_at') 
    
    # ВАЖНО: имя в кавычках 'articles' должно быть таким же, как в home.html
    return render(request, 'news/home.html', {'articles': articles})

# 2. СТРАНИЦА КАТЕГОРИИ
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all()
    return render(request, 'news/category.html', {'category': category, 'articles': articles})

# 3. ДЕТАЛЬНАЯ СТРАНИЦА НОВОСТИ + КОММЕНТАРИИ
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # Если юзер отправил комментарий
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'news/article.html', {
        'article': article, 
        'form': form
    })

# 4. ЛАЙКИ
def like_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    post = get_object_or_404(Article, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('article', args=[str(pk)]))

# 5. РЕГИСТРАЦИЯ
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Сразу логиним после регистрации
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'news/profile.html', {'u_form': u_form, 'p_form': p_form})