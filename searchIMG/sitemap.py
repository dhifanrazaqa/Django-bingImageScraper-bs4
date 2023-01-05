from django.contrib.sitemaps import Sitemap
from .models import Post
 
 
class imageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.1
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date_modified
        
    def location(self,obj):
        return '/%s' % (obj.slug)