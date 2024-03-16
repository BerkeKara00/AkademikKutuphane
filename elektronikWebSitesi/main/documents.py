from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products2'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}
    veriID = fields.IntegerField()
    title = fields.TextField()
   
    
    abstract = fields.TextField()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            
        }
    
    
    class Django:
        model = Product