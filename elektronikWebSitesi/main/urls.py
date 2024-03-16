from django.urls import URLPattern, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import product_detail

from django.urls import path
from .views import run_script
from django.contrib import admin
from django.urls import path, include


urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('download',views.search,name='download'),
    path('product-list',views.product_list,name='product-list'),
    
    path('category-list',views.category_list,name='category-list'),
    path('category_product_list/<int:primarylanguage_id>',views.category_product_list,name='category_product_list'),
    
    path('brand-list',views.brand_list,name='brand-list'),
     path('brand_product_list/<int:section_id>',views.brand_product_list,name='brand_product_list'),
    
    
    
    
    
    
    
    
    path('product/<int:id>/', product_detail, name='product_detail'),
    
    path('load-more-data',views.load_more_data,name='load_more_data'),
    
    
    
    path('run-script/', run_script, name='run_script'),
    path('admin/', admin.site.urls),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    
    
    
    
    
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)