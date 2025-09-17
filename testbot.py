import pandas as pd
import streamlit as st
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

while True:
    user_input = input("You: ")

    if(user_input.strip() == ''):
        break

    response = chat.send_message(user_input)
    print(f"Bot: {response.text}")