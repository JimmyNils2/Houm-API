from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Employee(Timestamp, Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    email = Column(EmailType, unique=True, index=True, nullable=False)

    # Relationships
    visits = relationship("Visit", back_populates="employee")
