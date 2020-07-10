from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from .applications.ui_predictor import Predictor


def index(request):

    context = {
        'title': 'Free Forecasts'
    }

    return render(request, 'main/index.html', context)


def model(request):
    feedback = ''
    predictor = Predictor()

    if request.method == 'POST':
        if 'predict_' in request.POST:
            try:
                predictor.predict()
                feedback = "Success"
            except:
                feedback = "Prediction failed"

    context = {
        'title': 'Free Forecasts',
        'feedback': feedback
    }

    return render(request, 'main/model.html', context)
