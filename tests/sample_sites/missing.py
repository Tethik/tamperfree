from flask import Flask

app = Flask(__name__)

content = """
<script src="new_stuff">Look, new stuff.</script>
test
"""

@app.route("/")
def hello():
    global content
    copy = content
    content = "Hello World!"
    return copy

@app.route("/new_stuff")
def new_stuff():
    return "Extra stuff here."

if __name__ == "__main__":
    app.run()
