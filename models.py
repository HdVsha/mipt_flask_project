from app import db
from sqlalchemy.orm import class_mapper, ColumnProperty

'''

Positions of classes actually play role here

'''

# Creating an assisting table Role for Many To Many relation

association_table = db.Table('Role', db.metadata,
                             db.Column('person_uid', db.ForeignKey('Person.uid'), primary_key=True),
                             db.Column('film_uid', db.ForeignKey('Film.uid'), primary_key=True),
                             db.Column("name", db.String(50)),
                             )


class Country(db.Model):
    __tablename__ = "Country"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    people = db.relationship("Person", backref="country_of_birth")
    films = db.relationship("Film", backref="country_films")


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
    films = db.relationship("Film",
                            secondary=association_table)

    def __init__(self, firstname, username):
        self.firstname = firstname
        self.username = username

    def __str__(self):
        return f"{self.firstname}"


def create_person(person_name, person_username):
    person = Person(person_name, person_username)
    db.session.add(person)
    db.session.commit()
    print(person)
    return person


class Film(db.Model):
    __tablename__ = "Film"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    country_id = db.Column(db.Integer, db.ForeignKey("Country.uid"))
    birth = db.Column(db.Date)
    description = db.Column(db.String(150))

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