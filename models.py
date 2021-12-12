from app import db
from sqlalchemy.orm import class_mapper, ColumnProperty

'''

Positions of classes actually play role here

'''

# Creating an assisting table Role for Many To Many relation


class Role(db.Model):
    __tablename__ = "Role"
    person_id = db.Column(db.ForeignKey('Person.uid'), primary_key=True)
    film_id = db.Column(db.ForeignKey('Film.uid'), primary_key=True)
    role = db.Column(db.String(50))
    person = db.relationship("Person", back_populates="films")
    film = db.relationship("Film", back_populates="people")


class Country(db.Model):
    __tablename__ = "Country"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    people = db.relationship("Person", backref="country_of_birth")
    films = db.relationship("Film", backref="country_films")


def create_country(name):
    country = Country(name=name)
    db.session.add(country)
    db.session.commit()

    return country

class Person(db.Model):
    __tablename__ = "Person"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    country_of_birth_id = db.Column(db.Integer, db.ForeignKey("Country.uid"))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    birth = db.Column(db.Date)
    films = db.relationship("Role", back_populates="person")

    def __init__(self, firstname, lastname, username=None, email=None, birth=None, country_id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.birth = birth
        self.country_of_birth_id = country_id

    def __str__(self):
        return f"{self.firstname}"

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]


def create_person(person_name, lastname, username=None, email=None, birth=None, country_of_birth_id=None):
    person = Person(person_name, lastname, username, email, birth, country_of_birth_id)
    db.session.add(person)
    db.session.commit()

    return person


def create_film(**kwargs):
    film = Film(**kwargs)
    db.session.add(film)
    db.session.commit()
    return film


class Film(db.Model):
    __tablename__ = "Film"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    country_id = db.Column(db.Integer, db.ForeignKey("Country.uid"))
    birth = db.Column(db.Date)
    description = db.Column(db.String(150))
    people = db.relationship("Role", back_populates="film")

    def __str__(self):
        return f"{self.name}"

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]


if __name__ == "__main__":
    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")

# from models import Person, Role, Film
# p = Person(firstname="Test2", username="Test2")
# f = Film(name="Test2")
# r = Role(role="Director")
# r.film = f
# p.films.append(r)
# from app import db