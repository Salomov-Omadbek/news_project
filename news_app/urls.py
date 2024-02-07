from django.urls import path
from .views import news_list,news_detail,ContactPage,page_404,SinglePageView,homepage,LocalNewsView,\
    XorijNewsView,TehnologyNewsView,SportNewsView
urlpatterns = [
    path('all/', news_list, name='all_news_list'),
    path('news/<slug:news>/',news_detail, name='news_detail_page'),
    path('',homepage.as_view(),name='home_page'),
    path('contact/',ContactPage.as_view(),name='contact_page'),
    path('single_page/',SinglePageView,name='single_page'),
    path('404_page', page_404,name='404_page'),
    path('sport/',SportNewsView.as_view(),name='sport_page'),
    path('xorij/',XorijNewsView.as_view(),name='xorij_page'),
    path('local/',LocalNewsView.as_view(),name='local_page'),
    path('tehnology/',TehnologyNewsView.as_view(),name='technology_page'),
]