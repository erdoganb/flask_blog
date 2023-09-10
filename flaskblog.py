from flask import Flask, render_template
import json

app = Flask(__name__)

# Function to parse JSON file
def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Parse the JSON file at application startup
json_data = parse_json_file('static/blog_posts.json')

#home page
@app.route("/")
@app.route("/home")
def hello():
    posts = json_data  # Access the parsed JSON data
    return render_template('home.html', title="home", posts=posts)

#about page
@app.route("/about")
def about():
    return render_template('about.html', title="about")

if __name__ == '__main__':
    app.run(debug=False)