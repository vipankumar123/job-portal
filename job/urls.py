from django.urls import path

from job.views import*

urlpatterns=[
	path('index/',index, name='index'),
	path('admin_login/',admin_login1, name='admin_login'),
	path('user_login/',user_login, name='user_login'),
	path('recruiter_login/',recruiter_login, name='recruiter_login'),
	path('signup/',signup1, name='signup'),
	path('userhome/',user_home, name='userhome'),
	path('logout/',logout1, name='logout'),
	path('recruitersignup/',recruiter_signup, name='recruitersignup'),
	path('recruiter_home/',recruiter_home, name='recruiter_home'),
	path('admin_home/',admin_home, name='admin_home'),
	path('viewusers/',view_users, name='viewusers'),
	path('delete/<int:id>/',delete, name='delete'),
	path('view_recruiters/',view_recruiter, name='view_recruiters'),
	path('change_status/<int:id>/',change_status, name='change_status'),
	path('delete_recruiter/<int:id>/',delete_recruiter, name='delete_recruiter'),
	path('recruiter_accepted/',recruiter_accepted, name='recruiter_accepted'),
	path('recruiter_pending/',recruiter_pending, name='recruiter_pending'),
	path('recruiter_rejected/',recruiter_rejected, name='recruiter_rejected'),
	path('recruiter_all/',recruiter_all, name='recruiter_all'),
	path('change_password_admin/',change_password_admin, name='change_password_admin'),
	path('change_password_user/',change_password_user, name='change_password_user'),
	path('change_password_recruiter/',change_password_recruiter, name='change_password_recruiter'),
	path('addjob/',add_job, name='addjob'),
	path('job_list/',job_list, name='job_list'),
	path('edit_job/<int:id>/',edit_job, name='edit_job'),
	path('delete_job_list/<int:id>/',delete_job_list, name='delete_job_list'),
	path('change_companylogo/<int:id>/',change_companylogo, name='change_companylogo'),
	path('latest_joblist/',latest_joblist, name='latest_joblist'),
	path('user_latestjob/',user_latestjob, name='user_latestjob'),
	path('job_detail/<int:id>/',job_detail, name='job_detail'),
	path('applyforjob/<int:id>/',applyforjob, name='applyforjob'),
	path('applied_candidate/',applied_candidate, name='applied_candidate'),
	path('contact/',contact, name='contact')




]