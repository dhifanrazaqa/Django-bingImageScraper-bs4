from django.urls import path
from .views import Home, keywordPost, detailPost, ImageDetailPost, dmca, Contact, TermsOfService, PrivacyPolicy
from django.contrib.sitemaps.views import sitemap
from .sitemap import imageSitemap

sitemaps = {
    'blog':imageSitemap
}

urlpatterns = [
    path('', Home, name="Home"),
    path('<slug:slug>', detailPost, name="detailPost"),
    path('imageDetail/<slug:slug>', ImageDetailPost, name="ImageDetailPost"),
    path('buatPost/', keywordPost, name="keywordPost"),
    path('dmca/', dmca, name="dmca"),
    path('terms-of-service/', TermsOfService, name="TermsOfService"),
    path('privacy-policy/', PrivacyPolicy, name="PrivacyPolicy"),
    path('contact/', Contact, name="Contact"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]