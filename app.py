from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Вставил, потому что слишком нагружает систему
                                               # (судя по warning-у)
db = SQLAlchemy(app)
Bootstrap(app)

if __name__ == "__main__":

    # Need to make sure Flask knows about its views before we run
    # the app, so we import them. We could do it earlier, but there's
    # a risk that we may run into circular dependencies, so I do it at the
    # last minute here.

    from views import *

    app.run(debug=True)
