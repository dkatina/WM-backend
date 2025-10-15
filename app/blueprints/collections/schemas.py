from app.extensions import ma
from app.models import Collection

class CollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collection
        include_fk = True


collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True) #handle a list of users