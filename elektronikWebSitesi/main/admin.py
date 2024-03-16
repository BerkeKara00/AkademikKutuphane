# admin.py

from django.contrib import admin
from .models import Product ,PrimaryLanguage ,Section ,Authors ,Anahtar_kelime ,Siralama 



admin.site.register(PrimaryLanguage)



    
admin.site.register(Product)
admin.site.register(Section)
admin.site.register(Authors)
admin.site.register(Anahtar_kelime)
admin.site.register(Siralama)
