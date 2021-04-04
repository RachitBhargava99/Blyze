from sqlalchemy.orm import Session

from typing import List

from db import models, schemas


def get_organization_by_id(db: Session, org_id: int) -> schemas.Organization:
    return db.query(models.Organization).filter_by(id=org_id).first()


def get_organization_by_name(db: Session, name: str) -> schemas.Organization:
    return db.query(models.Organization).filter_by(name=name).first()


def create_org_through_user(db: Session, name: str, user_id: int) -> schemas.Organization:
    db_org = create_org(db, name, user_id)
    add_user_to_org(db, db_org.id, user_id)
    return db_org


def create_org(db: Session, name: str, user_id: int) -> schemas.Organization:
    db_org = models.Organization(name=name, creator_id=user_id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def add_user_to_org(db: Session, org_id: int, user_id: int) -> schemas.User:
    db_user = db.query(models.User).filter_by(id=user_id).first()
    db_user.organization_id = org_id
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user_from_org(db: Session, user_id: int) -> schemas.User:
    db_user = db.query(models.User).filter_by(id=user_id).first()
    db_user.organization_id = None
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_org_by_id(db: Session, org_id: int) -> None:
    db.query(models.Organization).filter_by(id=org_id).delete()
    db.commit()


def get_users_by_org_id(db: Session, org_id: int) -> List[schemas.User]:
    return [x for x in db.query(models.User).filter_by(id=org_id)]
