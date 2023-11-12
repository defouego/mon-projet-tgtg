from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monprojet.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_cors import CORS

# After creating the Flask app instance
CORS(app)


class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(128))

with app.app_context():
    db.create_all()

@app.route('/inscription', methods=['POST'])
def inscription():
    email = request.json['email']
    mot_de_passe = request.json['mot_de_passe']
    mot_de_passe_hash = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
    nouvel_utilisateur = Utilisateur(email=email, mot_de_passe_hash=mot_de_passe_hash)
    db.session.add(nouvel_utilisateur)
    db.session.commit()
    return jsonify({"message": "Utilisateur créé avec succès"}), 201

@app.route('/authentification', methods=['POST'])
def authentification():
    email = request.json['email']
    mot_de_passe = request.json['mot_de_passe']
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe_hash, mot_de_passe):
        return jsonify({"message": "Authentification réussie"}), 200
    return jsonify({"message": "Échec de l'authentification"}), 401

if __name__ == '__main__':
    app.run(debug=True)
