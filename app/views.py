from django.shortcuts import render
from .models import HeartDiseaseData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
from sklearn.linear_model import LogisticRegression

model = joblib.load('app/model.pkl')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        name = data['name']
        answers = data['answers']
        
        # Convert answers to appropriate types
        answers = [float(i) for i in answers]
        
        # Create and save the HeartDiseaseData instance
        heart_disease_data = HeartDiseaseData(
            name=name,
            age=answers[0],
            sex=int(answers[1]),
            cp=int(answers[2]),
            trestbps=int(answers[3]),
            chol=int(answers[4]),
            fbs=int(answers[5]),
            restecg=int(answers[6]),
            thalach=int(answers[7]),
            exang=int(answers[8]),
            oldpeak=answers[9],
            slope=int(answers[10]),
            ca=int(answers[11]),
            thal=int(answers[12]),
            target=model.predict([answers])[0]   # Assuming target is unknown at the moment
        )
        heart_disease_data.save()

        # Make prediction
        prediction = model.predict([answers])
        print(answers)
        print("prediction+++++++", prediction[0])

        if prediction[0] == 1:
            result = 'Heart Disease'
        else:
            result = 'No Heart Disease'
        
        return JsonResponse({'prediction': result, 'val': int(prediction[0])})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def retrain(request):
    try:
        # Fetch data once
        data = HeartDiseaseData.objects.all()
        # Prepare features and target
        features = list(data.values_list('age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'))
        target = list(data.values_list('target', flat=True))
        models=LogisticRegression(max_iter=1000)
        # Retrain the model
        models.fit(features, target)
        
        # Save the model to disk
        joblib.dump(models, 'app/model.pkl')
        print('Model retrained successfully')
        
        return JsonResponse({'status': 'Model retrained successfully'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)