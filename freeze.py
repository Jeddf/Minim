from flask_frozen import Freezer
from Minim import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
