from app import app
import datetime
from flask import render_template, request
from models import create_person, create_film, create_country
from models import Film, Person, Country, Person_Film_Role, Role


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/person/add/', methods=['GET', 'POST'])
def person_add():
    if request.method == 'GET':
        return render_template('person_add.html')

    person_firstname_lastname = request.form.get('person_firstname_field')
    person_birth = request.form.get('person_birth_field')
    fields = {
        "firstname_lastname": person_firstname_lastname,
        "birth": person_birth
    }
    person = create_person(**fields)

    return render_template('person_add.html', person=person)


@app.route('/film/add/', methods=['GET', 'POST'])
def film_add():
    if request.method == 'GET':
        return render_template('film_add.html')

    film_name = request.form.get('film_name_field')
    film_birth = request.form.get('film_birth_field')
    film_description = request.form.get('film_description_field')
    film = {
        "name": film_name,
        "birth": int(film_birth),
        "description": film_description,
    }
    film = create_film(**film)

    return render_template('film_add.html', film=film)


@app.route('/films/', methods=["GET"])
def films():
    films = Film.query.order_by("uid").all()

    return render_template("films.html", films=films, obj=Film())


@app.route('/films/<int:uid>/', methods=["GET"])
def film(uid):
    film = Film.query.filter_by(uid=uid).first()
    if film:
        roles = Person_Film_Role.query.filter_by(film_id=uid)
        relations = []
        for role in roles:
            relations.append([Role.query.filter_by(uid=role.role_id).first(), Person.query.filter_by(uid=role.person_id).first()])
        return render_template("film.html", film=film, relations=relations)
    return '<p>This film does not exist</p>'


@app.route('/people/', methods=["GET"])
def people():
    people = Person.query.order_by("uid").all()
    # Can create an obj of class bc without transaction to db it won't get into db
    return render_template("people.html", people=people, obj=Person(firstname_lastname="Tmp"))


@app.route('/people/<int:uid>/', methods=["GET"])
def person(uid):
    person = Person.query.filter_by(uid=uid).first()
    if person:
        roles = Person_Film_Role.query.filter_by(person_id=uid)
        relations = []
        for role in roles:
            relations.append(
                [Role.query.filter_by(uid=role.role_id).first(), Film.query.filter_by(uid=role.film_id).first()])
        return render_template("person.html", person=person, relations=relations)
    return '<p>This person does not exist</p>'
