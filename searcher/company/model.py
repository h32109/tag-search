from sqlalchemy import (
    Integer,
    Column,
    String,
    ForeignKey,
    Table,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship

from searcher.globals import Base

company_tag = Table(
    'company_tag', Base.metadata,
    Column('company_id', Integer, ForeignKey('company.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag_name.id'), primary_key=True)
)


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    names = relationship("CompanyName")
    tags = relationship("TagName", secondary=company_tag)


class CompanyName(Base):
    __tablename__ = 'company_name'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'))
    language = Column(String(2), nullable=False)
    name = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('company_id', 'language', 'name', name='uq_company_language_name'),
        Index('ix_company_name_name', name)
    )


class TagName(Base):
    __tablename__ = 'tag_name'

    id = Column(Integer, primary_key=True)
    language = Column(String(2), nullable=False)
    name = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('language', 'name', name='uq_language_name'),
        Index('ix_tag_name_name', name)
    )