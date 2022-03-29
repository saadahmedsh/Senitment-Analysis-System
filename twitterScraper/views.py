from json.encoder import JSONEncoder
from sys import set_asyncgen_hooks
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
import threading
from django.views.decorators import csrf
from twitterScraper.models import *
from django.views.decorators.csrf import csrf_exempt
from twitterScraper.utilities import return_tweet_data, getData
from django.core import serializers
import json




def login_page(request):
    return render(request, 'login.html')


def home_page(request):
    return render(request, 'index.html')


def return_error_page(request):
    return render(request, 'error.html')


@csrf_exempt
def insert(request, keyword):
    if request.method == 'GET':
        keyword=keyword.lower()
        if not tweet.objects.filter(keyword=keyword).exists():
            try:
                t=threading.Thread(target=return_tweet_data, args=[keyword], daemon=True)
                t.start()
                return JsonResponse({"Inserting": "True"}, safe=False)
            except:
                return JsonResponse({"Error": "Some Error Occured"}, safe=False)
        else:
            return JsonResponse({"Inserting":"False"}, safe=False)
               
                
               
        
    
          

def get_keyword(request, keyword):
    if request.method == 'GET':
        keyword=keyword.lower()
        qs=tweet.objects.filter(keyword=keyword)
        data=json.loads(serializers.serialize('json', qs))
        return JsonResponse({'data': data[0]['fields']['keyword_data']}, safe=False)
    else:
        return HttpResponse('Some Error Occured!')
        

def login_page(request):
    return render(request, 'login.html')


def registration_page(request):
    return render(request, 'register.html')



@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data=getData(request.POST)
        if not data['email']  or not data['password']:
              return JsonResponse({"exists": "Error"}, safe=False)      
        else:
            if not user.objects.filter(user_email=data['email']).exists():
                try:
                    new_user=user()
                    new_user.user_email=data['email']
                    new_user.user_password=data['password']
                    new_user.save()
                    return JsonResponse({"exists": "False"}, safe=False)
                except:
                    return JsonResponse({"exists": "Error"}, safe=False)
            else:
                return JsonResponse({"exists": "True"}, safe=False)
          
    return JsonResponse({'exists': 'Error'}, safe=False)

                
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data=getData(request.POST)
        if not data['email']  or not data['password']:
              return JsonResponse({"exists": "Error"}, safe=False)      
        else:
            if not user.objects.filter(user_email=data['email'], user_password=data['password']).exists():
                return JsonResponse({"exists": "False"}, safe=False)
            else:
                return JsonResponse({"exists": "True"}, safe=False)
    return JsonResponse({'exists': 'Error'}, safe=False)
          
                  
           

def analytics(request, keyword):
    return render(request, 'charts.html')
          

        

