from flask import request, render_template
from database.db import add_user

def register_routes(bp):
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            add_user(username, password)
            return "注册成功"
        return render_template('register.html')
