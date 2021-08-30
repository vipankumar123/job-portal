from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from job.models import*
def index(request):
	return render(request,'index.html')

def admin_login1(request):
	error=''
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		try:
			if user.is_authenticated:
				login(request,user)
				error='no'

			else:
				error='yes'
		except Exception as e:
			print(e)
			error='yes'	
	d={'error':error}			

	return render(request,'admin_login.html',d)

def contact(request):
	return render(request,'contact.html')

def admin_home(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	rcount = Recruiter.objects.all().count()
	scount = Studentuser.objects.all().count()
	d={'rcount':rcount,'scount':scount}
	return render(request,'admin_home.html',d)

def latest_joblist(request):
	job = Job.objects.all().order_by('-start_date')
	d={'job':job}
	return render(request,'latest_joblist.html',d)	


def signup1(request):
	error=''
	d={}
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		mobile = request.POST['mobile']
		gender = request.POST['gender']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		image = request.FILES['image']
		try:
			if password1!=password2:
				print('password does not match')
			else:	
				user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, 
					password=password1)
				Studentuser.objects.create(user=user, mobile=mobile, gender=gender, image=image, Type='student')
				error='no'
				print('user created')
				return redirect('user_login')
		except Exception as e:
			print(e)
			error='yes'
	d={'error':error}		
	return render(request,'signup.html')		

def user_login(request):
	error=''
	if request.method=='POST':
		username = request.POST['username']
		password1 = request.POST['password1']
		user = authenticate(username=username, password=password1)
		if user:
			try:
				user1 = Studentuser.objects.get(user=user)
				if user1.Type=='student':
					login(request,user)
					error='no'
				else:
					error='yes'
			except Exception as e:
				print(e)
				error='yes'
		else:
			error='yes'
	d={'error':error}				
	return render(request,'userlogin.html',d)

def user_home(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	user = request.user
	studentuser = Studentuser.objects.get(user=user)

	error=''
	d={}
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		mobile = request.POST['mobile']
		gender = request.POST['gender']
		
		studentuser.user.first_name = first_name
		studentuser.user.last_name = last_name
		studentuser.user.email = email
		studentuser.mobile = mobile
		studentuser.gender = gender

		try:

			studentuser.save()
			error='no'
				
				
		except Exception as e:
			print(e)
			error='yes'

		try:
			image = request.FILES['image']
			studentuser.image = image
			studentuser.save()
			error='no'
		except Exception as e:
			pass	 	
	d={'studentuser':studentuser, 'error':error}		
	return render(request,'userhome.html',d)

def user_latestjob(request):
	job = Job.objects.all().order_by('-start_date')
	user = request.user
	student = Studentuser.objects.get(user=user)
	data = Apply.objects.filter(student=student)
	li = []
	for i in data:
		li.append(i.job.id)
	d={'job':job,'li':li}
	return render(request,'user_latestjob.html',d)

def job_detail(request,id):
	job = Job.objects.get(id=id)
	
	d={'job':job}
	return render(request,'job_detail.html',d)

def applyforjob(request,id):

	if not request.user.is_authenticated:
		return redirect('user_login')

	error=''
	user = request.user
	student = Studentuser.objects.get(user=user)
	job = Job.objects.get(id=id)
	date1 = date.today()
	if job.end_date < date1:
		error='close'
	elif job.start_date > date1:
		error='notopen'
	else:
		if request.method=='POST':
			resume = request.FILES['resume']
			Apply.objects.create(student=student, job=job, resume=resume, apply_date=date.today())
			error='done'

	d={'error':error}		
	return render(request,'applyforjob.html',d)	

def applied_candidate(request):

	if not request.user.is_authenticated:
		return redirect(request,'recruiter_login')
	data = Apply.objects.all()
	
	d={'data':data}

	return render(request,'applied_candidate.html',d)	

	

def logout1(request):
	logout(request)
	return redirect('index')		

def recruiter_login(request):
	error=''
	if request.method=='POST':
		username = request.POST['username']
		password1 = request.POST['password1']
		user = authenticate(username=username, password=password1)
		if user:
			try:
				user1 = Recruiter.objects.get(user=user)
				if user1.Type=='Recruiter' and user1.status !='Accept':
					login(request,user)
					error='no'
					return redirect('recruiter_home')
				else:
					error='yes'
			except Exception as e:
				print(e)
				error='not'
		else:
			error='yes'
	d={'error':error}	
	return render(request,'recruiter_login.html',d)

def recruiter_signup(request):
	error=''
	d={}
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		mobile = request.POST['mobile']
		gender = request.POST['gender']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		image = request.FILES['image']
		company = request.POST['company']


		try:
			if password1!=password2:
				print('password does not match')
			else:	
				user = User.objects.create_user(first_name=first_name,username=username, last_name=last_name, email=email, 
					password=password1)
				Recruiter.objects.create(user=user, mobile=mobile, gender=gender, image=image, Type='Recruiter', status='pending', company=company)
				error='no'
				print('user created')
				return redirect('recruiter_login')
		except Exception as e:
			print(e)
			error='yes'
	d={'error':error}		
	return render(request,'recruiter_signup.html',d)		

def recruiter_home(request):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	user = request.user
	recruiter = Recruiter.objects.get(user=user)

	error=''
	d={}
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		mobile = request.POST['mobile']
		gender = request.POST['gender']
		
		recruiter.user.first_name = first_name
		recruiter.user.last_name = last_name
		recruiter.user.email = email
		recruiter.mobile = mobile
		recruiter.gender = gender

		try:

			recruiter.save()
			error='no'
				
				
		except Exception as e:
			print(e)
			error='yes'

		try:
			image = request.FILES['image']
			recruiter.image = image
			recruiter.save()
			error='no'
		except Exception as e:
			pass	 	
	d={'recruiter':recruiter, 'error':error}	
	return render(request,'recruiter_home.html',d)

def view_users(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	data = Studentuser.objects.all()
	d={'data':data}	
	return render(request,'view_users.html',d)

def delete(request,id):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	data = Studentuser.objects.get(id=id)
	data.delete()
	
	return redirect('viewusers')

def view_recruiter(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiter = Recruiter.objects.all()
	d={'recruiter':recruiter}	
	return render(request,'view_recruiters.html',d)

def delete_recruiter(request,id):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	data = Recruiter.objects.get(id=id)
	data.delete()
	
	
	return redirect('view_recruiters')			

def recruiter_pending(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiter = Recruiter.objects.filter(status='pending')
	d={'recruiter':recruiter}
	
	return render(request,'recruiter_pending.html',d)

def change_status(request,id):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	error=''	
	data = Recruiter.objects.get(id=id)
	if request.method=='POST':
		s = request.POST['status']
		data.status= s
		try:
			data.save()
			error='no'
		except Exception as e:
			error='yes'	
	d={'data':data, 'error':error}
	
	return render(request,'change_status.html',d)			

def recruiter_accepted(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiter = Recruiter.objects.filter(status='Accept')
	d={'recruiter':recruiter}
	
	return render(request,'recruiter_accepted.html',d)


def recruiter_rejected(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiter = Recruiter.objects.filter(status='Reject')
	d={'recruiter':recruiter}
	
	return render(request,'recruiter_rejected.html',d)

def recruiter_all(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiter = Recruiter.objects.all()
	d={'recruiter':recruiter}
	
	return render(request,'recruiter_all.html',d)

def change_password_admin(request):

	if not request.user.is_authenticated:
		return redirect(request,'admin_login')
	error=''
	if request.method=='POST':
		current_password = request.POST['current_password']	
		new_password = request.POST['new_password']	
		confirm_password = request.POST['confirm_password']
		if new_password==confirm_password:
			user = User.objects.get(username__exact=request.user.username)
			user.set_password(new_password)
			user.save()
			print('114')
			error='no'

		else:
			error='yes'
	d={'error':error}

	return render(request,'change_password_admin.html',d)

def change_password_user(request):

	if not request.user.is_authenticated:
		return redirect(request,'admin_login')
	error=''
	if request.method=='POST':
		current_password = request.POST['current_password']	
		new_password = request.POST['new_password']	
		confirm_password = request.POST['confirm_password']
		if new_password==confirm_password:
			user = User.objects.get(id=request.user.id)
			if user.check_password(current_password):
				user.set_password(new_password)
				user.save()
				print('114')
				error='no'

		else:
			error='not'
			
	d={'error':error}

	return render(request,'change_password_user.html',d)

def change_password_recruiter(request):

	if not request.user.is_authenticated:
		return redirect(request,'recruiter_login')
	error=''
	if request.method=='POST':
		current_password = request.POST['current_password']	
		new_password = request.POST['new_password']	
		confirm_password = request.POST['confirm_password']
		if new_password==confirm_password:
			user = User.objects.get(id=request.user.id)
			if user.check_password(current_password):
				user.set_password(new_password)
				user.save()
				print('114')
				error='no'

		else:
			error='not'
			
	d={'error':error}

	return render(request,'change_password_recruiter.html',d)				

def add_job(request):

	if not request.user.is_authenticated:
		return redirect('recruiter_login')

	error=''
	if request.method=='POST':
		title = request.POST['title']
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		salary = request.POST['salary']
		image = request.FILES['image']
		experience = request.POST['experience']
		location = request.POST['location']
		skills = request.POST['skills']
		description = request.POST['description']
		user = request.user
		print(user)
		recruiter = Recruiter.objects.get(user=user)
		try:
			Job.objects.create(recruiter=recruiter, start_date=start_date, end_date=end_date, title=title, salary=salary,
			image=image, description=description, skills=skills, location=location, creationdate=date.today())
			error='no'
		except Exception as e:
			print('error is :',e)
			error='yes'
	d={'error':error}		
	return render(request,'add_job.html',d)	

def job_list(request):

	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	user =request.user
	recruiter = Recruiter.objects.get(user=user)
	job = Job.objects.filter(recruiter=recruiter)
	d={'job':job}	

	return render(request,'job_list.html',d)	

def edit_job(request,id):

	if not request.user.is_authenticated:
		return redirect('recruiter_login')

	error=False
	job = Job.objects.get(id=id)
	if request.method=='POST':
		title = request.POST['title']
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		salary = request.POST['salary']
		experience = request.POST['experience']
		location = request.POST['location']
		skills = request.POST['skills']
		description = request.POST['description']


		job.title = title
		job.salary = salary
		job.experience = experience
		job.location = location
		job.skills = skills
		job.description = description
		try:
			job.save()
			error='no'
		except Exception as e:
			print('error is :',e)
			error='yes'

		if start_date:

			try:
				job.start_date = start_date	
				job.save()
			except Exception as e:
				pass
		else:
			pass

		if end_date:

			try:
				job.end_date = end_date
				job.save()
			except Exception as e:
				pass
		else:
			pass

	d={'error':error,'job':job}		
	return render(request,'edit_job.html',d)	

def delete_job_list(request,id):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	data = Job.objects.get(id=id)
	data.delete()

	
	return redirect('job_list')	

def change_companylogo(request,id):

	if not request.user.is_authenticated:
		return redirect('recruiter_login')

	error=False
	job = Job.objects.get(id=id)
	if request.method=='POST':
		image = request.FILES['image']
		
		job.image = image
		try:
			job.save()
			error='no'
		except Exception as e:
			print('error is :',e)
			error='yes'


	d={'error':error,'job':job}		
	return render(request,'change_companylogo.html',d)	








































