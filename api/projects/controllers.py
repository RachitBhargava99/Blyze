from sqlalchemy.orm import Session

from typing import List, Union

from db import models, schemas


def get_project_by_name(db: Session, name: str) -> Union[models.Project, None]:
    return db.query(models.Project).filter_by(name=name).first()


def get_project_by_id(db: Session, project_id: int) -> Union[models.Project, None]:
    return db.query(models.Project).filter_by(id=project_id).first()


def delete_project_by_id(db: Session, project_id: int) -> None:
    db.query(models.Project).filter_by(id=project_id).delete()
    db.commit()


def change_project_info(db: Session, project_id: int, new_project_info: schemas.ProjectEdit) -> Union[
    models.Project, None]:
    project_to_edit = get_project_by_id(db, project_id)
    if project_to_edit is None:
        return None
    project_to_edit.name = new_project_info.name
    project_to_edit.base_location = new_project_info.base_location
    db.commit()
    db.refresh(project_to_edit)
    return project_to_edit


def create_project(db: Session, project_info: schemas.ProjectCreate) -> models.Project:
    db_project = models.Project(name=project_info.name, location=project_info.base_location)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def add_org_to_project(db: Session, project_id: int, org_id: int) -> models.Project_Membership:
    db_org_membership = models.Project_Membership(project_id=project_id, org_id=org_id)
    db.add(db_org_membership)
    db.commit()
    db.refresh(db_org_membership)
    return db_org_membership


def remove_org_from_project(db: Session, project_id: int, org_id: int) -> None:
    db.query(models.Project_Membership).filter_by(project_id=project_id, org_id=org_id).delete()


def is_org_in_project(db: Session, project_id: int, org_id: int) -> bool:
    return db.query(models.Project_Membership).filter_by(project_id=project_id, org_id=org_id).first() is not None


def get_all_orgs_in_project(db: Session, project_id: int) -> List[models.Organization]:
    return [db.query(models.Organization).filter_by(id=x.org_id).first() for x in
            db.query(models.Project_Membership).filter_by(project_id=project_id)]
