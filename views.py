from app import app

from flask import render_template, request
from models import create_person
from models import Film, Person


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')

    person_name = request.form.get('firstname_field')
    person_username = request.form.get('person_username_field')

    create_person(person_name, person_username)

    return render_template('add.html')


@app.route('/films/', methods=["GET"])
def films():
    films = Film.query.order_by("uid").all()

    return render_template("films.html", films=films, obj=Film())


@app.route('/films/<int:uid>/', methods=["GET"])
def film(uid):
    film = Film.query.filter_by(uid=uid).first()
    if film:
        return render_template("film.html", film=film)
    return '<p>This film does not exist</p>'


@app.route('/people/', methods=["GET"])
def people():
    people = Person.query.order_by("uid").all()
    # Can create an obj of class bc without transaction to db it won't get into db
    return render_template("people.html", people=people, obj=Person(firstname="Temp", username="Temp"))


@app.route('/people/<int:uid>/', methods=["GET"])
def person(uid):
    person = Person.query.filter_by(uid=uid).first()
    if person:
        return render_template("person.html", person=person)
    return '<p>This person does not exist</p>'
