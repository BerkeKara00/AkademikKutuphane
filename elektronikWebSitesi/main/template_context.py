from .models import Product


def get_filters(request):
    
    languages = Product.objects.distinct().values('primarylanguage__title','primarylanguage__id')
    # sections = Product.objects.distinct().values('section__title','section__id')
    
    data={
        'languages':languages,
        
        
    }
    return data