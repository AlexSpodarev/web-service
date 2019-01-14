from cars_api import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Cars(db.Model):
    __tablename__ = 'cars'
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    Vendor = db.Column(db.Text, nullable=False)
    Model = db.Column(db.Text, nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Engine = db.Column(db.Integer, nullable=False)
    HP = db.Column(db.Integer, nullable=False)
    Torque = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Car: {self.Vendor}>'
