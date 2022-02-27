from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from app.models.user_model import UsersModel
from app.configs.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def create_user():
	data = request.get_json()
	data_keys = data.keys()
	UsersModel.right_key(data_keys)

	try:
		data["name"] = data["name"].title()
		data["last_name"] = data["last_name"].title()
		user = UsersModel(**data)

		db.session.add(user)
		db.session.commit()

		return jsonify(user), 201
	
	except IntegrityError as e:
		email = data["email"]
		return jsonify({"error": f"email '{email}' already registered"}), 409


def login_user():
	data  = request.get_json()
	data_keys = data.keys()
	UsersModel.right_key(data_keys)

	user = UsersModel.query.filter_by(email=data["email"]).first()

	if not user:
		return {"error": "Email not found"}, 401

	if not user.check_password(data["password"]):
		return {"error": "Email and password missmatch"}, 401

	
	token = create_access_token(user, expires_delta=timedelta(hours=1))

	return jsonify({"access_token": token})

@jwt_required()
def get_users():
	user = get_jwt_identity()

	return jsonify(user), 200


@jwt_required()
def update_user():
	data = request.get_json()
	data_keys = data.keys()
	UsersModel.right_key(data_keys)

	data["name"] = data["name"].title()
	data["last_name"] = data["last_name"].title()

	try:
		user_to_update = get_jwt_identity()
		user_email = user_to_update["email"]
		user = UsersModel.query.filter_by(email=user_email).first()

		for key, value in data.items():
			setattr(user, key, value)

		db.session.add(user)
		db.session.commit()
	
	except IntegrityError as e:
		email = data["email"]
		return jsonify({"error": f"email '{email}' already registered"}), 409

	return jsonify(user), 200

@jwt_required()
def delete_user():
	user = get_jwt_identity()
	user_email = user["email"]
	user_to_delete = UsersModel.query.filter_by(email=user_email).first()

	user = user_to_delete.name
	
	db.session.delete(user_to_delete)
	db.session.commit()

	return {"msg": f"User {user} has been deleted."}