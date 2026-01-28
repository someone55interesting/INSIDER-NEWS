from .models import Category

def categories(request):
    return {'categories_menu': Category.objects.all()}