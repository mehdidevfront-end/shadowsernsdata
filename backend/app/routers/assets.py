from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..storage import list_assets, save_assets

router = APIRouter(prefix='/assets', tags=['assets'])


class Asset(BaseModel):
    id: str
    name: Optional[str]
    type: Optional[str]
    bu: Optional[str]
    env: Optional[str]
    criticite: Optional[str]


@router.get('/', response_model=List[Asset])
def get_assets():
    return list_assets()


@router.get('/{asset_id}', response_model=Asset)
def get_asset(asset_id: str):
    items = list_assets()
    for it in items:
        if it.get('id') == asset_id:
            return it
    raise HTTPException(status_code=404, detail='not found')


@router.post('/', response_model=Asset)
def create_asset(a: Asset):
    items = list_assets()
    if any(it.get('id') == a.id for it in items):
        raise HTTPException(status_code=400, detail='id exists')
    items.append(a.dict())
    save_assets(items)
    return a.dict()


@router.put('/{asset_id}', response_model=Asset)
def update_asset(asset_id: str, a: Asset):
    items = list_assets()
    for i, it in enumerate(items):
        if it.get('id') == asset_id:
            items[i] = a.dict()
            save_assets(items)
            return a.dict()
    raise HTTPException(status_code=404, detail='not found')
