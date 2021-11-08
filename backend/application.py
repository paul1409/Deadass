from flask import Flask, render_template, session
from flask_sso import SSO

application = Flask(__name__)
sso = SSO(app=application)

SSO_ATTRIBUTE_MAP = {
    'ADFS_AUTHLEVEL': (False, 'authlevel'),
    'ADFS_GROUP': (True, 'group'),
    'ADFS_LOGIN': (True, 'nickname'),
    'ADFS_ROLE': (False, 'role'),
    'ADFS_EMAIL': (True, 'email'),
    'ADFS_IDENTITYCLASS': (False, 'external'),
    'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
}

application.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP
application.secret_key = 'a_super_secret_key'


@application.route('/')
def index():
    if 'user' in session:
        #return 'Welcome {name}'.format(name=session['user']['nickname'])
        # return render_template('table.html')
        return render_template('index.html')
    return render_template('index.html')


@application.route('/login')
def login():
    session['user'] = True
    return render_template('table.html')


@application.route('/table')
def table():
    return render_template('table.html')


@application.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True)
