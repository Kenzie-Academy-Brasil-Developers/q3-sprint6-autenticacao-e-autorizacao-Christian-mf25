from secrets import token_urlsafe
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.models.user_model import UsersModel
from app.configs.database import db
from app.configs.auth import auth


def create_user():
	data = request.get_json()
	data_keys = data.keys()
	UsersModel.right_key(data_keys)

	try:
		data["name"] = data["name"].title()
		data["last_name"] = data["last_name"].title()
		data["api_key"] = token_urlsafe(16)
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

	return jsonify({"api_key": user.api_key})

@auth.login_required
def get_users():
	user = auth.current_user()

	return jsonify(user), 200


@auth.login_required
def update_user():
	data = request.get_json()
	data_keys = data.keys()
	UsersModel.right_key(data_keys)

	data["name"] = data["name"].title()
	data["last_name"] = data["last_name"].title()

	user = auth.current_user()

	for key, value in data.items():
		setattr(user, key, value)

	db.session.add(user)
	db.session.commit()

	return jsonify(user), 200

@auth.login_required
def delete_user():
	user_to_delete = auth.current_user()
	user = user_to_delete.name
	
	db.session.delete(user_to_delete)
	db.session.commit()

	return {"msg": f"User {user} has been deleted."}