from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # attach CORS to the entire app

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/entries', methods=['GET'])
def get_entries():
    entries = DiaryEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    new_entry = DiaryEntry(content=data['content'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

@app.route('/entries/<int:id>', methods=['PUT'])
def update_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    data = request.get_json()
    entry.content = data['content']
    db.session.commit()
    return jsonify(entry.to_dict())

@app.route('/entries/<int:id>', methods=['DELETE'])
def delete_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Entry deleted'})

if __name__ == '__main__':
    with app.app_context():  # アプリケーションコンテキストを設定
        db.create_all()  # create database
        app.run(debug=True)  # ローカル開発サーバーを起動
