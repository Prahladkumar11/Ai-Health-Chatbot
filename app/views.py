from django.shortcuts import render
from .models import *
from django.http  import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib

model=joblib.load('app/model.pkl')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict(request):
    if request.method == 'OPTIONS':
        # Handle preflight OPTIONS request
        response = JsonResponse({'message': 'Preflight request handled'})
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5173'
        response['Access-Control-Allow-Methods'] = 'POST'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    elif request.method == 'POST':
        # Handle POST request
        # Your existing code for handling the prediction
        data = json.loads(request.body)
        data = [float(i) for i in data]
        prediction = model.predict([data])
        print(data)
        print("prediction+++++++",prediction[0])
        if prediction[0] == 1:
            result = 'Heart Disease'
            
            return JsonResponse({'prediction': result, 'val': 1})
        else:
            result = 'No Heart Disease'
            return JsonResponse({'prediction': result, 'val': 0})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)