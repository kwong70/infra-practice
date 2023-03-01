from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_host = "database-2.chk1uu9qegvf.us-east-1.rds.amazonaws.com"
db_port = 5432
db_name = "postgres"
db_user = "postgres"
db_password = "password"
app.config['SQLALCHEMY_DATABASE_URI'] = f'posgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db = SQLAlchemy(app)    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, age):
        self.name = name
        self.age = age

@app.route('/healthy', methods=['GET'])
def healthy(): 
    return {"status_code": 200}

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    age = request.json['age']

    user = User(name, age)
    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User created'})
    response.status_code = 201
    return response

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [{'name': user.name, 'age': user.age} for user in users]})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return jsonify({'name': user.name, 'age': user.age})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        user.name = request.json['name']
        user.age = request.json['age']
        db.session.commit()
        return jsonify({'message': 'User updated'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
