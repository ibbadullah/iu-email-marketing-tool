from django.db import models

# Create your models here.
class EmailsBank(models.Model):
    email = models.EmailField(null=True,blank=True)
    saved_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    class Meta:
        db_table = "emails_bank"

# Campaign history
class CampaignHistory(models.Model):
    emailId = models.ForeignKey(EmailsBank,on_delete=models.CASCADE,verbose_name="email_id")
    status = models.CharField(blank=True,null=True,max_length=50)
    date = models.DateTimeField(blank=True,null=True,auto_now=True)

    class Meta:
        db_table = "campaignhistory"