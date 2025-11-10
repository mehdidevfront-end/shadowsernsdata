from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..storage import list_risks, save_risks

router = APIRouter(prefix='/risks', tags=['risks'])


class Risk(BaseModel):
    id: str
    title: Optional[str]
    severity: Optional[str]
    asset_id: Optional[str]
    description: Optional[str]


@router.get('/', response_model=List[Risk])
def get_risks():
    return list_risks()


@router.get('/{risk_id}', response_model=Risk)
def get_risk(risk_id: str):
    items = list_risks()
    for it in items:
        if it.get('id') == risk_id:
            return it
    raise HTTPException(status_code=404, detail='not found')


@router.post('/', response_model=Risk)
def create_risk(r: Risk):
    items = list_risks()
    if any(it.get('id') == r.id for it in items):
        raise HTTPException(status_code=400, detail='id exists')
    items.append(r.dict())
    save_risks(items)
    return r.dict()


@router.put('/{risk_id}', response_model=Risk)
def update_risk(risk_id: str, r: Risk):
    items = list_risks()
    for i, it in enumerate(items):
        if it.get('id') == risk_id:
            items[i] = r.dict()
            save_risks(items)
            return r.dict()
    raise HTTPException(status_code=404, detail='not found')
