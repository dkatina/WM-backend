from app.extensions import ma
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True) #handle a list of users
login_schema = UserSchema(exclude=['role', 'spotify_id', 'id'])