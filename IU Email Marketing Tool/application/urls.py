from django.urls import path
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name="HomeView"),
    path('campaign-generator/',RenderCampaignGen,name="CampaignGen"),
    path('logoutuser',logoutUser,name="LogoutUser"),
    path('record',Last50Emails,name="EmailsRecord"),
    path('delete-c-history',deleteCampaigns,name="DelCampaigns"),
    path('batch-completed',campaignGenerator,name="SendEmails"),
]