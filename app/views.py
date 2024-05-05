from django.shortcuts import render
from .models import *
import joblib
from django.http  import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

model=joblib.load('app/model.pkl')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict(request):
    if request.method == 'POST':
       
    
        data = json.loads(request.body)
        data=[int(i) for i in data]
        
        prediction = model.predict([data])

        if prediction[0] == 1:
            result = 'Heart Disease'
            return JsonResponse({'prediction': result,'val':1})
        else:
            result = 'No Heart Disease'
            return JsonResponse({'prediction': result, 'val':0})
    return JsonResponse({'prediction': 'error'})

