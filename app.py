from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from extensions import db
from collections import defaultdict
from config import Config 
from models import User, City, Favorite, Weather, db 
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

app = Flask(__name__)

app.config.from_object(Config)
app.config['DEBUG'] = True
db.init_app(app)
migrate = Migrate(app, db)

# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_DB_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





def fetch_weather_data(city_name):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(api_url)

    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data.get('main', {}).get('temp')
        conditions = weather_data.get('weather', [{}])[0].get('description')
        icon = weather_data.get('weather', [{}])[0].get('icon')

        if temp is None or conditions is None or icon is None:
            return None  

        return {
            'temp': temp,
            'conditions': conditions,
            'icon': icon
        }
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None
    
def fetch_forecast(city_name):
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:
        forecast_data = response.json()
        processed_forecast = {}
        for forecast in forecast_data['list']:
            day_of_week = datetime.fromtimestamp(forecast['dt']).strftime('%A')
            processed_forecast[day_of_week] = {
                'max_temp': forecast['main']['temp_max'],
                'condition': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon']
            }
        return processed_forecast
    return None   
def convert_to_fahrenheit(celsius_temp):
    return round((celsius_temp * 9/5) + 32, 2)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """ 
    Render the homepage.
    
    Displays the main landing page for the weather application. 
    
    """
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user restistration.
    
    - GET: Display registration form
    - POST: Process form submission and create a new user if valid data is provided
    
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
       
        if existing_user:
            flash('Username or email is already in use. Please try another.', 'danger')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)  
            
            flash(f'Account created successfully. Welcome {new_user.username}!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            
            flash('An error occurred while creating your account. Please try again.', 'danger')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    - GET: Display login form
    -POST: Validate user credentials. If corret:
         -Logs in the user.
         -Redirects to 'index' on the first login, or 'weather' for subsequent logins.
         
    """
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Login successful! Welcome back, {user.username}!', 'success')
            if user.first_login:
                user.first_login = False  
                db.session.commit()
                return redirect(url_for('index'))  
            else:
                return redirect(url_for('weather'))  
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """ 
    Log the user out and redirect to the login page.
    - Clear the user's session and flashes a success message.
    
    """
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """
    Display weather information for a specified location.

    - GET: If a location query parameter is provided, fetch current weather and 
      forecast for that location and store the data in the session.
    - POST: Fetch current weather and forecast for a city name or ZIP code 
      provided by the user in the form, then store the data in the session.
      
    """
    city_name = None
    weather_data = None
    daily_forecast = None
    icon_code = None
    temp_unit = 'C'

    location = request.args.get('location') or request.form.get('location')
    
    if location:
        for key in ['city_name', 'weather_data', 'daily_forecast', 'icon_code', 'temp_unit']:
            session.pop(key, None)

        api_url = (f"http://api.openweathermap.org/data/2.5/weather?zip={location},US&appid={API_KEY}&units=metric"
                   if location.isdigit()
                   else f"http://api.openweathermap.org/data/2.5/weather?q={location.lower()}&appid={API_KEY}&units=metric")

        response = requests.get(api_url)
        if response.status_code != 200:
            flash(f"Could not retrieve weather data for {location}. Please try again.", 'danger')
            return render_template('weather.html')

        weather_data = response.json()
        city_name = weather_data['name'].title()
        temp_unit = 'F' if weather_data['sys']['country'] == 'US' else 'C'
        temp = convert_to_fahrenheit(weather_data['main']['temp']) if temp_unit == 'F' else weather_data['main']['temp']
        weather_data['main']['temp'] = int(temp)
        icon_code = weather_data['weather'][0]['icon']

        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            daily_forecast = defaultdict(lambda: {"max_temp": None, "condition": "", "icon": ""})
            for forecast in forecast_data['list']:
                day_of_week = datetime.fromtimestamp(forecast['dt']).strftime('%a')
                temp_celsius = forecast['main']['temp']
                temp = convert_to_fahrenheit(temp_celsius) if temp_unit == 'F' else temp_celsius

                if daily_forecast[day_of_week]["max_temp"] is None or temp > daily_forecast[day_of_week]["max_temp"]:
                    daily_forecast[day_of_week].update({
                        "max_temp": int(temp),
                        "condition": forecast['weather'][0]['description'],
                        "icon": forecast['weather'][0]['icon']
                    })

            session.update({
                'city_name': city_name,
                'weather_data': weather_data,
                'daily_forecast': daily_forecast,
                'icon_code': icon_code,
                'temp_unit': temp_unit
            })
        else:
            flash(f"Could not retrieve forecast data for {city_name}.", 'danger')

    return render_template(
        'weather.html',
        city_name=session.get('city_name'),
        weather_data=session.get('weather_data'),
        daily_forecast=session.get('daily_forecast'),
        icon_code=session.get('icon_code'),
        temp_unit=session.get('temp_unit')
    )

@app.route('/favorites', methods=['GET'])
@login_required
def favorites():
    """ 
    
    Display the user's favorite cities with current weather data.
    
    - Fetches and dislays current weather details for each favorite city.
    - Updates weather data if it's older than one hour.
    - Provides links to view weather for each favorite city.
    
    """
    favorite_cities = current_user.favorites  
    
    weather_data = []
    for favorite in favorite_cities:
        weather = Weather.query.filter_by(city_id=favorite.city.id).first()

        new_weather_data = None
        
        if not weather or (datetime.utcnow() - weather.last_updated).total_seconds() > 3600:
            new_weather_data = fetch_weather_data(favorite.city.name)
            if new_weather_data:
                if weather:
                    weather.current_temp = new_weather_data['temp']
                    weather.current_conditions = new_weather_data['conditions']
                    weather.last_updated = datetime.utcnow()
                else:
                    weather = Weather(
                        city_id=favorite.city.id,
                        current_temp=new_weather_data['temp'],
                        current_conditions=new_weather_data['conditions'],
                        last_updated=datetime.utcnow()
                    )
                    db.session.add(weather)
                db.session.commit()
                
        icon_code = new_weather_data['icon'] if new_weather_data else fetch_weather_data(favorite.city.name)['icon']
        
        if favorite.city.country == 'US':
            temp_in_fahrenheit = int(convert_to_fahrenheit(weather.current_temp))
            temp_unit = 'F'  
        else:
            temp_in_fahrenheit = int(weather.current_temp)
            temp_unit = 'C'  
       
        weather_data.append({
            'city_name': favorite.city.name,
            'current_temp': temp_in_fahrenheit, 
            'current_conditions': weather.current_conditions,
            'icon_code': icon_code,
            'favorite_id': favorite.id,  
            'temp_unit': temp_unit
        })
    
    return render_template('favorites.html', favorites=favorite_cities, weather_data=weather_data)

@app.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    """
    Add a new city to the user's favorite cities.
    
    - Retrieves city weather data to validate the city name.
    - Ensures the city isn’t already a favorite and that the user has fewer than 3 favorites.
    - Adds the city to the user's favorites list if all conditions are met.
    
    """
    city_name = request.form.get('city_name')
    if not city_name:
        flash("City name is required to add to favorites.", "danger")
        return redirect(url_for('weather'))

    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(api_url)
    if response.status_code != 200:
        flash(f"Could not retrieve data for {city_name}. Please try again.", "danger")
        return redirect(url_for('weather', location=city_name))

    weather_data = response.json()

    city = City.query.filter_by(name=city_name).first()
    if not city:
      
        city = City(
            name=weather_data['name'],
            country=weather_data['sys']['country'],
            latitude=weather_data['coord']['lat'],
            longitude=weather_data['coord']['lon']
        )
        db.session.add(city)
        db.session.commit()

    if len(current_user.favorites) >= 3:
        flash("You can only save up to 3 cities.", "danger")
    elif any(fav.city.name == city_name for fav in current_user.favorites):
        flash(f"{city_name} is already in your favorites.", "warning")
    else:
       
        favorite = Favorite(user_id=current_user.id, city_id=city.id)
        db.session.add(favorite)
        db.session.commit()
        flash(f"{city_name} added to favorites!", "success")

    return redirect(url_for('weather', location=city_name))

@app.route('/remove_favorite/<int:favorite_id>', methods=['POST'])
@login_required
def remove_favorite(favorite_id):
    """ 
    Remove a city from the user's favorite cities list.
    
    - Ensures the favorite exists and belongs to the current user.
    - Deletes the favorite entry if it exists and the user has permission. 
    
    """
    favorite = Favorite.query.get(favorite_id)
    
    if favorite and favorite.user_id == current_user.id:
        db.session.delete(favorite)
        db.session.commit()
        flash("Favorite city removed.", "success")
    else:
        flash("Unable to remove favorite. Please try again.", "danger")
        
    return redirect(url_for('favorites'))


if __name__ == '__main__':
    app.run(debug=True)
