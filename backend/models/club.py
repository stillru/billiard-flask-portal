from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.extensions import db

"""
Clubs representation
"""


class Club(db.Model):
    id = Column(Integer, primary_key=True)
    """Inucue id of the club"""
    name = Column(String(255), nullable=False)
    """Name of the club"""
    description = Column(Text, nullable=True)
    """Description of the club"""

    def __init__(self, name: str):
        """
        Create a new Club object with the given name.
        """
        self.name = name

    def __repr__(self):
        return f"<Club {self.name}>"
