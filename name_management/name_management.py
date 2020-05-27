import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "namedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Name(db.Model):
    first_name = db.Column(db.String(80), unique=True,
                           nullable=False, primary_key=True)

    def __repr__(self):
        return "<Name: {}>".format(self.first_name)


@app.route('/', methods=["GET", "POST"])
def home():
    duplicate = False
    names = None
    if request.form:
        try:
            name = Name(first_name=request.form.get("name"))
            indexed_name = Name.query.filter_by(
                first_name=name.first_name).first()
            if indexed_name is not None:
                duplicate = True
            else:
                db.session.add(name)
                db.session.commit()
        except Exception as e:
            print("Failed to add name")
            print(e)
    names = Name.query.all()
    return render_template("home.html", names=names, duplicate=duplicate)


@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        name = Name.query.filter_by(first_name=oldname).first()
        indexed_name = Name.query.filter_by(first_name=newname).first()

        if indexed_name is None:
            name.first_name = newname
        else:
            db.session.delete(name)
        db.session.commit()
    except Exception as e:
        print("Couldn't update name")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    name = Name.query.filter_by(first_name=name).first()
    db.session.delete(name)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
