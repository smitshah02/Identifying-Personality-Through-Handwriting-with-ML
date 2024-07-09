# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import cv2
import pickle
import numpy as np
from .extract import *
from django.conf import settings
from PIL import Image

# views.py
from django.shortcuts import render
# Your existing imports...

# Your existing index view
def index(request):
    return render(request, 'index.html')

# Your new view for page2.html
def page2(request):
    return render(request, 'page2.html')

# Your new view for page3.html
def page3(request):
    return render(request, 'page3.html')

# Your new view for page4.html
#def page4(request):
#    return render(request, 'page4.html')


def predict(request):
    if request.method == 'POST' and request.FILES['image']:
        username = request.POST.get('username', 'Guest')
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        img_path = fs.url(filename)
        print(os.path.join(settings.BASE_DIR, "media", filename))
        img = cv2.imread(os.path.join(settings.BASE_DIR, "media", filename))

        with Image.open(os.path.join(settings.BASE_DIR, "media", filename)) as img2:
            dpi = img2.info.get('dpi')
            mm_per_px = 25.4 / dpi[0] if dpi else 25.4 / 96  # Fallback to default DPI if not available

        print(mm_per_px)
        predictions, qualitative_interpretations, features_list = predict_personality_traits(img, mm_per_px)
        
        traits_img_processing = get_traits(features_list, mm_per_px)
        
        featureValue = {
            'BASE_LINE_ANGLE': f"{features_list[0]} deg",
            'TOP_MARGIN': f"{features_list[1]} % of whole page",
            'LINE_SPACING': f"{features_list[2]} mm",
            'SLANT_ANGLE': f"{features_list[3]} deg",
            'WORD_SPACING': f"{features_list[4]} mm",
            'LETTER_SIZE': f"{features_list[5]} mm"
        }

        return render(request, 'predict.html', {
            'predictions': predictions,
            'img_path': img_path,
            'username': username,
            'featureValue': featureValue,
            'traits_img_processing': traits_img_processing,
            'qualitative_interpretations': qualitative_interpretations
        })
    return render(request,'predict.html')


# Assuming the existence of the models dictionary, features dictionary, and other helper functions from your original script

models_dir = os.path.join(settings.BASE_DIR, "models")
models = {
    'Extroversion': os.path.join(models_dir, 'Extroversion_model.pickle'),
    'Introversion': os.path.join(models_dir, 'Introversion_model.pickle'),
    'Emotional_Stability': os.path.join(models_dir, 'Emotional_stability_model.pickle'),
    'Neuroticism': os.path.join(models_dir, 'Neuroticism_model.pickle'),
    'Openness_to_Experience': os.path.join(models_dir, 'Openness_to_experience_model.pickle'),
    'Conscientiousness': os.path.join(models_dir, 'Conscientiousness_model.pickle'),
    'Agreeableness': os.path.join(models_dir, 'Agreeableness_model.pickle')
}

features = {
    'Extroversion': [5, 3, 2, 1, 4],
    'Introversion': [5, 3, 2, 1, 4],
    'Emotional_Stability': [0, 4],
    'Neuroticism': [0, 3],
    'Openness_to_Experience': [5, 3, 2, 4],
    'Conscientiousness': [5, 2, 1],
    'Agreeableness': [5, 3, 2, 4]
}

def predict_personality_traits(img, mm_per_px):
    features_list_ = extract_feature(img)
    indices = [2, 4, 5]  # The indices for features that need scaling
    for index in indices:
        features_list_[index] *= mm_per_px
    features_list = [round(float(num), 2) for num in features_list_]

    predictions = {}
    qualitative_interpretations = {}

    for trait, model_path in models.items():
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        trait_features = np.array(features[trait])
        trait_features_list = [features_list[i] for i in trait_features]
        trait_features_array = np.array(trait_features_list).reshape(1, -1)

        prediction = model.predict(trait_features_array)[0]
        predictions[trait] = prediction

        # Mapping the quantitative score to a qualitative interpretation
        qualitative_interpretations[trait] = get_qualitative_interpretation(trait, prediction)

    return predictions, qualitative_interpretations, features_list

def get_qualitative_interpretation(trait, score):
    # Define thresholds and interpretations for each trait

    if trait == 'Introversion':
        return 'Highly Sociable and Energetic' if score <= 0.25 else 'Moderately Sociable' if score <= 0.5 else 'Somewhat Reserved' if score <= 0.7 else 'Deep Thinker and Reflective'
    elif trait == 'Emotional_Stability':
        return 'Calm, Composed, and Resilient under stress' if score > 0.7 else 'Generally stable with occasional sensitivity' if score > 0.4 else 'More sensitive to stress and emotional fluctuations'
    elif trait == 'Neuroticism':
        return 'Sensitive and Nervous' if score > 0.7 else 'Somewhat Sensitive' if score > 0.4 else 'Emotionally Stable'
    elif trait == 'Openness_to_Experience':
        return 'Innovative and Creative' if score > 0.7 else 'Somewhat open to new experiences' if score > 0.4 else 'Routine preferable and familiarity over novelty and change'
    elif trait == 'Conscientiousness':
        return 'Well-organized, dependable, and disciplined' if score > 0.7 else 'Generally reliable but can occasionally be flexible with plans' if score > 0.4 else 'More spontaneous and may struggle with organization and punctuality'
    elif trait == 'Agreeableness':
        return 'Compassionate, cooperative, and harmony valued' if score > 0.7 else 'Generally friendly but has a competitive side' if score > 0.4 else 'More competitive, less concerned with others'
    else:
        return 'Unknown Trait'

"""
def get_qualitative_interpretation(trait, score):
    if trait == 'Introversion':
        if score <= 0.25:
            return 'Highly Sociable and Energetic'
        elif 0.25 < score <= 0.5:
            return 'Moderately Sociable'
        elif 0.5 < score <= 0.7:
            return 'Somewhat Reserved'
        else:
            return 'Deep Thinker and Reflective'

    elif trait == 'Emotional_Stability':
        if score > 0.7:
            return 'Calm, Composed, and Resilient under stress'
        elif 0.4 < score <= 0.7:
            return 'Generally stable with occasional sensitivity'
        else:
            return 'More sensitive to stress and emotional fluctuations'
    
    elif trait == 'Neuroticism':
        if score > 0.7:
            return 'Sensitive and Nervous'
        elif 0.4 < score <= 0.7:
            return 'Somewhat Sensitive'
        else:
            return 'Emotionally Stable'
    
    elif trait == 'Openness_to_Experience':
        if score > 0.7:
            return 'Innovative and Creative'
        elif 0.4 < score <= 0.7:
            return 'Somewhat open to new experiences'
        else:
            return 'Routine preferable and familiarity over novelty and change'
    
    elif trait == 'Conscientiousness':
        if score > 0.7:
            return 'Well-organized, dependable, and disciplined'
        elif 0.4 < score <= 0.7:
            return 'Generally reliable but can occasionally be flexible with plans'
        else:
            return 'More spontaneous and may struggle with organization and punctuality'
    
    elif trait == 'Agreeableness':
        if score > 0.7:
            return 'Compassionate, cooperative, and harmony valued'
        elif 0.4 < score <= 0.7:
            return 'Generally friendly but has a competitive side'
        else:
            return 'More competitive, less concerned with others'
    
    else:
        return 'Unknown Trait'
"""

# Add other helper functions from your script here

# Function definitions for get_baseline, get_top_margin, get_line_spacing, get_slant_of_writing, get_spacing_between_words, get_size_of_letters

def get_traits(features_list, mm_per_px):
    traits_img_processing = {
            'BASE_LINE_ANGLE': get_baseline(features_list[0]),
            'TOP_MARGIN': get_top_margin(features_list[1]),
            'SLANT_ANGLE': get_slant_of_writing(features_list[3]),
            'LETTER_SIZE': get_size_of_letters(features_list[5]),
            'WORD_SPACING': get_spacing_between_words(features_list[4])
    }
    return traits_img_processing

def get_baseline(baseline):
    if -15 <= baseline <= -1:
        return "Fatigue"
    elif -1 < baseline <= 1:
        return "Dependability"
    elif 1 < baseline <= 15:
        return "Ambition"
    return "Unknown"

def get_top_margin(top_margin):
    if 0 <= top_margin <= 5:
        return "Focus"
    elif 5 < top_margin <= 10:
        return "Balance"
    elif top_margin > 10:
        return "Creativity"
    return "Unknown"

def get_slant_of_writing(slant_of_writing):
    if slant_of_writing == 0:
        return "Independence"
    elif 0 < slant_of_writing <= 9:
        return "Empathy"
    elif 9 < slant_of_writing <= 18:
        return "Goal-orientation"
    elif 18 < slant_of_writing <= 27:
        return "Passion"
    elif -9 <= slant_of_writing < 0:
        return "Charm"
    elif -18 <= slant_of_writing < -9:
        return "Goal-orientation"
    elif -27 <= slant_of_writing < -18:
        return "Evasiveness"
    return "Unknown"

def get_size_of_letters(size_of_letters):
    if size_of_letters > 8:
        return "Boldness"
    elif 5 < size_of_letters <= 8:
        return "Adaptability"
    elif 2 < size_of_letters <= 5:
        return "Modesty"
    return "Unknown"

def get_spacing_between_words(spacing_between_words):
    if spacing_between_words <= 11:
        return "Hostility"
    elif 11 < spacing_between_words <= 22:
        return "Self-Confidence"
    elif spacing_between_words > 22:
        return "Extroversion"
    return "Unknown"

# You might need to adjust the get_line_spacing function as per your requirements
def get_line_spacing(line_spacing):
    # Assuming 'line_spacing' is numeric. Adjust the logic if it's categorized differently.
    if line_spacing > 6:
        return "Heavy"
    elif 4 < line_spacing <= 6:
        return "Normal"
    return "Tight"

# Ensure to include the `models` and `features` dictionaries as defined in your original script.

# Add the logic for loading models and extracting features as shown earlier.


