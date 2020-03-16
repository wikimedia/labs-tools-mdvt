from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
import mwoauth

from mdvt.config.config import config

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('main/home.html',
                           title='Home',
                           username=session.get('username', None))


@main.route('/login', defaults={'return_url': None})
@main.route('/login/<path:return_url>')
def login(return_url):
    if return_url:
        session['return_url'] = return_url
    consumer_token = mwoauth.ConsumerToken(
        config['OAUTH_TOKEN'], config['OAUTH_SECRET'])
    redirect_url, request_token = mwoauth.initiate(
        config['OAUTH_URI'], consumer_token)
    session['request_token'] = dict(zip(request_token._fields, request_token))
    return redirect(redirect_url)


@main.route('/oauth-callback')
def oauth_callback():
    consumer_token = mwoauth.ConsumerToken(config['OAUTH_TOKEN'],
                                           config['OAUTH_SECRET'])
    access_token = mwoauth.complete(
        config['OAUTH_URI'], consumer_token,
        mwoauth.RequestToken(**session['request_token']), request.query_string)
    identity = mwoauth.identify(
        config['OAUTH_URI'], consumer_token, access_token)
    session['username'] = identity['username']
    session['access_token'] = dict(zip(access_token._fields, access_token))
    return redirect(session.pop('return_url', url_for('main.home')))


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))
