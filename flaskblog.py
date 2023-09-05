from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'title': 'Blog Post 1',
        'author': 'Albert Einstein',
        'content': 'Photoelectric Effect ...',
        'date_posted': '05 June 1955'
    },{
        'title': 'Blog Post 2',
        'author': 'Enrico Fermi',
        'content': 'Where are the aliens?',
        'date_posted': '18 May 1959'
    }
]


#home page
@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', title="home", posts=posts)

#about page
@app.route("/about")
def about():
    return render_template('about.html', title="about")



if __name__ == '__main__':
    app.run(debug=False)