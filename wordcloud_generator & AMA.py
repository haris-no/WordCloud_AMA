import os
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import openai
from dotenv import load_dotenv

# Load environment variables from .env file if you choose to use it
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI credentials
openai.api_key = openai_api_key

# Function to scrape comments (or any text) from a webpage
def scrape_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # This example scrapes all paragraph text from a page
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Function to generate a word cloud from text
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Function to get a response from OpenAI GPT-3.5 Turbo model
def get_openai_response(prompt):
    try:
        # Call OpenAI's GPT-3.5 Turbo model using the provided prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Adjust this based on your needs
            temperature=0.7
        )
        # Extract and return the text from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"

def main():
    url = input("Enter a URL to scrape: ")
    text = scrape_webpage(url)

    if text:
        print("Generating word cloud...")
        generate_wordcloud(text)
        
        while True:
            # Ask for a prompt based on the scraped text
            user_prompt = input("\nAsk a question about the article (or type 'exit' to quit): ")
            if user_prompt.lower() == 'exit':
                print("Exiting...")
                break

            # Combine the user's question with the scraped text
            combined_prompt = f"Article content: {text}\nQuestion: {user_prompt}\nAnswer:"

            # Get a response from OpenAI
            response = get_openai_response(combined_prompt)
            print(f"OpenAI's Response: {response}")
    else:
        print("Failed to scrape the webpage.")

if __name__ == "__main__":
    main()
