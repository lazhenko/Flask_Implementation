# weather_microservice

1. Which stores the temperature of one city every hour, for example, Kyiv (specified in env).
Alternatively, you can use this API: https://openweathermap.org/api.
2. According to the API, it gives the temperature history for the day (which we set):
  - day - GET parameters in Y-m-d format;
  - x-token - a line of 32 characters is transmitted through the header (this is just a constant against which you need to check the request to filter out spam);
  - return format for all responses (including errors) in JSON format;
#########################################################################

Create a Virtual Environment:
    Open your terminal or command prompt.
    Run the command python3 -m venv venv to create a virtual environment named venv within your project directory. Feel free to name it differently if you prefer.

Activate the Virtual Environment:
    On Windows: .\venv\Scripts\activate
    On macOS/Linux: source venv/bin/activate
    Your prompt will change to indicate that you are now working within the virtual environment.

Install Requirements:
    Ensure you have a requirements.txt file in your project directory listing all necessary packages.
    Install the packages using pip install -r requirements.txt.

Run "microservice_weather.py":
    python microservice_weather.py
    
Deactivating the Virtual Environment:
    When you're done, you can exit the virtual environment by running the command deactivate.
