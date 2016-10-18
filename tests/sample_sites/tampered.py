from flask import Flask

app = Flask(__name__)

content = "Hello World!"

@app.route("/")
def hello():
    global content
    copy = content
    content = """
    test
    """
    return copy
