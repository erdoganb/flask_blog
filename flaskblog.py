from flask import Flask
app = Flask(__name__)


#home page
@app.route("/")
@app.route("/home")
def hello():
    return "<h2>Hello World...</h2>"

#about page
@app.route("/about")
def about():
    return "<h2>About Page</h2>"



if __name__ == '__main__':
    app.run(debug=True)