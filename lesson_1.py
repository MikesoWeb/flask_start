from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    name = 'Mike'
    return f'<h1>Hello, {name}</h1>'





if __name__ == '__main__':
    app.run(debug=1, port=8000)
