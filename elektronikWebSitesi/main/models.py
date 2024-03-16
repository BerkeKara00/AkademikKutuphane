from email.policy import default
from unicodedata import category
from django.db import models
from django.utils.html import mark_safe
import django

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry








class PrimaryLanguage(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural='Languages'
    
    def __str__(self):
        return self.title 

class Section(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title       
    
class Authors(models.Model):
    title = models.CharField(max_length=300)
    
    def __str__(self):
        return self.title   
    

class Anahtar_kelime(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title
      

class Siralama(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Product(models.Model):
    veriID = models.IntegerField()
    title = models.CharField(max_length=500)
   
    authors = models.ManyToManyField(Authors)
    
    abstract = models.CharField(max_length=20000)  # Değişiklik: Uzun metin için TextField kullanıldı.
    
    
    anahtar_kelime = models.ManyToManyField(Anahtar_kelime)
    
    
    search_keyword = models.CharField(max_length=300,null=True)
    doi_number = models.CharField(max_length=300)
    url = models.URLField(max_length=500)  # Değişiklik: URLField kullanıldı.
    primarylanguage = models.ForeignKey(PrimaryLanguage, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    publication_date = models.DateField()  # Değişiklik: Tarih bilgisi için DateField kullanıldı.
    
    siralama = models.ForeignKey(Siralama, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            
        }
    
    def __str__(self):
        return self.title
    
    
    
    
    
  
    
