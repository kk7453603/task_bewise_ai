from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import requests
app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bd_admin:secret_key@db/Question_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель для сохранения вопросов
class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    answer = Column(String)
    created_at = Column(DateTime, default=datetime.now)


# Создание таблицы в базе данных
with app.app_context():
    db.create_all()


@app.route('/questions/', methods=['POST'])
def create_questions():
    data = request.get_json()
    questions_to_save = data['questions_num']

    saved_questions = Question.query.count()

    while questions_to_save > 0:
        response = requests.get("https://jservice.io/api/random")
        question_data = response.json()[0]

        # Проверка на уникальность
        if not Question.query.filter_by(text=question_data["question"]).first():
            question = Question(
                text=question_data["question"],
                answer=question_data["answer"]
            )
            db.session.add(question)
            db.session.commit()
            questions_to_save -= 1

    return jsonify(message=f"Saved {data['questions_num']} questions")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
