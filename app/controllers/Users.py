from system.core.controller import *
from rauth.service import OAuth1Service
from flask import redirect

facebook = OAuth1Service(
    name='facebook',
    base_url='https://graph.facebook.com/',
    # request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='259154491127882',
    consumer_secret='c5b9a2e1e25bfa25abc75a9cd2af450a',
    # request_token_params={'scope': 'email'}
)

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db

    # routes['/'] = "Users#index"
    def index(self):
        # check if user is logged in
        return self.load_view('index.html')

    # routes['/login'] = "Users#login"
    def login(self):
        if 'user' in session:
            return redirect('/')
        return self.load_view('login.html')

    # routes['/logout'] = "Users#logout"
    def logout(self):
        if 'user' in session:
            session.clear()
            session['user'] = False
            flash('You have successfully logged out','success')
        return redirect('/')

    # routes['/user/<user_id>'] = "Users#show_user"
    def show_user(self, user_id):
        if 'user' in session:
            user = self.models['User'].get_user(user_id)
            if user:
                return self.load_view('user.html', user=user)
            return redirect('/')
        return redirect('/')

    # routes['/user/inbox'] = "Users#show_inbox"
    def show_inbox(self):
        if 'user' in session:
            return self.load_view('inbox.html')
        return redirect('/')

    # routes['POST']['/login/process'] = "Users#login_process"
    def login_process(self):
        if 'user' in session:
            return redirect('/')
        return facebook.authorize(
            callback=self._app.url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))

    def oauth_authorized(self, resp):
        next_url = request.args.get('next') or self._app.url_for('index')
        if resp is None:
            flash('You denied the request to sign in.', 'error')
            return redirect(next_url)

        session['facebook_token'] = (
            resp['oauth_token'],
            resp['oauth_token_secret']
        )
        session['facebook_user'] = resp['screen_name']

        flash("You signed in as %s" % resp['screen_name'])
        return redirect(next_url)
