Open weather map API:
https://openweathermap.org/api



# Description

Quik Weather is a weather forecasting website that provides users with quick and accurate weather information for their chosen locations. Users can view current weather conditions, a detailed 5-day forecast, and save up to three favorite locations for easy access. The site aims to deliver an intuitive and visually appealing experience for users who need reliable weather updates on the go.

## Features

## Key Features Implemented
1. ### User Registration and Login:
* **Purpose:**  Allows users to create a personalized account for managing their favorite cities.
* **Why:** Adding user accounts enables saved preferences, making it easier for users to quickly access their preferred weather information.
2. ### Current Weather Data:
* **Purpose:** Displays real-time weather information, including temperature, conditions, and location-specific weather icons.
* **Why:** Immediate access to current weather conditions is essential for users making short-term plans.
3. ### 5-Day Forecast:
* **Purpose:** Provides an extended view of weather conditions over the next five days.
* **Why:** A multi-day forecast allows users to make informed decisions about upcoming events, trips, or daily activities.
4. ### Favorite Cities:
* **Purpose:** Allows users to save up to three favorite cities, displaying the current weather for each on their dashboard.
* **Why:** This feature provides quick access to frequently checked locations, enhancing usability and personalization.
5. ### Error Handling and Notifications:
* **Purpose:** Provides feedback messages when a location cannot be found or data is unavailable.
* **Why:** Clear messaging improves user experience by managing expectations and offering guidance.

## User Flows
1. ### New User Registration and Login:
* **Steps:**
    1. The user visits the registration page and signs up with a username, email, and password.
    2. They log in and are greeted with a welcome message.
    3. After login, they can add favorite cities, view the current weather, and explore the forecast.
2. ### Searching for Weather:
* **Steps:**
    1. The user enters a city name or ZIP code in the search field.
    2. The website fetches and displays current conditions, a weather icon, and a 5-day forecast for the location.
3. ### Adding Favorite Cities:
* **Steps:**
    1. The user searches for a location and clicks “Add to Favorites.”
    2. Up to three locations can be saved, with the option to remove any at any time.

## API Used

**OpenWeather API:** This API provides the weather data displayed on the site, including current weather and 5-day forecasts. The API offers extensive weather information for cities globally, enabling reliable and up-to-date weather data retrieval.

## Technology Stack
* **Backend:**
    * **Python:** Core programming language used for server-side development.
    * **Flask:** Web framework that handles routing, session management, and database interactions.
    * **PostgreSQL:** Relational database used to store user data, favorites, and weather-related information.
* **Frontend:**
    * **HTML/CSS:** Structure and styling of the site, ensuring a responsive and user-friendly design.
    * **Bootstrap:** CSS framework used for styling and layout, providing a consistent, modern UI.
* **API:**
    * **OpenWeather API:** Provides weather and forecast data for various locations.
* **Tools:**
    * **Postman:** For testing API calls and responses.
    * **Git/GitHub:** Version control for tracking changes and collaborating on the project.

## Additional Notes

* **Session Management:** Flask's session handling ensures that user sessions remain active, improving user experience by keeping users logged in during their browsing session.
* **Responsive Design:** The site layout adapts across device sizes, making it accessible and easy to use on both desktop and mobile devices.
* **Security Considerations:** Passwords are hashed using bcrypt to protect user credentials, and user input is validated to prevent potential injection attacks.
