from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import get_organization_by_name, create_org_through_user, get_organization_by_id, delete_org_by_id, \
    get_users_by_org_id, add_user_to_org
from etc.decorators import login_required
from etc.fastapi_dependencies import get_user_id

router = APIRouter()


@router.put('', response_model=schemas.Organization)
@login_required
def create_organization(org: schemas.OrganizationCreate, request: Request, user_id: int = Depends(get_user_id),
                        db: Session = Depends(get_db)):
    if get_organization_by_name(db, org.name) is not None:
        raise HTTPException(status_code=409, detail="Organization with the provided name already exists")
    db_org = create_org_through_user(db, org.name, user_id)
    return db_org


@router.delete('/{orgId}', response_model=schemas.Organization)
@login_required
def delete_organization(orgId: int, request: Request, user_id: int = Depends(get_user_id),
                        db: Session = Depends(get_db)):
    db_org = get_organization_by_id(db, orgId)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Requested organization not found")
    if db_org.owner_id != user_id:
        raise HTTPException(status_code=401, detail="Non-owners not allowed to delete organization")
    delete_org_by_id(db, orgId)
    return db_org


@router.put('/{orgId}/add/{newUserId}', response_model=schemas.Organization)
def add_user_to_organization(orgId: int, newUserId: int, request: Request, user_id: int = Depends(get_user_id),
                             db: Session = Depends(get_db)):
    db_org = get_organization_by_id(db, orgId)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Requested organization not found")
    if db_org.owner_id != user_id:
        raise HTTPException(status_code=401, detail="Non-owners not allowed to perform this operation")
    org_user_ids = [x.id for x in get_users_by_org_id(db, orgId)]
    if newUserId in org_user_ids:
        raise HTTPException(status_code=409, detail="The user is already a member of this organization.")
    add_user_to_org(db, orgId, newUserId)
    return db_org


@router.delete('/{orgId}/add/{newUserId}', response_model=schemas.Organization)
def remove_user_from_organization(orgId: int, newUserId: int, request: Request, user_id: int = Depends(get_user_id),
                                  db: Session = Depends(get_db)):
    db_org = get_organization_by_id(db, orgId)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Requested organization not found")
    if db_org.owner_id != user_id:
        raise HTTPException(status_code=401, detail="Non-owners not allowed to perform this operation")
    org_user_ids = [x.id for x in get_users_by_org_id(db, orgId)]
    if newUserId not in org_user_ids:
        raise HTTPException(status_code=404, detail="The user must already be a member of this organization.")
    remove_user_from_organization(db, newUserId)
    return db_org


@router.get('/{orgId}/users', response_model=schemas.UserList)
def get_org_users(orgId: int, request: Request, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    db_org = get_organization_by_id(db, orgId)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Requested organization not found")
    org_users = get_users_by_org_id(db, orgId)
    org_user_ids = [x.id for x in org_users]
    if user_id not in org_user_ids:
        raise HTTPException(status_code=401, detail="Non-members not allowed to perform this operation")
    return {'users': org_users}
