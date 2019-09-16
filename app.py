from flask import Flask

site = Flask(__name__)

@site.route('/')
def home():
    return "Hello There!"


if __name__ == "__main__":
    site.run(host='0.0.0.0')