from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from .models import StudentModel
from .studentform import StudentForm,LoginForm
from django.views.decorators.csrf import csrf_exempt
# celery redis
from api.tasks import mul,visit_cache

registration_page="reg.html"
login_page="login.html"
login_url='login'
home_url='home'
home_page='home.html'

@csrf_exempt
def registrationForm(request):
    if request.method=='POST':
        # request.FILES for profile image and resume
        fm=StudentForm(request.POST,request.FILES)
        if fm.is_valid():
            nm=fm.cleaned_data['name']
            em=fm.cleaned_data['email']
            pw=fm.cleaned_data['password']
            pincode=fm.cleaned_data['pincode']
            dob=fm.cleaned_data['dob']

            appointment_time = fm.cleaned_data['appointment_time']
            appointment_date=fm.cleaned_data['appointment_date']
            appointment_datetime=fm.cleaned_data['appointment_datetime']
            is_agreed=fm.cleaned_data['is_agreed']
            agree_terms=fm.cleaned_data['agree_terms']
            gender=fm.cleaned_data['gender']

            interests=fm.cleaned_data['interests']
            profile_pic=fm.cleaned_data['profile_pic']
            resume=fm.cleaned_data['resume']
            
            website=fm.cleaned_data['website']
            mobile_no=fm.cleaned_data['mobile_no']
            
            slug=fm.cleaned_data['slug']
            ip_address=fm.cleaned_data['ip_address']
            rating=fm.cleaned_data['rating']
            content=fm.cleaned_data['content']
            
            marriedornot=fm.cleaned_data['marriedornot']
            split_date_time=fm.cleaned_data['split_date_time']

            print('pincode',pincode)
            print('dob',dob)
            print('appointment_time',appointment_time)
            print('appointment_date',appointment_date)
            print('appointment_datetime',appointment_datetime)
            print('is_agreed',is_agreed)
            print('agree_terms',agree_terms)
            print('gender',gender)
            print('interests',interests)
            print('profile_pic',profile_pic)
            print('resume',resume)
            print('website',website)
            print('mobile_no',mobile_no)
            print('slug',slug)
            print('ip_address',ip_address)
            print('rating',rating)
            print('content',content)
         
            print('marriedornot',marriedornot)
            print('split_date_time',split_date_time)

            # put data into db 
            stud_create=StudentModel(
                name=nm,
                email=em,
                password=pw,
                pincode=pincode,
                dob=dob,
                appointment_time=appointment_time,
                appointment_date=appointment_date,
                appointment_datetime=appointment_datetime,
                is_agreed=is_agreed,
                
                gender=gender,
                interests=interests,
                profile_pic=profile_pic,
                resume=resume,

                website=website,
                mobile_no=mobile_no,
                slug=slug,

                ip_address=ip_address,
                rating=rating,
                content=content,
                marriedornot=marriedornot,
                split_date_time=split_date_time)
            stud_create.save()
            return redirect(login_url)
        else:
            return render(request,registration_page, {'fm':fm})
    else:
        fm=StudentForm()
        # calling celery,redis
        visits = visit_cache.delay()
        muls = mul.delay(1,5)
        context = {
            "fm": fm,
            'visits':visits,
            'mul':muls
        }
        print('task= ',visits)
        print('multiplication = ',muls)
        return render(request,registration_page,context)

def homepage(request):
    fname = request.session.get('name','guest')
    if fname=='guest':
        print('if')
        print(fname)
        return redirect(login_url)
    else:
        keys=request.session.keys()
        items=request.session.items()
        getexpireatbrowser = request.session.get_expire_at_browser_close()
        get_expiry_age = request.session.get_expiry_age()
        expiry_date = request.session.get_expiry_date()
        return render(request,home_page,{'fname':fname,'keys':keys,'items':items,'getexpireatbrowser':getexpireatbrowser,'expiry_date':expiry_date,
    'get_expiry_age':get_expiry_age})

def login(request):
    fname = request.session.get('name','guest')
    if fname=='guest':
        print('if guest')
        if request.method=='POST':
            fm=LoginForm(request.POST)
            if fm.is_valid():
                nm=fm.cleaned_data['name']
                pw=fm.cleaned_data['password']
                try:
                    student_chk = StudentModel.objects.get(name=nm,password=pw)
                    print('student_chk',student_chk)

                    # set session with name for 10 seconds
                    request.session['name']=nm
                    request.session.set_expiry(50)# for 50 seconds
                    return redirect(home_url)
                except StudentModel.DoesNotExist:
                    return HttpResponse("""
                        <html>
                            <body>
                                <h3 style="color:red;">Login Failed</h3>
                                <p>You will be redirected shortly in 3 seconds...</p>
                                <script>
                                    setTimeout(function(){
                                        window.location.href = '/login/';
                                    }, 3000);  // 3 seconds
                                </script>
                            </body>
                        </html>
                    """)
                
            else:
                return render(request, login_page, {"fm": fm})
        else:
            fm=LoginForm()
            return render(request,login_page,{'fm':fm})
    else:
        return redirect(home_url)
    
def logout(request):
    request.session.flush()
    request.session.clear()
    return render(request,'logout.html')