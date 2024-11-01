from django.shortcuts import render
from .models import Dimensions
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from autoworld.models import YouTubeComment,YouTubeVideo
import seaborn as sns
from django.db.models import Count


def scraped_data_view(request):
    data = Dimensions.objects.all()  # Fetch all scraped data from the database
    image_names = ['fronx.jpg', 'invicto.jpg', 'jimny.jpg','vitara.jpg','xl6.jpg','ignis.jpg','baleno.jpg','ciaz.jpg','celerio.jpg','wagonr.jpg','s-presso.jpg','ertiga.jpg','swift.jpg','alto.jpg','brezza.jpg','eeco.jpg','dzire.jpg']
    combined_lists = zip(data, image_names)
    return render(request, 'auto.html', {'combined_lists': combined_lists})

def feedbacks(request):
    return render(request,'feedbacks.html')

def compare_cars(request):
    cars = Dimensions.objects.all()  # Fetch all cars for comparison
    return render(request, 'compare.html', {'cars': cars})


from collections import defaultdict

def feedback_chart(request, model_name):
    videos = YouTubeVideo.objects.filter(model__Modelname=model_name)

    # Retrieve comments with their categories and sentiments
    comments = YouTubeComment.objects.filter(video__model__Modelname=model_name).values('author','text', 'category', 'sentiment')

    # Use a new variable for the uppercase model name
    formatted_model_name = model_name.upper()

    categories = ['exterior', 'interior', 'comfort', 'engine', 'suspension', 'performance', 'quality', 'general']
    sentiments = ['Positive', 'Negative', 'Neutral']

    # Initialize a dictionary to store comments by category and sentiment
    comments_by_category = defaultdict(lambda: defaultdict(list))

    # Populate the comments_by_category dictionary
    for comment in comments:
        author=comment['author']
        category = comment['category']
        sentiment = comment['sentiment']
        text = author+" : "+comment['text']
        comments_by_category[category][sentiment].append(text)
    

    # Initialize counts with zero for each category and sentiment
    counts = {category: {sentiment: 0 for sentiment in sentiments} for category in categories}
    # Fill counts with data from the comments
    for category in comments_by_category:
        for sentiment in comments_by_category[category]:
            counts[category][sentiment] = len(comments_by_category[category][sentiment])
            
    flattened_comments = []
    for category, sentiments in comments_by_category.items():
        for sentiment, comments in sentiments.items():
            flattened_comments.append({
                'category': category,
                'sentiment': sentiment,
                'comments': comments
            })


    context = {
        'counts': counts,
        'categories': ['exterior', 'interior', 'comfort', 'engine', 'suspension', 'performance', 'quality', 'general'],
        'sentiments': ['Positive', 'Negative', 'Neutral'],
        'model_name': formatted_model_name,
        'comments_by_category': flattened_comments,  # Pass comments grouped by category and sentiment
    }

    return render(request, 'feedback_chart.html', context)

