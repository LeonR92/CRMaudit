from flask import Flask
from crm.app import crm

app = Flask(__name__)

app.register_blueprint(crm, url_prefix="/crm")


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
