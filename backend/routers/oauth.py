from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, verify_jwt_in_request
)
from flask import Blueprint, jsonify, request
from backend.database.oauth import ClientUserInfo, ClientSecretInfo

oauth_bp = Blueprint('oauth', __name__)


@oauth_bp.route('/client', methods=['POST'])
def client():
    data = request.get_json()
    client_id = data.get('clientId')
    client_secret = data.get('clientSecret')
    if ClientSecretInfo.query.filter_by(client_id=client_id, client_secret=client_secret,is_disable=False).first():
        client_user_info = ClientUserInfo.query.filter_by(client_id=client_id).first()
        user_id = client_user_info.user_id
        access_token = create_access_token(identity=user_id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'code': 401, 'msg': 'client_id or client_secret error'})
