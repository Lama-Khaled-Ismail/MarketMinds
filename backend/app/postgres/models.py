from postgres.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String 
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "user"
   
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    
    # Relationships
    brands = relationship("Brand", back_populates="user", cascade="all, delete-orphan") # bi-directional
    
class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"),nullable=False)
    name = Column(String, nullable=False, unique=True)
    
    
    
    # Relationships 
    user = relationship("User", back_populates="brands")     # one to many
    alt_names = relationship("Altname",back_populates="brand", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="brand", cascade="all, delete-orphan")


class Altname(Base):
    __tablename__ = "altname"
    id = Column(Integer, primary_key=True, nullable=False)
    brand_id = Column(Integer, ForeignKey("brand.id", ondelete="CASCADE"),nullable=False)
    altname = Column(String, nullable=False, unique=True)
    
    # Relationships
    brand = relationship("Brand", back_populates="alt_names")
    
    
class Analysis(Base):
    __tablename__ = "analysis"
    
    id = Column(Integer, primary_key=True, nullable=False)
    brand_id = Column(Integer, ForeignKey("brand.id", ondelete="CASCADE"),nullable=False)
    positive = Column(Integer, nullable=False)
    negative = Column(Integer, nullable=False)
    num_reviews = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    platform = Column(String, nullable=False)
    language = Column(String, nullable=False)
    
    # Relationships
    brand = relationship('Brand', back_populates="analyses")
    reviews = relationship("Review", back_populates="analysis", cascade="all, delete-orphan")

    
class Review(Base):
    __tablename__ = "review"
    
    id = Column(Integer, primary_key=True, nullable=False)
    analysis_id = Column(Integer, ForeignKey("analysis.id", ondelete="CASCADE"),nullable=False)
    text = Column(String, nullable=False)
    score = Column(Boolean, nullable=False)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="reviews")
    
    

    
    
