from flask import Flask, render_template, request
from mrs import recommend

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    if request.method == 'POST':
        searched_movie = request.form['movieInput']
        recommendations = recommend(searched_movie)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)