from flask import Flask

app = Flask(__name__)

content = "Hello World!"

@app.route("/")
def hello():
    global content
    copy = content
    content = """
    <script src="new_stuff"></script>
    test
    """
    return copy

@app.route("/new_stuff")
def new_stuff():
    return "Extra stuff here."
