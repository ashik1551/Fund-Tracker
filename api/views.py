from datetime import datetime

from django.shortcuts import render

from django.db.models import Sum

from django.utils import timezone

from .models import User,Expense,Income

from rest_framework.views import APIView

from rest_framework.viewsets import ViewSet,ModelViewSet

from rest_framework.response import Response

from rest_framework import status,authentication,permissions

from .serializers import UserSerializer,ExpenseSerializer,IncomeSerializer

from .permissions import OwnerOnly

class SignupView(ViewSet):
    
    def create(self,request,*args,**kwargs):
        
        serializer=UserSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(data=serializer.data,status=status.HTTP_200_OK)
            
        else:
            
            return Response(data=serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        
class ExpenseView(ModelViewSet):
    
    queryset=Expense.objects.all()

    serializer_class=ExpenseSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        
        qs=Expense.objects.filter(owner=self.request.user)

        if 'month' in request.query_params:

            month=request.query_params.get('month')

            qs=qs.filter(created_date__month=month)
        
        if 'year' in request.query_params:

            year=request.query_params.get('year')

            qs=qs.filter(created_date__year=year)
        
        if 'category' in request.query_params:

            category=request.query_params.get('category')

            qs=qs.filter(category=category)

        if 'priority' in request.query_params:

            priority=request.query_params.get('priority')

            qs=qs.filter(priority=priority)
        
        if len(request.query_params.keys())==0:

            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)
        
        serializer=ExpenseSerializer(qs,many=True)

        return Response(data=serializer.data)

class IncomeView(ModelViewSet):

    queryset=Income.objects.all()

    serializer_class=IncomeSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        
        qs=Income.objects.filter(owner=self.request.user)

        if 'month' in request.query_params:

            month=request.query_params.get('month')

            qs=qs.filter(created_date__month=month)
        
        if 'year' in request.query_params:

            year=request.query_params.get('year')

            qs=qs.filter(created_date__year=year)
        
        if 'category' in request.query_params:

            category=request.query_params.get('category')

            qs=qs.filter(category=category)
        
        if len(request.query_params.keys())==0:

            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)
        
        serializer=IncomeSerializer(qs,many=True)

        return Response(data=serializer.data)

class ExpenseSummayView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.filter(owner=request.user)

        if "from" in request.query_params and "to" in request.query_params:

            start=datetime.strptime(request.query_params.get('from'),"%Y-%m-%d").date()

            end=datetime.strptime(request.query_params.get('to'),"%Y-%m-%d").date()

            qs=qs.filter(created_date__range=[start,end])
        
        else:
            
            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)

        total_expense=qs.values('amount').aggregate(total=Sum('amount'))["total"]   #Total expense

        category=qs.values('category').annotate(total=Sum('amount')).order_by('total')    #Category-wise sum

        priority=qs.values('priority').annotate(total=Sum('amount'))    #priority-wise sum

        data={
            "total":total_expense,
            "category_summary":category,
            "priority":priority
        }

        return Response(data=data)
    
class IncomeSummayView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=Income.objects.filter(owner=request.user)

        if "from" in request.query_params and "to" in request.query_params:

            start=datetime.strptime(request.query_params.get("from"),"%Y-%m-%d").date()

            end=datetime.strptime(request.query_params.get("to"),"%Y-%m-%d").date()

            qs=qs.filter(created_date__range=[start,end])
        
        else:
            
            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)

        total_income=qs.values('amount').aggregate(total=Sum('amount'))['total']    #Total income

        category=qs.values('category').annotate(total=Sum('amount')).order_by('-total')     #Category-wise sum

        data={
            "total":total_income,
            "category":category
        }

        return Response(data=data)