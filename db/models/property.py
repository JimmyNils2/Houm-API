from sqlalchemy import Column, Integer, String, DECIMAL,Text
from sqlalchemy.orm import relationship
from ..db_setup import Base
from .mixins import Timestamp



class Property(Timestamp, Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(200), nullable=False, index=True, unique=True)
    location = Column(String(200), nullable=False)
    price = Column(DECIMAL(10,2), nullable=True, default=10)
    description = Column(Text, nullable=True)

    # Relationships
    visits = relationship("Visit", back_populates="property")