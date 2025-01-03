import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import os
import google.generativeai as genai

# API keys
ALPHA_VANTAGE_API_KEY = "AMIP6EYSS83VRYBR"
from config import apikey

genai.configure(api_key=apikey)

# Configure OpenAI model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Helper functions
def say(text):
    """Speak a text string using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def take_voice_input():
    """Capture voice input from the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=15)
            query = recognizer.recognize_google(audio, language="en-in")
            st.write(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            st.write("Error connecting to speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            st.write(f"An error occurred: {e}")
            return ""

def get_stock_price(stock_symbol):
    """Fetch the stock price using Alpha Vantage API."""
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
            return "Couldn't fetch stock price. Please check the stock symbol."
    except Exception as e:
        return f"Error fetching stock price: {e}"

def handle_query(query):
    """Generate a response using OpenAI's Gemini model and save it."""
    response = chat_session.send_message(query)
    folder = "responses"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/response_{len(os.listdir(folder)) + 1}.txt"
    with open(filename, 'w') as file:
        file.write(response.text)
    return response.text

# Streamlit UI
st.set_page_config(page_title="EVO BR_AI_N", page_icon="🤖", layout="wide")
st.title("Welcome to EVO_BRAIN 🤖")

if st.button("Start Listening"):
    user_query = take_voice_input()
    if user_query:
        if "stock price of" in user_query:
            stock_symbol = user_query.split("stock price of")[-1].strip()
            st.write("Fetching stock price...")
            stock_response = get_stock_price(stock_symbol)
            st.write(stock_response)
            say(stock_response)
        else:
            st.write("Processing your query with AI...")
            ai_response = handle_query(user_query)
            st.write(ai_response)
            say(ai_response)
