
from django.contrib import admin
from django.urls import path,include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('base', views.BASE, name='base'),
    path('404',views.PAGE_NOT_FOUND, name='404'),
    path('',views.HOME, name='home'),
    path('courses', views.SINGLE_COURSE, name='single_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'), 
    path('search', views.SEARCH_COURSE, name="search_course"),
    path('contactus', views.CONTACTUS, name='contactus'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register',user_login.REGISTER, name='register'),
    path('doLogin',user_login.DO_LOGIN, name='doLogin'),
    path('accounts/profile',user_login.PROFILE, name='profile'),
    path('accounts/profile/update',user_login.Profile_Update, name='profile_update'),
    path('checkout/<slug:slug>',views.CHECKOUT, name='checkout'),
    path('my-course',views.MY_COURSE, name='my_course'),
    path('course/watch-course/<slug:slug>',views.WATCH_COURSE, name='watch_course'),
    path('tools',views.TOOLS, name='tools'),
    path('tools/Engineering_Calculation_Converter',views.ENGCON, name='engcon'),
    path('tools/jpg_converter',views.IMGCON, name='imgcon'),
    path('tools/pdf_compressor',views.PDFCON, name='pdfcon'),
    path('tools/pdf_toword',views.PDFWORD, name='pdfword'),
    path('tools/resume',views.RESUME, name='resume'),
    path('tools/jarvis',views.JARVIS, name='jarvis'),


    








]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
