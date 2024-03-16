from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product, PrimaryLanguage, Section, Authors, Anahtar_kelime, Siralama
from django.template.loader import render_to_string
from django.db.models import Max,Min

from django.shortcuts import render
from django.http import HttpResponse

import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

from django import forms


from django.shortcuts import render, redirect


from django.http import HttpResponse


from datetime import datetime
import locale
import ast

from elasticsearch_dsl import Search
from .documents import ProductDocument

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class SearchForm(forms.Form):
    q = forms.CharField(label='Anahtar Kelimeleri Girin', max_length=100)

# ana sayyfa
def home(request):
    data = Product.objects.all().order_by('-veriID')[:8]
    return render(request, 'index.html', {'data': data})


#kategoriler
def category_list(request):
    data = PrimaryLanguage.objects.all().order_by('-veriID')
    return render(request,'category_list.html' ,{'data':data})

def category_product_list(request,language_id):
    primarylanguage=PrimaryLanguage.objects.get(id=language_id)
    data=Product.objects.filter(primarylanguage=primarylanguage).order_by('-veriID')
    
    
    
    return render(request,'category_product_list.html' ,{'data':data,})


def brand_list(request):
    data = Section.objects.all().order_by('-veriID')
    return render(request,'brand_list.html' ,{'data':data})





def brand_product_list(request,section_id):
    section=Section.objects.get(id=section_id)
    data=Product.objects.filter(section=section).order_by('-veriID')

    return render(request,'category_product_list.html' ,{'data':data,}) 





def clean_keywords(keywords1):
    try:
        
        keywords_list = ast.literal_eval(keywords1)
        
        
        cleaned_list = [word.strip(" ',") for word in keywords_list]
        
        
        cleaned_string = ', '.join(cleaned_list)
        
        return cleaned_string
    except (SyntaxError, ValueError):
        
        return keywords1















#ürünler
def product_list(request):
    langs = PrimaryLanguage.objects.all()
    total_data=Product.objects.count()
    data = Product.objects.all().order_by('-veriID')
    
    section_ids = []
    authors_ids = []
    anahtar_kelime_ids = []
    siralama_ids = []
    
    
    
    
    for id in data.values("section__id"):
        section_ids.append(id["section__id"])
        
    section_ids = set(section_ids)
    
    sections = Section.objects.filter(id__in=section_ids).all()
    
    
    
    
    
    
    for id in data.values("authors__id"):
        authors_ids.append(id["authors__id"])
        
    authors_ids = set(authors_ids)
    
    authorss = Authors.objects.filter(id__in=authors_ids).all()
    
    
    
    
        
    
    for id in data.values("anahtar_kelime__id"):
        anahtar_kelime_ids.append(id["anahtar_kelime__id"])
        
    anahtar_kelime_ids = set(anahtar_kelime_ids)
    
    anahtar_kelimes = Anahtar_kelime.objects.filter(id__in=anahtar_kelime_ids).all()
    
    
    
    
    
    for id in data.values("siralama__id"):
        siralama_ids.append(id["siralama__id"])
        
    siralama_ids = set(siralama_ids)
    
    siralamas = Siralama.objects.all()
    
    
    
    return render(request,'product_list.html' ,{  
                                                'data':data, 
                                                'total_data':total_data,
                                                'langs':langs,
                                                'sections':sections,
                                                'authorss':authorss,
                                                'siralamas':siralamas,
                                                'anahtar_kelimes':anahtar_kelimes
                                                } 
                  )
    
    #ürün listeleme
    
    

                                                        
                                                        
                                                    
    
    
    

    
    
#ürün sayfası


def product_detail(request,id):
    product=Product.objects.get(id=id)
    print(product.primarylanguage)
    return render(request, 'product_detail.html',{'data':product})    




# arama
from django.shortcuts import render
from elasticsearch_dsl import Search
from elasticsearch.exceptions import NotFoundError
from elasticsearch import Elasticsearch
def search(request): 
    q = request.GET.get('q', '')

    # Elasticsearch'de arama yap
    search = Search(index='products2')
    search = search.query("multi_match", query=q, fields=['title','abstract'])

    try:
        # Elde edilen sonuçları al
        response = search.execute()
        hits = response.hits

        # Elasticsearch'ten dönen belgeleri bir liste olarak al
        data = [hit.to_dict() for hit in hits]
    except NotFoundError:
        # Elasticsearch'te index bulunamazsa boş bir liste oluştur
        data = []

    # search.html şablonuna verileri gönder
    return render(request, 'search.html', {'data': data, 'query': q})



#indirme
 







def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    langTrValue = int(request.GET['langTrValue'])
    langEnValue = int(request.GET['langEnValue'])

    if (langTrValue == 0) and (langEnValue == 0):
        
    # Queryset'i oluşturun, ancak sonucu almadan önce koşulları kontrol edin
        queryset = Product.objects.filter(primarylanguage__id=langTrValue).order_by('-veriID')[offset:offset+limit]
        data = list(queryset) if queryset else []
    # Koşullara uygun bir sonuç elde edilmediyse, queryset'i boş bir liste olarak ayarlayın
        


    if (langTrValue != 0) & (langEnValue == 0):
        print("LangTr value 1")
        data = Product.objects.all().filter(primarylanguage__id=langTrValue).order_by('-veriID')[offset:offset+limit]
    
    if (langTrValue == 0) & (langEnValue != 0):
        print("LangEn Value 1")
        data = Product.objects.all().filter(primarylanguage__id=langEnValue).order_by('-veriID')[offset:offset+limit]
        
    if (langTrValue != 0) & (langEnValue != 0):
        print("both is done")
        data = Product.objects.all().order_by('-veriID')[offset:offset+limit]

        
        
    print(request.GET)
    t=render_to_string('ajax/product-list.html',{'data':data})
    return JsonResponse({'data':t})






def index(request):
    
    return render(request, 'index.html')








 
        
        
        
def run_script(request):
    data = Product.objects.all().order_by('-veriID')[:8]
    keyword = ""  # Varsayılan değeri boş bir string olarak atayın
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['q']
        
            # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['akademiDb10']
        collection = db['main_product']

        # Veritabanında en büyük veriID değerini al
        max_document = collection.find_one(sort=[("veriID", pymongo.DESCENDING)])
        max_veriID = max_document["veriID"] if max_document else 0
        veriID = max_veriID + 1

        # Anahtar kelime ve DergiPark URL'si
        url = f"https://dergipark.org.tr/tr/search?q={keyword}&section=articles"

        # Selenium WebDriver'ı başlatma
        driver = webdriver.Chrome()
        driver.get(url)

        # Sayfa içeriğini çekme
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # İlk 10 yayını bulma
        publications = soup.find_all("div", class_="card-body")[:24]

        # Eklenen makaleleri takip etmek için bir liste oluşturma
        added_documents = []

        # Türkçe ay isimlerini İngilizceye çevirme
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

        # Her bir yayının linkine tıklayarak içeriği çekme
        for publication in publications:
            link_elem = publication.find("a")
            link = link_elem["href"] if link_elem else ""

            # Eğer link zaten eklenmişse, bu yayını atla
            if link in added_documents:
                continue

            # Linki açma ve içeriği çekme
            driver.get(link)
            content_soup = BeautifulSoup(driver.page_source, "html.parser")

            # İçerikten başlığı ve yazarları çekme
            title_elem = content_soup.find("h3", class_="article-title")
            title = title_elem.text.strip() if title_elem else ""

            authors_elem = content_soup.find("p", class_="article-authors")
            authors = ", ".join([author.text.strip() for author in authors_elem.find_all("a")]) if authors_elem else ""

            # Özet kısmını çekme
            ozet_elem = content_soup.find("div", class_="article-abstract data-section")
            ozet_text = ""
            if ozet_elem:
                paragraphs = ozet_elem.find_all("p")
                ozet_text = "\n".join([p.text.strip() for p in paragraphs])

            ozet = ozet_text

            # Anahtar kelimeleri çekme
            keywords_elem = content_soup.find("div", class_="article-keywords data-section")
            keywords = [keyword.text.strip() for keyword in keywords_elem.find_all("a")] if keywords_elem else ""

            # Doi numarasını çekme
            doi_elem = content_soup.find("div", class_="article-doi data-section")
            doi_link = doi_elem.find("a")["href"] if doi_elem else ""
            doi_number = doi_link.replace("https://doi.org/", "") if doi_link else ""

            # Tablo verilerini çekme ve istenilen verileri al
            table = content_soup.find('table', class_='record_properties table')
            if table:
                tbody = table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    table_data = {}
                    for row in rows:
                        key = row.find('th').text.strip()
                        if key in ["Birincil Dil", "Yayımlanma Tarihi", "Bölüm", "Yazarlar"]:
                            value = row.find('td').text.strip()
                            table_data[key] = value

            # Pdf indirme linkini çekme
            pdf_link_elem = content_soup.find("div", id="article-toolbar").find("a", href=True)
            pdf_link = pdf_link_elem["href"] if pdf_link_elem else ""

            # Eğer bu makale veritabanında zaten varsa, bu yayını atla ve bütün bilgilerini ekrana yazdır
            if collection.find_one({"url": link}):
                existing_document = collection.find_one({"url": link})
                # print("Bu makale zaten veritabanında var:")
                # print("Yayın Adı:", existing_document["title"])
                # print("Yazarlar:", existing_document["authors"])
                # print("Özet:", existing_document["abstract"])
                # print("Anahtar Kelimeler:", ", ".join(existing_document["keywords"]))
                # print("Doi Numarası:", existing_document["doi_number"])
                # print("Yayımlanma Tarihi:", existing_document.get("publication_date", ""))
                for key, value in table_data.items():
                    print(f"{key}: {value}")

                # print("Url Adresi:", link)
                # print("-" * 50)
                continue

            publication_date_str = table_data.get("Yayımlanma Tarihi", "")
            publication_date_obj = datetime.strptime(publication_date_str, "%d %B %Y") if publication_date_str else None
            
            
            
            
            print(keywords)
            keywords1 = str(keywords)
            
            cleaned_keywords = clean_keywords(keywords1)
            print(cleaned_keywords)
            
            cleaned_keywords_list = cleaned_keywords.split(', ')
            
            authors_list = authors.split(', ')
            
            if not title or not authors or not ozet or not keywords or not publication_date_obj or not table_data.get("Birincil Dil")  or not table_data.get("Bölüm") :
                continue
       
            
            
            inserting_product = Product(
                veriID=veriID,
                title= title,
                
                abstract= ozet,
                
                doi_number= doi_number,
                url= link,  # Add the URL to the document
                search_keyword= keyword,  # Add the keyword to the document
                publication_date= publication_date_obj , # Add the publication date to the document
                # section = section_object,  # Add the section information to the document
                # primarylanguage = PrimaryLanguage.objects.get(title="İngilizce")
                # authors= authors,
                # cleaned_keywords= cleaned_keywords,
            )
            
            
            
            for anahtar_kelime in cleaned_keywords_list:
                    # Her bir anahtar kelime için ayrı bir Cleaned_keywords nesnesi oluştur
                    anahtar_kelime_object = Anahtar_kelime.objects.filter(title=anahtar_kelime).first()
                                        
                    if anahtar_kelime_object is None:
                        anahtar_kelime_object = Anahtar_kelime(title=anahtar_kelime)
                        anahtar_kelime_object.save()
                    
                    # Anahtar kelime nesnesini Product nesnesine ekle
                    inserting_product.save()
                    inserting_product.anahtar_kelime.add(anahtar_kelime_object)

                    # Product nesnesini kaydet
                    
            
            
            for authors in authors_list:
                    # Her bir anahtar kelime için ayrı bir Cleaned_keywords nesnesi oluştur
                    authors_object = Authors.objects.filter(title=authors).first()
                                        
                    if authors_object is None:
                        authors_object = Authors(title=authors)
                        authors_object.save()
                    
                    # Anahtar kelime nesnesini Product nesnesine ekle
                    inserting_product.save()
                    inserting_product.authors.add(authors_object)

                    # Product nesnesini kaydet
            
            
            
                         
               
                         
            
            
            
            
            
            
            
            
            
            section_object = Section.objects.filter(title=table_data.get("Bölüm", "")).first()
                        
            if section_object is None:
                
                    
                section_object = Section(
                    title = table_data.get("Bölüm", ""),
                )
                section_object.save()
                
            inserting_product.section = section_object          
                
            
            
            
            my_language = str(table_data.get("Birincil Dil", ""))
            
            if my_language is not None:
                my_language = my_language.capitalize()
                existing_lang = PrimaryLanguage.objects.filter(title=my_language).first()
                
                if existing_lang is None:
                    continue
                else:
                    inserting_product.primarylanguage = existing_lang
                
            inserting_product.save()    
                

            es = Elasticsearch(['https://localhost:9200'],verify_certs=False, http_auth=('elastic', 'CPN5ncI79RKPsFg1r0Xe'))
            productse = Product.objects.all()

            # Bulk işlemi için belgeler listesi
            bulk_data = []

            for producte in productse:
                # Ürünün eşsiz kimliği olarak 'id' alanını kullanın
                doc_id = str(producte.id)
                # Ürün bilgilerini alın
                product_data = producte.to_dict()
                # Bulk veri listesine ekle
                bulk_data.append({
                    "_index": "products2",
                    "_id": doc_id,  # Eşsiz kimlik olarak 'id' kullanın
                    "_source": product_data
                })

            # Bulk olarak belgeleri Elasticsearch'e ekleyin
            bulk(es, bulk_data)
                    
            
            
            
            # document = {
            #     "veriID": veriID,
            #     "title": title,
            #     "authors": authors,
            #     "abstract": ozet,
            #     "keywords": keywords,
            #     "doi_number": doi_number,
            #     "url": link,  # Add the URL to the document
            #     "search_keyword": keyword,  # Add the keyword to the document
            #     "publication_date": publication_date_obj , # Add the publication date to the document
            #     "section": table_data.get("Bölüm", ""),  # Add the section information to the document
            #     "primarylanguage": table_data.get("Birincil Dil", "")  # Add the primary language information to the document
            # }

            # Eğer başlık, yazar, özet, anahtar kelimeler veya doi numarası bilgisi eksikse bu yayını atla
            

            # print("Yayın Adı:", title)
            # print("Yazarlar:", authors)
            # print("Özet:", ozet)
            # print("Anahtar Kelimeler:", ", ".join(keywords))
            # print("Doi Numarası:", doi_number)
            for key, value in table_data.items():
                print(f"{key}: {value}")

            # PDF dosyasını indirme
            if pdf_link:
                pdf_response = requests.get(f"https://dergipark.org.tr{pdf_link}")
                # Dosya adındaki geçersiz karakterleri temizleme
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                with open(f"{clean_title}.pdf", "wb") as f:
                    f.write(pdf_response.content)
                print("Yayının PDF dosyası başarıyla indirildi.")

            print("Url Adresi:", link)
            
            # Insert the document into the collection
            # collection.insert_one(document)

            # create_main_section_collection(db, 'main_product', 'title', 'main_section')
            veriID += 1

            print("Veri MongoDB'ye kaydedildi.")
            print("-" * 50)

        client.close()
        # WebDriver'ı kapatma
        driver.quit()

        result = keyword
        
        return render(request, 'run_script.html', {'result': result, 'data': data})



def filter_data(request, ):
    

   
    
    
    languages=request.GET.getlist('primarylanguage[]')
    sections=request.GET.getlist('section[]')
    authorss=request.GET.getlist('authors[]')
    anahtar_kelimes=request.GET.getlist('anahtar_kelime[]')
    siralamas=request.GET.getlist('siralama[]')
    allProducts=Product.objects.all().order_by('-veriID').distinct()
    
    
    if len(languages)>0:
        allProducts=allProducts.filter(primarylanguage__id__in=languages).distinct()
    
    if len(sections)>0:
        allProducts=allProducts.filter(section__id__in=sections).distinct()
        
        
    if len(authorss)>0:
        allProducts=allProducts.filter(authors__id__in=authorss).distinct()
        
    if len(anahtar_kelimes)>0:
        allProducts=allProducts.filter(anahtar_kelime__id__in=anahtar_kelimes).distinct()
    
    
    
    
    if '1' in siralamas:
    # Liste içinde '1' değeri varsa bu blok çalıştırılır
        allProducts = allProducts.order_by('-publication_date')
        print("'1' değeri listenin içinde.")
    elif '2' in siralamas:
    # Liste içinde '1' değeri yoksa bu blok çalıştırılır
        allProducts = allProducts.order_by('publication_date')
        print("'2' değeri listenin içinde.")
    
    t=render_to_string('ajax/product-list.html',{'data':allProducts})
    
    
    return JsonResponse({'data':t})