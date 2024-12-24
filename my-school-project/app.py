from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # 결과를 딕셔너리처럼 사용 가능
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/school-info')
def school_info():
    return render_template('school-info.html')

@app.route('/teachers')
def teachers():
    return render_template('teachers.html')

@app.route('/board', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            # 게시글 데이터베이스에 저장
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
        return redirect('/board')

    # 게시글 목록을 최신 순으로 불러오기
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()

    # 각 게시글에 해당하는 댓글 불러오기
    posts_with_comments = []
    for post in posts:
        # 각 게시글의 댓글 가져오기
        comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (post['id'],)).fetchall()
        post_data = dict(post)  # `sqlite3.Row`를 `dict`로 변환하여 수정 가능하도록 처리
        post_data['comments'] = comments  # 댓글 목록 추가
        posts_with_comments.append(post_data)

    conn.close()

    return render_template('board.html', posts=posts_with_comments)

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    comment_content = request.form.get('comment')

    if comment_content:
        conn = get_db_connection()
        conn.execute('INSERT INTO comments (content, post_id) VALUES (?, ?)', (comment_content, post_id))
        conn.commit()
        conn.close()

    return redirect('/board')

@app.route('/school-projects')
def school_projects():
    return render_template('school-projects.html')

@app.route('/school-local')
def school_local(): 
    return render_template('school-local.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
