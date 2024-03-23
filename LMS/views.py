from django.shortcuts import redirect,render
from app.models import Categories, Course, Level,Video,UserCource
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from app.models import Profile, Course
import random

def BASE(request):
    return render(request, 'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('id')

    context = {
        'category':category,
        'course':course,
    }

    return render(request, 'Main/home.html', context)
def SINGLE_COURSE(request):
    category= Categories.get_all_categories(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        'level':level,
        'course':course,
        'FreeCourse_count':FreeCourse_count,
        'PaidCourse_count':PaidCourse_count,
    }
    return render(request, 'Main/single_course.html', context)

def filter_data(request):
     category = request.GET.getlist('category[]')
     level = request.GET.getlist('level[]')
     price=request.GET.getlist('price[]')
     if price==['PriceFree']:
         course = Course.objects.filter(price=0)
     elif price==['PricePaid']:
          course = Course.objects.filter(price__gte=1)
     elif price==['PriceAll']:
          course = Course.objects.all()
     elif category:
         course=Course.objects.filter(category__id__in = category).order_by('-id')
     elif level:
         course=Course.objects.filter(level__id__in =level).order_by('-id')    
     else:
         course= Course.objects.all().order_by('-id')
     context={
         'course':course
     }    

     t = render_to_string('ajax/course.html',context)
     return JsonResponse({'data': t})
   

def CONTACTUS(request):
    category=Categories.get_all_categories(Categories)
    context={
        'category':category

    }
    return render(request, 'Main/contactus.html',context)

def SEARCH_COURSE(request):
    category=Categories.get_all_categories(Categories)
    
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
        'category':category
    }
    return render(request,'search/search.html',context)





from django.shortcuts import redirect

def COURSE_DETAILS(request, slug):
    category = Categories.get_all_categories(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    course = Course.objects.filter(slug=slug).first()
    if not course:
        return redirect('404')

    try:
        user_enrolled_courses = UserCource.objects.filter(user=request.user).values_list('course', flat=True)
    except UserCource.DoesNotExist:
        user_enrolled_courses = []

    # Filter out courses that the user has already enrolled in
    all_courses = Course.objects.exclude(id__in=user_enrolled_courses)
    all_courses = list(all_courses)
    random.shuffle(all_courses) 

    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'all_courses': all_courses[:3],
    }

    return render(request, 'course/course_details.html', context)




def PAGE_NOT_FOUND(request):
    category=Categories.get_all_categories(Categories)
    context={
        'category':category

    }
    return render(request, 'error/404.html',context)

def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)

    if course.price == 0:
        course = UserCource(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request,'Course are successfully enrolled')
        return redirect('my_course')
    
    return render(request, 'checkout/checkout.html')

def MY_COURSE(request):
    course=UserCource.objects.filter(user=request.user)
    category=Categories.get_all_categories(Categories)
    context={
        'course':course,
        'category':category,
    }
    return render(request, 'course/my-course.html',context)

def WATCH_COURSE(request,slug):
    course=Course.objects.filter(slug=slug)
    lecture=request.GET.get('lecture')
    video=Video.objects.get(id=lecture)
    if course.exists():
        course=course.first()
    else:
        return redirect('404')    
    context={
        'course':course,
        'video' : video,
    }
    return render(request,'course/watch-course.html',context)

def TOOLS(request):
    category=Categories.get_all_categories(Categories)
    context={
        'category':category

    }
    return render(request,'Main/tools/tools.html',context)
def ENGCON(request):
    return render(request,'Main/tools/engineer_calculation_converter.html',)
def IMGCON(request):
    return render(request,'Main/tools/jpg to png convertor.html',)
def PDFCON(request):
    return render(request,'Main/tools/pdf compressor.html',)
def PDFWORD(request):
    return render(request,'Main/tools/pdf to word.html',)
def RESUME(request):
    return render(request,'Main/tools/resume.html',)
def JARVIS(request):
    return render(request,'Main/tools/jarvis.html',)

def course_profile(request):
    course_id = request.GET.get('course_id')
    course = None
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            # Handle the case where the course doesn't exist
            pass

    user_profile = Profile.objects.get(user=request.user)
    interests = user_profile.interests.split(',')
    

    recommended_courses = []
    for interest in interests:
        interest = interest.strip()
        courses = Course.objects.filter(title__icontains=interest)
        recommended_courses.extend(courses)

    context = {
        'course': course,
        'recommended_courses': recommended_courses
    }
    return render(request, 'course_details.html', context)

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    jaccard_index = intersection / union
    return jaccard_index
def courses_from_interests(interests, courses_data):
    courses_similarity = {}
    for course, course_interests in courses_data.items():
        similarity = jaccard_similarity(interests, course_interests)
        courses_similarity[course] = similarity
    sorted_courses = sorted(courses_similarity.items(), key=lambda x: x[1], reverse=True)
    sorted_courses = [course[0] for course in sorted_courses]
    return sorted_courses
def recommend_courses(request):
    # Fetch all user interests from the database
    all_users_interests = get_all_users_interests()
    
    recommended_courses = []
    
    for interests in all_users_interests:
        recommended_courses.extend(courses_from_interests(interests))
    
    return render(request, 'course_details.html', {'recommended_courses': recommended_courses})

def get_all_users_interests():
    # Query all user profiles and retrieve their interests
    all_profiles = Profile.objects.all()
    all_users_interests = [set(profile.interests.split(',')) for profile in all_profiles]
    return all_users_interests

def courses_from_interests(interests):
    # Query courses from the database based on interests
    # Assuming that interests are stored as tags in the Course model
    courses = Course.objects.filter(tags__in=interests).distinct()
    return courses