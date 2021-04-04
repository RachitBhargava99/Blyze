from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import get_project_by_id, get_project_by_name, create_project, change_project_info, \
    delete_project_by_id, add_org_to_project, is_org_in_project, get_all_orgs_in_project
from api.orgs.controllers import get_organization_by_id
from api.users.controllers import get_user_by_id
from etc.decorators import login_required
from etc.fastapi_dependencies import get_user_id

router = APIRouter()


@router.put('', response_model=schemas.Project)
@login_required
def create_project_route(project: schemas.ProjectCreate, request: Request, user_id: int = Depends(get_user_id),
                         db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if get_project_by_name(db, project.name) is not None:
        raise HTTPException(409, "Project with the provided name already exists")
    db_project = create_project(db, project)
    add_org_to_project(db, db_project.id, user.organization_id)
    return db_project


@router.delete('/{projectId}', response_model=schemas.Project)
@login_required
def delete_project(projectId: int, request: Request, user_id: int = Depends(get_user_id),
                   db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to be able to delete it.")
    delete_project_by_id(db, projectId)
    return db_project


@router.get('/{projectId}', response_model=schemas.Project)
@login_required
def get_project_info(projectId: int, request: Request, user_id: int = Depends(get_user_id),
                     db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to be able to delete it.")
    return db_project


@router.patch('/{projectId}', response_model=schemas.Project)
@login_required
def change_project_info_route(projectId: int, project: schemas.ProjectEdit, request: Request,
                              user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to perform this operation.")
    return change_project_info(db, projectId, project)


@router.put('/{projectId}/orgs/{orgId}', response_model=schemas.Project)
@login_required
def add_project_org(projectId: int, orgId: int, request: Request, user_id: int = Depends(get_user_id),
                    db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if get_organization_by_id(db, orgId) is None:
        raise HTTPException(404, "The request organization could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to perform this operation.")
    if is_org_in_project(db, db_project.id, orgId):
        raise HTTPException(409, "The organization is already a part of the given project.")
    add_org_to_project(db, projectId, orgId)
    return db_project


@router.delete('/{projectId}/orgs/{orgId}', response_model=schemas.Project)
@login_required
def remove_project_org(projectId: int, orgId: int, request: Request, user_id: int = Depends(get_user_id),
                       db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if get_organization_by_id(db, orgId) is None:
        raise HTTPException(404, "The request organization could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to perform this operation.")
    if not is_org_in_project(db, db_project.id, orgId):
        raise HTTPException(422, "The organization is not already a part of the given project.")
    add_org_to_project(db, projectId, orgId)
    return db_project


@router.get('/{projectId}/orgs', response_model=schemas.OrganizationList)
@login_required
def get_project_org_list(projectId: int, request: Request, user_id: int = Depends(get_user_id),
                         db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    db_project = get_project_by_id(db, projectId)
    if db_project is None:
        raise HTTPException(404, "The requested project could not be found.")
    if not is_org_in_project(db, db_project.id, user.organization_id):
        raise HTTPException(401, "You must be in the organization handling the project to perform this operation.")
    org_list = get_all_orgs_in_project(db, projectId)
    return {'orgs': org_list}
