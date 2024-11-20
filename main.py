from flask import Flask


app = Flask("__main__")


@app.route("/")
def home():
    return "I hate my life"

if __name__ == "__main__":
    app.run()