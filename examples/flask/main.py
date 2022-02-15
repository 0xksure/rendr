from render import Render
from flask import Flask

app = Flask(__name__)


render = Render(folder="sources")


@app.route("/")
def index():
    return render.go()


if __name__ == '__main__':
    app.run()
