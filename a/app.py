from flask import Flask, render_template, request, redirect, url_for
import json
import os 
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = 'posts.json'

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return []
            
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            
            posts = json.load(f)
        
        now = datetime.now()
        fresh_posts = []
        for post in posts:
            if 'full_time' not in post:
                continue
                
            post_time = datetime.strptime(post['full_time'], '%Y-%m-%d %H:%M:%S')
            
            
            if now - post_time < timedelta(hours=1):
                fresh_posts.append(post)
        
        
        save_data(fresh_posts)
        
        return fresh_posts
    
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    posts = load_data()
    return render_template('index.html', posts=reversed(posts))

@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    status = request.form.get('status')
    comment = request.form.get('comment')
    
    if name and status:
        posts = load_data()
        now = datetime.now() 
        new_post = {
            'name': name,
            'status': status,
            'comment': comment,
            'full_time': now.strftime('%Y-%m-%d %H:%M:%S'), 
            'time': now.strftime('%m/%d %H:%M')
        }
        posts.append(new_post)
        save_data(posts)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)