from email.mime import image
from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from .models import Post, imagePost
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import json
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
import random

# initialize beautifulsoup
def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def Home(request):
    # Get newest post
    postNewest = postNewest = Post.objects.all().order_by('-id')
    # Get search query
    search = request.GET.get('q') 
    if request.GET.get('q') != None:
        # filtering post
        postRandom = Post.objects.filter(
            Q(keyword__icontains=search)
        )
    else:
        # show random
        postRandom = Post.objects.all().order_by('?')
    
    context = {
        'post' : postRandom,
        'postNew' : postNewest,
    }
    return render(request, 'Home.html', context)

def detailPost(request, slug):
    # Get detail post using slug (images)
    postDetails = imagePost.objects.filter(slugImage=slug)
    # Get keyword
    postKeyword = get_object_or_404(Post, slug=slug)
    # Show random post (bottom section)
    postRandom = Post.objects.all().order_by('?')
    context = {
        'postDetails' : postDetails,
        'postKeyword' : postKeyword,
        'postRandom' : postRandom
    }
    return render(request, 'postDetail.html', context)

def ImageDetailPost(request, slug):
    # Get detail post using slug (single image)
    postDetails = get_object_or_404(imagePost, slugImageDetail=slug)
    #postDetails = imagePost.objects.get(slugImageDetail=slug)
    # Show random post (bottom section)
    postRandom = Post.objects.all().order_by('?')
    context = {
        'postDetails' : postDetails,
        'postRandom' : postRandom
    }
    return render(request, 'videoPostDetail.html', context)

def keywordPost(request):
    spinText = ''
    if request.method == 'POST':
        q = request.POST.get('keyword')
        jmlhPage = request.POST.get('jumlah')
        # prepare keyword
        q = q.replace('\r', '')
        q = q.split("\n")
        # loop for each keyword split by newline
        for j in q:
            # check existing keyword
            if Post.objects.filter(keyword=j).exists() == False:
                # create post
                Post.objects.create(
                            keyword=j,
                        )
                # prepare keyword to search on bing
                j = j.replace(" ", "+")
                j = j.encode('ascii', 'ignore').decode('ascii')
                # print(j)
                # get image from each page
                for i in range(int(jmlhPage)):
                    url="http://www.bing.com/images/search?q={}&pageNum={}&FORM=HDRSC2".format(j, i)
                    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
                    # bs4 working now
                    soup = get_soup(url,header)
                    for a in soup.find_all("a",{"class":"iusc"}):
                        num = 0
                        m = json.loads(a["m"])
                        turl = m["turl"]
                        murl = m["murl"]
                        title = m["t"]
                        title = title.replace("\ue000", "")
                        title = title.replace("\ue001", "")
                        desc = m["desc"]
                        spinText = spinText + " " + desc
                        # create imagePost
                        imagePost.objects.create(
                            imageTitle=title,
                            imageURL=turl,
                            imageURLHD=murl,
                            imageKeyword=Post.objects.latest('id'),
                            imageDescription=desc,
                        )
                        if num == 0:
                            postUpdate = Post.objects.get(id=Post.objects.latest('id').id)
                            postUpdate.url = turl
                            postUpdate.save()
                            num = 1
                # get spinned description
                spinText = spinText.split(" ")
                for i in imagePost.objects.filter(imageKeyword=Post.objects.latest('id').id):
                    random.shuffle(spinText)
                    i.imageDescription = ' '.join(spinText)
                    i.save()
                spinText=""
                messages.info(request, 'Success!')
            else:
                messages.info(request, j+" sudah dipost")
                        
    return render(request, "createPost.html")

def dmca(request):
    return render(request, 'DMCA.html')

def TermsOfService(request):
    return render(request, 'TermsOfService.html')

def PrivacyPolicy(request):
    return render(request, 'PrivacyPolicy.html')

def Contact(request):
    return render(request, 'contact.html')