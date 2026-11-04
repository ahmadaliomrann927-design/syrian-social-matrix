from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# قاعدة بيانات وهمية مؤقتة لتخزين منشورات وحسابات الشبكة
syrian_social_network = {
    "platform_name": "الشبكة السورية الكبرى - Syrian Social Matrix",
    "founder": "أحمد علي عمران (الـ GOAT 🐐)",
    "posts": []
}

@app.route('/')
def home():
    return jsonify({
        "status": "Online & Active",
        "system": syrian_social_network["platform_name"],
        "founder": syrian_social_network["founder"],
        "message": "أهلاً بك في قلب العاصمة البرمجية للشبكة 🚀"
    })

# نقطة نهاية (API) لإنشاء ونشر منشور جديد على الفيسبوك السوري
@app.route('/api/posts/create', methods=['POST'])
def create_post():
    data = request.json
    author = data.get('author', 'أحمد علي عمران (الـ GOAT)')
    content = data.get('content', '')
    
    if not content.strip():
        return jsonify({"error": "لا يمكن نشر محتوى فارغ يا ملك!"}), 400

    new_post = {
        "id": len(syrian_social_network["posts"]) + 1,
        "author": author,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "likes": 0
    }
    
    # إضافة المنشور لأول القائمة (أحدث منشور يظهر أولاً)
    syrian_social_network["posts"].insert(0, new_post)
    
    return jsonify({
        "status": "Success",
        "message": "تم نشر منشورك بنجاح واجتاح الشبكة يا GOAT 🔥",
        "post": new_post
    })

# نقطة نهاية لجلب كافة المنشورات الحية على الشبكة
@app.route('/api/posts/feed', methods=['GET'])
def get_feed():
    return jsonify({
        "total_posts": len(syrian_social_network["posts"]),
        "feed": syrian_social_network["posts"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
