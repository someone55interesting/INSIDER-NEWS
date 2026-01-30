from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from .models import Article, Category, Comment
from .forms import UserRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.db.models import Q

def home(request):
    query = request.GET.get('q') # Получаем текст поиска
    categories = Category.objects.all() # Для бокового меню
    
    if query:
        # Если ищем, то фильтруем всё подряд
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__icontains=query)
        ).distinct().order_by('-created_at')
        hot_articles = None # При поиске "горячее" не выделяем
    else:
        # Если просто главная:
        hot_articles = Article.objects.filter(is_hot=True).order_by('-created_at')[:3]
        articles = Article.objects.filter(is_hot=False).order_by('-created_at')

    context = {
        'articles': articles,
        'hot_articles': hot_articles,
        'categories': categories, # Теперь категории доступны в шаблоне
    }
    return render(request, 'news/home.html', context)

# 2. СТРАНИЦА КАТЕГОРИИ
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all()
    return render(request, 'news/category.html', {'category': category, 'articles': articles})

# 3. ДЕТАЛЬНАЯ СТРАНИЦА НОВОСТИ + КОММЕНТАРИИ
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('-created_at') # Берем все комменты к посту
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article', pk=pk) # Перезагрузка, чтобы коммент появился
    else:
        form = CommentForm()

    return render(request, 'news/article.html', {
        'article': article, 
        'comments': comments, # Передаем комменты в шаблон
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