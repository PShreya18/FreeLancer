from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
# Create your views here.
from django.urls import reverse
from datetime import date
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def home(request):
    return render(request, 'home.html')


def freelancer_login(request):
    if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Freelancer.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("/freelancer_homepage")
            else:
                thank = True
                return render(request, "freelancer_login.html", {"thank":thank})
    return render(request, "freelancer_login.html")


def freelancer_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/freelancer_login/')
    applicant = Freelancer.objects.get(user=request.user)
    project = Project.objects.filter(creator=applicant)
    print(project)
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        #last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']
        skills = (request.POST['skills'])
        #skills = skills.split(',')
        print(skills,name)
        applicant.user.email = email
        applicant.user.first_name = name
        applicant.name = name
        applicant.email = email
        #applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.skills = skills
        applicant.save()
        applicant.user.save()

        alert = True
        return render(request, "freelancer_homepage.html", {'alert':alert})
    return render(request, "freelancer_homepage.html", {'applicant':applicant,'project':project})


def all_jobs(request):
    jobs = Job.objects.all().order_by('-start_date')
    applicant = Freelancer.objects.get(user=request.user)
    apply = Application.objects.filter(freelancer=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "all_jobs.html", {'jobs':jobs, 'data':data})


def job_detail(request, myid):
    job = Job.objects.get(id=myid)
    return render(request, "job_detail.html", {'job':job})


def job_apply(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicant = Freelancer.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    date1 = date.today()
    if job.end_date < date1:
        closed=True
        return render(request, "job_apply.html", {'closed':closed})
        '''elif job.start_date > date1:
        notopen=True
        return render(request, "job_apply.html", {'notopen':notopen})'''
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Application.objects.create(job=job, company=job.company, freelancer=applicant, resume=resume, apply_date=date.today())
            alert=True
            return render(request, "job_apply.html", {'alert':alert})
    return render(request, "job_apply.html", {'job':job})


def show_resume(request):
    #return render(request,"homePage/static/P.Shreya_CV.docx")
    file_path = 'homePage/static/P.Shreya_CV.docx'
    with open(file_path, 'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/ms-word')
        # response = HttpResponse(template_output)
        response['Content-Disposition'] = 'attachment;filename=P.Shreya_CV.docx'
        return response

def all_applicants(request):
    company = Hirer.objects.get(user=request.user)
    application = Application.objects.filter(company=company)
    return render(request, "all_applicants.html", {'application':application})


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['name']
        #last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        skills = request.POST['skills']
        #image = request.FILES['image']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(username=username,
                                        password=password1)
        applicants = Freelancer.objects.create(user=user,phone=phone, gender=gender, skills = skills, type="applicant")
        user.save()
        applicants.save()
        return render(request, "freelancer_login.html")
    return render(request, "signup.html")


def company_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        #last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        #image = request.FILES['image']
        company_name = request.POST['company_name']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(email=email, username=username,
                                        password=password1)
        company = Hirer.objects.create(user=user, phone=phone, gender=gender, company_name=company_name,
                                         type="company")
        user.save()
        company.save()
        return render(request, "hirer_login.html")
    return render(request, "hirer_signup.html")


def company_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Hirer.objects.get(user=user)
            if user1.type == "company":
                login(request, user)
                return redirect("/company_homepage")
        else:
            alert = True
            return render(request, "hirer_login.html", {"alert":alert})
    return render(request, "hirer_login.html")


def company_homepage(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    company = Hirer.objects.get(user=request.user)
    if request.method=="POST":
        email = request.POST['email']
        name = request.POST['name']
        #last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        company.user.email = email
        company.user.first_name = name
        #company.user.last_name = last_name
        company.phone = phone
        company.gender = gender
        company.save()
        company.user.save()
        alert = True
        return render(request, "company_homepage.html", {'alert':alert})
    return render(request, "company_homepage.html", {'company':company})


def add_job(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']
        user = request.user
        company = Hirer.objects.get(user=user)
        job = Job.objects.create(company=company, title=title,start_date=start_date, end_date=end_date, salary=salary, experience=experience, location=location, skills=skills, description=description, creation_date=date.today())
        job.save()
        alert = True
        return render(request, "add_job.html", {'alert':alert})
    return render(request, "add_job.html")


def job_list(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    companies = Hirer.objects.get(user=request.user)
    jobs = Job.objects.filter(company=companies)
    return render(request, "job_list.html", {'jobs':jobs})

def delete_job(request,myid):
    job = Job.objects.get(id=myid)
    job.delete()
    return render(request,"job_list.html")

def Logout(request):
    logout(request)
    return redirect('/')

def view_freelancers(request):
    applicants = Freelancer.objects.all()
    return render(request, "view_applicants.html", {'applicants': applicants})


def view_hirers(request):
    company = Hirer.objects.all()
    return render(request, "all_companies.html", {'companies': company})


def add_projects(request):
    if request.method == "POST":
        title = request.POST['project_title']
        domain = request.POST['domain']
        price = request.POST['price']
        demo = request.POST['demo']
        repo = request.POST['repo']
        description = request.POST['description']
        user = request.user
        creator = user
        freelancer = Freelancer.objects.get(user=user)
        project = Project.objects.create(creator=freelancer, title=title,description=description, domain=domain, price = price,demo=demo,repo=repo)
        project.save()
        print(project)
        return render(request, "add_projects.html")
    return render(request, "add_projects.html")


def view_projects(request):
    projects = Project.objects.all()
    return render(request, "all_projects.html", {'projects': projects})


def filter_projects(request,domain):
    pid = int(domain)
    project_map={1:"Machine Learning",2:"Web Development",3:"Internet of Things",4:"Blockchain",5:"Data Science",6:"Android",7:"NLP",8:"Cybersecurity",9:"PHP",10:"Python",11:"C",12:"Java"}
    projects = Project.objects.filter(domain=project_map[pid])
    if not projects:
        return HttpResponse("No projects found!")
    return render(request,"all_projects.html",{'projects':projects})


def buy_project(request,seller,price):
    if not request.user.is_authenticated:
        return redirect("/freelancer_login")
    #buyer = request.user
    #buyer = Freelancer.objects.get(user=buyer)
    #print(buyer,buyer.coins,Freelancer.coins,Freelancer.objects.all().values())
    currency = 'INR'
    amount = int(price)*100
    #bcoins = buyer.coins*100
    #if bcoins >= amount:
     #   seller = Freelancer.objects.get(id=2)
      #  print(seller,seller.coins)
       # buyer.coins -= amount//100
       # seller.coins += amount//100
       # print(buyer,buyer.coins,seller,seller.coins,Freelancer.objects.get(name=buyer),User.objects.get(freelancer=buyer))
        #buyer = request.user
        #return render(request,'all_projects.html')
    #else:
        # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print(context)
    return render(request, 'buy.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            #amount = request.POST.get('razorpay_amount', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print(params_dict)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result is not None:
                amount = int(10)*100
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request,'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfailed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfailed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
        
'''  
def port(request):
    return render(request, 'FreelancerPortfolio.html')


def sign(request):
    return render(request, 'SignINOUT.html')


def profile(request):
    return render(request, 'ProfileCreationForm.html')


def login_user(request):
    if request.method == 'POST':
        #context = dict()
        username = request.POST['usname']
        email = request.POST['eml']
        password = request.POST['pwd1']
        #userType = request.POST['utype']
        user = authenticate(request, username=username, email=email ,password=password)
        print(user,username,password,"login")
        if user:
            login(request, user)
            if request.COOKIES.get('post_project'):
                return form_state(request, id=2)
            else:
            return HttpResponseRedirect('FreelancerPortfolio.html')
        else:
            #context['error_message'] = 'Username or password is incorrect'
            return render(request, 'SignINOUT.html',)
    return HttpResponseRedirect('FreelancerPortfolio.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home.html'))


def signup_user(request):
    #context = dict()
    # skill_list = Skill.objects.all()
    # language_list = CommunicationLanguage.objects.all()
    # context['skill_list'] = skill_list
    # context['language_list'] = language_list
    if request.method == 'POST':
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pwd']
        userType = request.POST['userType']
        gender = request.POST['gender']
        # skills = request.POST.getlist('skills[]')
        # languages = request.POST.getlist('languages[]')
        user = User.objects.create_user(username=username, email=email, password=password)
        cuser = CustomUser(user=user, gender=gender, userType=userType)
        user.save()
        cuser.save()
        for uskill in skills:
            skill = Skill.objects.get(skill_name=uskill)
            cuskill = UsersSkill()
            cuskill.skill = skill
            cuskill.user = cuser
            cuskill.level_of_proficiency = int(request.POST[skill.skill_name])
            cuskill.save()
        for ulanguage in languages:
            language = CommunicationLanguage.objects.get(
                language_name=ulanguage)
            culanguage = UsersCommunicationLanguage()
            culanguage.language = language
            culanguage.user = cuser
            culanguage.level_of_fluency = int(
                request.POST[language.language_name])
            culanguage.save()
        login(request, user)
        print(username,password,gender,email,userType,"signup")
        #return HttpResponseRedirect(reverse(sign(request)))
        #return render(request,'SignINOUT.html')
    return render(request, 'FreelancerPortfolio.html')
'''