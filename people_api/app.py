from os import path
import sys
from flask import render_template
from people_api.config import *
from people_api.models import Person
from people_api.constants import PEOPLE_DATABASE_URI

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

app = create_app(PEOPLE_DATABASE_URI)

@app.route('/')
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

