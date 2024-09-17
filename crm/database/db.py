from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import event

Base = declarative_base()

# BD_versicherungsunternehmen model
class BDVersicherungsunternehmen(Base):
    __tablename__ = 'bd_versicherungsunternehmen'
    id = Column(Integer, primary_key=True)
    mandantkuerzel = Column(String(10), nullable=False)
    mandantenname = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('bd_versicherungsunternehmen.id'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    @classmethod
    def add_company(cls, session, mandantkuerzel, mandantenname, parent_name=None):
        parent = session.query(cls).filter_by(mandantenname=parent_name).first()
        new_company = cls(
            mandantkuerzel=mandantkuerzel,
            mandantenname=mandantenname,
            parent_id=parent.id if parent else None
        )
        session.add(new_company)
        session.commit()
        return new_company

# Kontaktperson model
class Kontaktperson(Base):
    __tablename__ = 'kontaktperson'
    id = Column(Integer, primary_key=True)
    versicherungsunternehmen_id = Column(Integer, ForeignKey('bd_versicherungsunternehmen.id'))
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# BDVersicherungsunternehmenAudit model
class BDVersicherungsunternehmenAudit(Base):
    __tablename__ = 'bd_versicherungsunternehmen_audit'
    id = Column(Integer, primary_key=True)
    versicherungsunternehmen_id = Column(Integer)  # Link to original company table
    mandantkuerzel = Column(String(10), nullable=False)
    mandantenname = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('bd_versicherungsunternehmen.id'))
    operation_type = Column(String(10))  # 'INSERT', 'UPDATE', or 'DELETE'
    changed_at = Column(TIMESTAMP, default=datetime.utcnow)

# Set up engine and session
DATABASE_URL = "postgresql+psycopg2://postgres:Leon9999@localhost/CRM"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

@event.listens_for(BDVersicherungsunternehmen, 'before_update')
def log_update(mapper, connection, target):
    try:
        audit_entry = BDVersicherungsunternehmenAudit(
            versicherungsunternehmen_id=target.id,
            mandantkuerzel=target.mandantkuerzel,
            mandantenname=target.mandantenname,
            parent_id=target.parent_id,
            operation_type='UPDATE'
        )
        session.add(audit_entry)
    except Exception as e:
        session.rollback()
        raise

@event.listens_for(BDVersicherungsunternehmen, 'before_delete')
def log_delete(mapper, connection, target):
    try:
        audit_entry = BDVersicherungsunternehmenAudit(
            versicherungsunternehmen_id=target.id,
            mandantkuerzel=target.mandantkuerzel,
            mandantenname=target.mandantenname,
            parent_id=target.parent_id,
            operation_type='DELETE'
        )
        session.add(audit_entry)
    except Exception as e:
        session.rollback()
        raise


