import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from backend.extensions import db
from backend.models.season import Season


class SeasonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Season
        load_instance = True
        sqla_session = db.session
