from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'posts.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
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
        new_post = {
            'name': name,
            'status': status,
            'comment': comment,
            'time': datetime.now().strftime('%m/%d %H:%M')
        }
        posts.append(new_post)
        save_data(posts)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)