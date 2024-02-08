from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from .forms import ContactsForm, CommentsForm
from .models import News, Category,Contacts
from django.views.generic import UpdateView, DeleteView


def news_list(request):
    news_list = News.objects.all()
    context = {'news_list': news_list}
    return render(request, 'news/news_list.html', context)

def news_detail(request,news):
    news = get_object_or_404(News, slug=news,status = News.Status.Published)
    comments =news.comments.filter(active=True)
    new_comments = None
    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            new_comments = comment_form.save(commit=False)
            new_comments.news = news
            new_comments.user = request.user
            new_comments.save()
    else:
        comment_form = CommentsForm()
    context = {'news': news, 'comments': comments, 'new_comments': new_comments,'comment_form': comment_form}
    return render(request, 'news/news_detail.html', context)

class homepage(TemplateView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_posts'] = News.objects.all().order_by('-publish_time')[:5]
        context['news_list'] = News.objects.all().order_by('-publish_time')[:10]
        context['sport'] = News.objects.all().filter(category__name ='Sport').order_by('-publish_time')
        context['xorij'] = News.objects.all().filter(category__name='Xorij').order_by('-publish_time')[:5]
        context['mahaliy'] = News.objects.all().filter(category__name='Mahaliy').order_by('-publish_time')[0:6]
        context['technology_news'] = News.objects.all().filter(category__name='Texnologiya').order_by('-publish_time')
        context['lastest_news'] = News.objects.all().order_by('-publish_time')[:5]
        return context


class ContactPage(TemplateView):
    tempate_name = 'news/contact.html'

    def get(self,request,*args,**kwargs):
        form = ContactsForm()
        context = {
            'form':form
        }
        return render(request,'news/contact.html',context)

    def post(self,request, *args,**kwargs):
        form = ContactsForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(' <h1> Raxmat :)')

        context = {
            'form':form
        }

        return render(request,'news/contact.html',context)

def SinglePageView(request):
    context = {

    }
    return render(request, 'news/single_page.html', context)

def page_404(requst):
    context = {

    }
    return render(requst,'news/404.html',context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahaliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Mahaliy').order_by('-publish_time')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Sport').order_by('-publish_time')
        return news

class TehnologyNewsView(ListView):
    model = News
    template_name = 'news/tehnology.html'
    context_object_name = 'tehnologiya_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Texnologiya').order_by('-publish_time')
        return news

class XorijNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Xorij').order_by('-publish_time')
        return news

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body','category','images','status',)
    template_name = 'update/news_edit.html'

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'update/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(CreateView):
    model = News
    fields = ('title', 'slug','body','category','images','status',)
    template_name = 'update/news_create.html'
