import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# إعداد قاعدة البيانات الدائمة (تخزين آمن على السيرفر لا يتمسح عند إعادة التشغيل)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تصميم جدول المنشورات في قاعدة البيانات
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()  # إنشاء الجدول تلقائياً إذا لم يكن موجوداً

@app.route('/')
def home():
    return "Syrian Social Matrix API with Permanent DB is Live! 🚀"

# جلب المنشورات من قاعدة البيانات الدائمة
@app.route('/api/posts/feed', methods=['GET'])
def get_feed():
    posts = Post.query.order_by(Post.id.desc()).all()
    feed_list = []
    for p in posts:
        feed_list.append({
            "id": p.id,
            "author": p.author,
            "content": p.content,
            "timestamp": p.timestamp
        })
    return jsonify({"feed": feed_list})

# إنشاء منشور وحفظه للأبد في قاعدة البيانات
@app.route('/api/posts/create', methods=['POST'])
def create_post():
    data = request.get_json()
    author = data.get("author", "مجهول").strip()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "المحتوى فارغ يا ملك!"}), 400

    # توقيت منشور دقيق
    current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")

    new_post = Post(author=author, content=content, timestamp=current_time)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "تم النشر وحفظ البيانات بنجاح للأبد! 🔥"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
