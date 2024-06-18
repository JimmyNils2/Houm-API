from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db_setup import Base
from .mixins import Timestamp



class Visit(Timestamp, Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    visit_date = Column(DateTime(timezone=True), nullable=False, index=True)
    comment = Column(Text, nullable=True)

    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="visits")
    property = relationship("Property", back_populates="visits")