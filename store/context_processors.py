from store.models import Category

def categories_nav(request):
    return {'categories_nav': Category.objects.all()[:10]}