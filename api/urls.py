from django.urls import path

from api import views

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()

router.register('register',views.SignupView,basename='register')

router.register('expences',views.ExpenseView,basename='expences')

router.register('incomes',views.IncomeView,basename="incomes")

urlpatterns=[
    
    path('token/',ObtainAuthToken.as_view()),

    path('expences/summary/',views.ExpenseSummayView.as_view()),

    path('incomes/summary/',views.IncomeSummayView.as_view()),
    
]+router.urls
