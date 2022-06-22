# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, DecimalField
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app.models import Chat
import os
import joblib
import speech_recognition as sr
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests
from . import preprocess


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def home(request):
    context = 'page-detector'
    chats = Chat.objects.all()
    all_users = User.objects.filter(messages__isnull=False).distinct()
    HSCount = 0
    NonHSCount = 0

    for chat in chats:
        if chat.sentiment == "HATE SPEECH!":
            HSCount += 1
        elif chat.sentiment == "NOT HATE SPEECH!":
            NonHSCount += 1

    ctx = {
        'home': 'active',
        'chat': chats,
        'allusers': all_users,
        'HSCount': HSCount,
        'NonHSCount': NonHSCount,
        'segment': context
    }

    html_template = loader.get_template('page-detector.html')
    return HttpResponse(html_template.render(ctx, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


def upload(request):
    customHeader = request.META['HTTP_MYCUSTOMHEADER']

    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    filename = str(Chat.objects.count())
    filename = filename + "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    # put additional logic like creating a model instance or something like this here
    r = sr.Recognizer()
    harvard = sr.AudioFile(filename)
    with harvard as source:
        audio = r.record(source)
    msg = r.recognize_google(audio, language="id-ID")
    os.remove(filename)

    # Sentiment Analysis
    print(msg)

    saved_model = joblib.load("C:/Users/user/Desktop/Skripsi/app/HateSpeechClassifier.joblib")
    saved_tfidf = joblib.load("C:/Users/user/Desktop/Skripsi/app/HateSpeechTF-IDFVectorizer.joblib")
    message = [msg]
    vectorized_tweets = saved_tfidf.transform(message)
    input_prediction = saved_model.predict(vectorized_tweets)

    for i in range(len(message)):
        if input_prediction[i] == 1:
            result = "HATE SPEECH!"
        else:
            result = "NOT HATE SPEECH!"

    chat_message = Chat(user=request.user, message=msg, sentiment=result)
    if msg != '':
        chat_message.save()
    return redirect('/')


def messages(request):
    chat = Chat.objects.all()
    lower = Lower(Chat.sentiment)
    return render(request, 'messages.html', {'chat': chat})


def predict(request):
    if request.method == 'POST':
        context = {}
        context['segment'] = 'index'
        message = request.POST.get('message', None)
        saved_model = joblib.load("C:/Users/user/Desktop/FullSkripsi/Skripsi/app/HateSpeechClassifier.joblib")
        saved_tfidf = joblib.load("C:/Users/user/Desktop/FullSkripsi/Skripsi/app/HateSpeechTF-IDFVectorizer.joblib")
        message = [message]
        vectorized_tweets = saved_tfidf.transform(message)
        input_prediction = saved_model.predict(vectorized_tweets)

        for i in range(len(message)):
            if input_prediction[i] == 1:
                result = {'res': "\nHate Speech!\n".upper()}
            else:
                result = {'res': "\n Not Hate Speech!\n".upper()}

        ctx = {
            'result': result,
            'segment': context
        }
        return render(request, 'sentiment-result.html', result)

    else:
        return render(request, 'index.html')
