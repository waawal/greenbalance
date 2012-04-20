from flask import Flask, request
from pprint import pprint
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from 3101"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3101, debug=True)
