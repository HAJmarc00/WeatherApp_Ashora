from django.shortcuts import render
from django.conf import settings
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import quote
import json
import re


def weather_view(request):
    api_key = settings.OPENWEATHER_API_KEY
    city = request.GET.get('city', 'Tehran').strip().title()

    temperature = '--'
    condition = 'N/A'
    icon = ''
    image_url = ''
    theme_class = 'light'
    error_message = ''

    # Validate city: only letters (English or Persian), spaces and hyphens allowed
    if not re.match(r'^[\u0600-\u06FFa-zA-Z\s\-]+$', city):
        error_message = "Invalid input. Please enter only letters (no numbers or symbols)."
    else:
        try:
            encoded_city = quote(city)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric&lang=en'
            response = urlopen(url)
            data = json.loads(response.read().decode('utf-8'))

            if data.get("cod") == "404":
                error_message = f"City '{city}' not found."
            else:
                temperature = round(data['main']['temp'])
                condition = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                image_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'
                theme_class = 'dark' if icon.endswith('n') else 'light'

        except URLError as e:
            print("Network error:", e)
            error_message = "Network error. Please try again later."
            image_url = 'https://openweathermap.org/img/wn/01d@2x.png'
            theme_class = 'light'

        except Exception as e:
            print("Unexpected error:", e)
            error_message = "Unexpected error occurred. Please try again."

    context = {
        'city': city,
        'temperature': temperature,
        'condition': condition,
        'icon': icon,
        'image_url': image_url,
        'theme_class': theme_class,
        'error_message': error_message
    }

    return render(request, 'weather.html', context)
