from app.models import *
from app.subcriber import *
from app.urls import *
from app import app

if __name__ == "__main__":
    with app.app_context():
        app.run()