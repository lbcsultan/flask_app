from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from datetime import datetime
import uuid

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# 1. Home 페이지 라우트
@app.route('/')
def home():
    return render_template('home.html')

# 2. About 페이지 라우트
@app.route('/about')
def about():
    return render_template('about.html')

# 3. Contact 페이지 라우트
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 4. Dashboard 페이지 라우트
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('로그인이 필요합니다.')
        return redirect(url_for('login'))
    # 마지막 접속 시간 업데이트
    session['last_access'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('dashboard.html')


# 5. Posts 페이지 라우트 (기존 코드)
@app.route('/posts')
def posts():
    api_url = "https://jsonplaceholder.typicode.com/posts"
    posts_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        posts_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        posts_data = []
    
    return render_template('posts.html', posts=posts_data)

# 6. Photos 페이지 라우트 (기존 코드)
@app.route('/photos')
def photos():
    api_url = "https://jsonplaceholder.typicode.com/photos"
    photos_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        photos_data = response.json()[:20] 
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        photos_data = []
    
    return render_template('photos.html', photos=photos_data)

# 7. Users 페이지 라우트
@app.route('/users')
def users():
    api_url = "https://jsonplaceholder.typicode.com/users"
    users_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status() # HTTP 오류가 발생하면 예외 발생
        users_data = response.json() # JSON 응답을 파이썬 객체로 변환
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        users_data = [] # 오류 발생 시 빈 리스트 전달
    
    return render_template('users.html', users=users_data)

# 로그인 라우트 추가
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 하드코딩된 사용자 정보 (예시)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['_id'] = str(uuid.uuid4())  # 고유한 세션 ID 생성
            session['username'] = username
            session['last_access'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            flash('로그인 성공!')
            return redirect(url_for('dashboard'))
        else:
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'
    return render_template('login.html', error=error)

# 로그아웃 라우트 추가
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('로그아웃 되었습니다.')
    return redirect(url_for('home'))

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)