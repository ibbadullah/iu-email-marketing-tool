from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import *

# Login/Home view
class HomeView(views.View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('CampaignGen')
        return render(request,'home.html') 

    def post(self,request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # User athenticating
            user = authenticate(username=username,password=password)
            # Checking and logining
            if user is not None:
                login(request,user)
                return redirect('CampaignGen')
            else:
                messages.info(request,'Username or password is incorrect!')
                return redirect('HomeView')


# Campaign Generator Render View
@login_required(login_url='HomeView')
def RenderCampaignGen(request):
    totalEmails = EmailsBank.objects.all().count()
    totalSent = CampaignHistory.objects.all().count()
    return render(request,'campaign.html',{"TotalEmails":totalEmails,"TotalSent":totalSent})

# Logout function
def logoutUser(request):
    logout(request)
    messages.info(request,'You have logout sucessfully.')
    return redirect('HomeView')

#Last 50 emails record
@login_required(login_url='HomeView')
def Last50Emails(request):
    totalSent = CampaignHistory.objects.all().count()
    historyData = CampaignHistory.objects.all().order_by('-id')[:50]
    #return render(request,'email-template.html')
    return render(request,'record.html',{"Data":historyData,"TotalSent":totalSent})

#Campaign generator
@login_required(login_url='HomeView')
def campaignGenerator(request):
    if request.method == "POST":
        fromLimit = int(request.POST['fromLimit'])-1
        toLimit = int(request.POST['toLimit'])
        title = request.POST['subject']
        mailBody = request.POST['mailbody']
        tempLocation = "email-template.html"
        mailsLimit = toLimit - fromLimit
        totalEmails = EmailsBank.objects.all().count()
        # Checking from and two limit
        if fromLimit >= toLimit:
            messages.warning(request,"From limit shouldn't be equal to or greater than to limit.")
            return redirect('CampaignGen')
        elif mailsLimit > 50:
            messages.warning(request,"You can't send more than 50 emails per batch.")
            return redirect('CampaignGen')
        elif totalEmails < 2:
            messages.warning(request,"Please add more emails.")
            return redirect('CampaignGen')
        elif totalEmails == fromLimit or fromLimit > totalEmails:
            messages.warning(request,"From limit shouldn't be greater than or equal to total emails.")
            return redirect('CampaignGen')
        # Getting email addresses
        getEmailAdresses = EmailsBank.objects.all().order_by('id')[fromLimit:toLimit]
        for mail in getEmailAdresses:
            html_content = render_to_string(tempLocation,{"Title":title,"Message":mailBody})
            text_content = strip_tags(html_content)
            sendEmail = EmailMultiAlternatives(
                title,
                text_content,
                settings.EMAIL_HOST_USER,
                [mail.email]
            )
            sendEmail.attach_alternative(html_content,"text/html")
            sendEmail.send()
            
            # Saving sent email record
            CampaignHistory.objects.create(emailId=mail,status="Sent")
        return render(request,"campaign-completed.html")

# Deleting campaigns history
@login_required(login_url='HomeView')
def deleteCampaigns(request):
    deleteCampn = CampaignHistory.objects.all()
    deleteCampn.delete()
    messages.info(request,"Campaigns history deleted successfully.")
    return redirect("CampaignGen")
