import typing
try:
    import strawberry
except Exception:
    strawberry = None

from .storage import list_assets, list_risks


if strawberry:
    @strawberry.type
    class AssetType:
        id: str
        name: typing.Optional[str]
        type: typing.Optional[str]
        bu: typing.Optional[str]
        env: typing.Optional[str]
        criticite: typing.Optional[str]

    @strawberry.type
    class RiskType:
        id: str
        title: typing.Optional[str]
        severity: typing.Optional[str]
        asset_id: typing.Optional[str]
        description: typing.Optional[str]

    @strawberry.type
    class Query:
        @strawberry.field
        def assets(self) -> typing.List[AssetType]:
            data = list_assets()
            return [AssetType(**d) for d in data]

        @strawberry.field
        def risks(self) -> typing.List[RiskType]:
            data = list_risks()
            return [RiskType(**d) for d in data]

    schema = strawberry.Schema(Query)
else:
    schema = None
