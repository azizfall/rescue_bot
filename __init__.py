from flask import Flask 

app = Flask(__name__)

@app.route('/')
def homepage():
        return "HI MAN HERRO" 

if __name__ == "__main__": 
        app.run()

