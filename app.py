import streamlit as st
import os
import google.generativeai as palm
from langdetect import detect
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
palm.configure(api_key=api_key)
translator = Translator()

models = [model for model in palm.list_models()]
model_name = models[1].name

def generate_questions(model_name, text):
    response = palm.generate_text(
        model=model_name,
        prompt=f"Generate questions from the following text:\n\n{text}\n\nQuestions:",
        max_output_tokens=150
    )
    questions = response.result.strip() if response.result else "No questions generated."
    return questions

def main():
    st.title("Inquisitive: A Multilingual AI Question Generator")

    user_text = st.text_area("Enter the text you want questions generated from: ")

    if user_text:
        detected_language = detect(user_text)
        if detected_language!='en':
            translated_text = translator.translate(user_text, src=detected_language, dest="en").text
        else:
            translated_text = user_text

    if st.button("Generate Questions"):
        if user_text:
            questions = generate_questions(model_name, translated_text)
            if detected_language !='en':
                questions = translator.translate(questions, src="en", dest=detected_language).text
            st.subheader("Generated Questions:")
            st.write(questions)
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()