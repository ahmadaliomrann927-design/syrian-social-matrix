import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# إعداد قاعدة البيانات الدائمة والمرعبة للسيستم الاحترافي
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matrix_elite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 1. جدول المستخدمين (حسابات حقيقية)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(255), default="عضو في الإمبراطورية 🖤")

# 2. جدول المنشورات والفيديوهات (يدعم الوسائط والنصوص)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500), nullable=True)  # رابط فيديو أو صورة
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.String(50), nullable=False)

# 3. جدول القصص (Stories - تختفي وتهلك بمرور الوقت)
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    media_url = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Syrian Social Matrix - Elite Edition is Online & Ready 💀🔥"

# جلب الحائط الكامل مع المنشورات والفيديوهات
@app.route('/api/feed', methods=['GET'])
def get_feed():
    posts = Post.query.order_by(Post.id.desc()).all()
    feed_list = []
    for p in posts:
        feed_list.append({
            "id": p.id,
            "author": p.author,
            "content": p.content,
            "media_url": p.media_url,
            "likes": p.likes,
            "timestamp": p.timestamp
        })
    return jsonify({"feed": feed_list})

# نشر منشور أو فيديو جديد
@app.route('/api/post/create', methods=['POST'])
def create_post():
    data = request.get_json()
    author = data.get("author", "مجهول").strip()
    content = data.get("content", "").strip()
    media_url = data.get("media_url", "").strip()

    if not content and not media_url:
        return jsonify({"error": "ما يصير تنشر فراغ يا ملك!"}), 400

    current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
    new_post = Post(author=author, content=content, media_url=media_url, timestamp=current_time)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "تم إطلاق المنشور بنجاح في الإمبراطورية 🔥"}), 201

# نظام الإعجابات الخارق
@app.route('/api/post/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({"likes": post.likes})

# نظام القصص (Stories)
@app.route('/api/stories', methods=['GET'])
def get_stories():
    stories = Story.query.order_by(Story.id.desc()).all()
    story_list = [{"id": s.id, "author": s.author, "media_url": s.media_url, "timestamp": s.timestamp} for s in stories]
    return jsonify({"stories": story_list})

@app.route('/api/story/create', methods=['POST'])
def create_story():
    data = request.get_json()
    author = data.get("author", "مجهول").strip()
    media_url = data.get("media_url", "").strip()
    
    if not media_url:
        return jsonify({"error": "القصة تحتاج إلى محتوى مرئي أو فيديو!"}), 400

    current_time = datetime.now().strftime("%I:%M %p")
    new_story = Story(author=author, media_url=media_url, timestamp=current_time)
    db.session.add(new_story)
    db.session.commit()

    return jsonify({"message": "تم بث القصة بنجاح 🚀"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
