from flask import Flask, render_template, session
from flask_sso import SSO

# Python standard libraries
import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = "41527998879-60duld414e26c6aef9ual8va2i5vveg8.apps.googleusercontent.com"#os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = "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"#os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)




application = Flask(__name__)
application.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# sso = SSO(app=application)

# SSO_ATTRIBUTE_MAP = {
#     'ADFS_AUTHLEVEL': (False, 'authlevel'),
#     'ADFS_GROUP': (True, 'group'),
#     'ADFS_LOGIN': (True, 'nickname'),
#     'ADFS_ROLE': (False, 'role'),
#     'ADFS_EMAIL': (True, 'email'),
#     'ADFS_IDENTITYCLASS': (False, 'external'),
#     'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
# }

# application.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP
# application.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
#application.secret_key = 'a_super_secret_key'
login_manager = LoginManager()
login_manager.init_app(application)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
print(client)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




@application.route('/')
def index():
    # if 'user' in session:
    #     #return 'Welcome {name}'.format(name=session['user']['nickname'])
    #     # return render_template('table.html')
    #     return render_template('index.html')

    if current_user.is_authenticated:
        # return (
        #     "<p>Hello, {}! You're logged in! Email: {}</p>"
        #     "<div><p>Google Profile Picture:</p>"
        #     '<img src="{}" alt="Google profile pic"></img></div>'
        #     '<a class="button" href="/logout2">Logout</a>'.format(
        #         current_user.name, current_user.email, current_user.profile_pic
        #     )
        # )
        print('success')
        return render_template('table.html', user_name=current_user.name)

    else:
        return '<a class="button" href="/login2">Google Login</a>'
    return 'fail'#render_template('index.html')

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@application.route("/login2")
def login2():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)







@application.route("/login2/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]


    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))


    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

        # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@application.route("/logout2")
@login_required
def logout2():
    logout_user()
    return redirect(url_for("index"))
'''
original application code
'''
@application.route('/login')
def login():
    session['user'] = True
    return render_template('table.html')


@application.route('/table')
def table():
    return render_template('table.html')


@application.route('/genderVisualizations')
def visualizations():
    return render_template('gender.html')


@application.route('/ageVisualizations')
def ageVisualizations():
    return render_template('age.html')


@application.route('/salaryVisualizations')
def salaryVisualizations():
    return render_template('salary.html')


@application.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')



if __name__ == "__main__":
    application.run(ssl_context="adhoc")

# if __name__ == '__main__':
#     application.run(debug=True)
