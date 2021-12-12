from app import app
import datetime
from flask import render_template, request
from models import create_person, create_film, create_country
from models import Film, Person, Country


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/person/add/', methods=['GET', 'POST'])
def person_add():
    countries = Country.query.all()
    if request.method == 'GET':
        return render_template('person_add.html', countries=countries)

    person_name = request.form.get('person_firstname_field')
    person_lastname = request.form.get('person_lastname_field')
    person_email = request.form.get('person_email_field')
    person_birth = request.form.get('person_birth_field')
    person_username = request.form.get('person_username_field')
    person_country = request.form.get('person_country_field')
    if person_birth:
        person_birth = datetime.datetime.strptime(person_birth, '%Y-%m-%d').date()
    person = create_person(person_name, person_lastname, person_username, person_email, person_birth, person_country)

    return render_template('person_add.html', person=person, countries=countries)


@app.route('/film/add/', methods=['GET', 'POST'])
def film_add():
    countries = Country.query.all()
    if request.method == 'GET':
        return render_template('film_add.html', countries=countries)

    film_name = request.form.get('film_name_field')
    film_birth = request.form.get('film_birth_field')
    film_description = request.form.get('film_description_field')
    film_country = request.form.get('film_country_field')
    if film_birth:
        film_birth = datetime.datetime.strptime(film_birth, '%Y-%m-%d').date()
    film = {
        "name": film_name,
        "birth": film_birth,
        "description": film_description,
        "country_id": film_country
    }
    film = create_film(**film)

    return render_template('film_add.html', film=film, countries=countries)


@app.route('/country/add/', methods=['GET', 'POST'])
def country_add():
    if request.method == 'GET':
        return render_template('country_add.html')

    country_name = request.form.get('country_name_field')

    country = create_country(country_name)

    return render_template('country_add.html', country=country)


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
    return render_template("people.html", people=people, obj=Person(firstname="Temp", lastname="Temp"))


@app.route('/people/<int:uid>/', methods=["GET"])
def person(uid):
    person = Person.query.filter_by(uid=uid).first()
    if person:
        return render_template("person.html", person=person)
    return '<p>This person does not exist</p>'
