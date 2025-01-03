import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime
import requests
from gemitest import generate_response_and_save

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "AMIP6EYSS83VRYBR"

# Function to make the assistant speak
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to take voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=25)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            say("Sorry, I'm having trouble connecting to the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            say("An error occurred.")
            print(f"Error: {e}")
            return ""

# Function to get stock price
def get_stock_price(stock_symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": stock_symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = data["Global Quote"]["05. price"]
            return f"The current price of {stock_symbol.upper()} is ${price}."
        else:
            return "Sorry, I couldn't fetch the stock price. Please check the stock symbol or try again later."
    except Exception as e:
        return f"An error occurred while fetching the stock price: {e}"

# Function to get response and save it to a file
def handle_query(query):
    response = generate_response_and_save(query)
    return response

# Main logic
if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Jarvis AI. How can I assist you?")
    while True:
        query = takeCommand().lower()

        # List of websites
        sites = [
            ['youtube', 'https://www.youtube.com'],
            ['wikipedia', 'https://www.wikipedia.com'],
            ['google', 'https://www.google.com'],
            ['linkedin','https://www.linkedin.com']
        ]

        # Check if the query is to open a website
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} sir")
                webbrowser.open(site[1])
                break

        # Respond with the current time
        if 'the time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, the time is {current_time}")

        # Open the camera
        if "open camera" in query:
            say("Opening camera")
            os.system("start microsoft.windows.camera:")

        # Fetch stock market updates
        if "stock price of" in query:
            stock_symbol = query.split("stock price of")[-1].strip()
            say(f"Fetching the stock price for {stock_symbol}. Please wait.")
            stock_price = get_stock_price(stock_symbol)
            say(stock_price)
            print(stock_price)

        # Trigger response when "Jarvis using AI" is said
        if "jarvis using ai" in query:
            say("Processing your request sir")
            response = handle_query(query)
            print("Response saved:", response)

        # Exit the assistant
        if "exit" in query or "quit" in query:
            say("Goodbye, sir. Have a great day!")
            break