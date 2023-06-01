from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    variable = request.form['variable']
    return f"The variable you entered is: {variable}"

if __name__ == '__main__':
    app.run(debug=True)