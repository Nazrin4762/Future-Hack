import random
from flask import Flask, render_template, request, send_from_directory
import requests
import wikipediaapi

app = Flask(__name__)

# List of random topics for unrelated results
random_topics = [
    "ocean", "mountain", "cityscape", "astronomy", "wildlife",
    "architecture", "technology", "art", "history", "sports",
    "literature", "culture", "fashion", "food", "travel", "science",
    "music", "education", "environment", "psychology", "space", "robotics"
]

# Dummy data for demonstration
dummy_data = [
    {
        'topic': 'Flask',
        'summary': 'Flask is a micro web framework for Python based on Werkzeug, Jinja2.',
        'link': 'https://flask.palletsprojects.com/',
        'image_url': 'https://via.placeholder.com/100'
    },
    {
        'topic': 'Python',
        'summary': 'Python is a programming language that lets you work quickly and integrate systems more effectively.',
        'link': 'https://www.python.org/',
        'image_url': 'https://via.placeholder.com/100'
    },
    {
        'topic': 'JavaScript',
        'summary': 'JavaScript is a programming language that is one of the core technologies of the World Wide Web.',
        'link': 'https://www.javascript.com/',
        'image_url': 'https://via.placeholder.com/100'
    },
]

# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="Unsearch/1.0 (https://yourwebsite.com; contact@example.com)"
)

# Function to get images from Unsplash based on a topic
def get_image(topic):
    access_key = 'y_qPxDuIBajo0KxWstx0wK4RAJDoVghcAoG-k4rrQWo'  # Replace with your Unsplash API access key
    url = f"https://api.unsplash.com/search/photos?query={topic}&client_id={access_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['small']  # Return URL of the first image
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image for '{topic}': {e}")
    return None

# Function to get a summary from Wikipedia for a random topic
def get_wikipedia_summary(topic):
    try:
        page = wiki.page(topic)
        if page.exists():
            return page.summary[:300], page.fullurl  # Return summary and link
    except Exception as e:
        print(f"Error fetching Wikipedia summary for '{topic}': {e}")
    return None, None

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/styles.css")
def css():
    return send_from_directory("static","styles.css")

# Route to handle the search form
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].lower()

    # Select random topics to display as "unrelated results"
    topics = random.sample(random_topics, 1)
    results = []

    for topic in topics:
        # Fetch image and Wikipedia summary for each topic
        image_url = get_image(topic)
        summary, link = get_wikipedia_summary(topic)
        
        if summary:  # Only add to results if summary is available
            results.append({
                'topic': topic.capitalize(),
                'image_url': image_url,
                'summary': summary,
                'link': link
            })
    print(results)
    # Render the results to the template
    return render_template('results.html', query=query, results=results)

@app.route("/index2")
def index2():    
    return render_template('index2.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form.get('query')
    
    # For demonstration, we are filtering results based on the query
    filtered_results = [data for data in dummy_data if query.lower() in data['topic'].lower()]
    return render_template('results.html', query=query, results=filtered_results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
