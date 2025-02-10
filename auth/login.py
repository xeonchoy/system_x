from flask import request, render_template, redirect, url_for
from database.db import verify_user

def login_routes(bp):
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if verify_user(username, password):
                return redirect(url_for('dashboard'))
        return render_template('login.html')
