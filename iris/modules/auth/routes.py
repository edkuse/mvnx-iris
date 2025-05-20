from flask import render_template, redirect, url_for, current_app, request, session, Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from . import bp
from .models import User
from .services import UserService
from iris.extensions import db, login_manager
from iris.utils.helpers import flash_error
import base64
import msal
import requests
import uuid


# Microsoft Entra ID (Azure AD) configuration
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        current_app.config['MS_CLIENT_ID'],
        authority=current_app.config['MS_AUTHORITY'],
        client_credential=current_app.config['MS_CLIENT_SECRET'],
        token_cache=cache
    )

def _get_token_from_cache(scopes):
    cache = _load_cache()
    cca = _build_msal_app(cache)
    accounts = cca.get_accounts()
    if accounts:
        result = cca.acquire_token_silent(scopes, account=accounts[0])
        _save_cache(cache)
        return result
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/login')
def login():
    # Generate a random state for CSRF protection
    session["state"] = str(uuid.uuid4())
    
    # Build the auth URL
    auth_url = _build_msal_app().get_authorization_request_url(
        current_app.config['MS_SCOPES'],
        state=session["state"],
        redirect_uri='https://mvnx-iris-tool-azg8b6edecfudkbd.westcentralus-01.azurewebsites.net/auth/callback'
    )
    
    return render_template('auth/login.html', auth_url=auth_url)

@bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('dashboard.index'))

@bp.route('/callback')
def authorized():
    # Verify state to prevent CSRF
    if request.args.get('state') != session.get("state"):
        return redirect(url_for('auth.login'))
    
    # Get token
    cache = _load_cache()
    cca = _build_msal_app(cache)
    
    result = cca.acquire_token_by_authorization_code(
        request.args['code'],
        scopes=current_app.config['MS_SCOPES'],
        redirect_uri='https://mvnx-iris-tool-azg8b6edecfudkbd.westcentralus-01.azurewebsites.net/auth/callback'
    )
    
    # Save cache
    _save_cache(cache)
    
    if "error" in result:
        flash_error(f"Login failed: {result.get('error_description', 'Unknown error')}")
        return redirect(url_for('dashboard.index'))
    
    # Get user info
    ms_id = result.get('id_token_claims', {}).get('oid')
    if not ms_id:
        flash_error("Could not retrieve user information from Microsoft Entra ID")
        return redirect(url_for('auth.login'))
    
    # Get user from database or create new user
    user = User.query.filter_by(ms_id=ms_id).first()
    
    if not user:
        # Get more user info from Microsoft Graph API
        graph_data = _get_user_info_from_graph(result['access_token'])
        
        if not graph_data:
            flash_error("Could not retrieve user information from Microsoft Graph")
            return redirect(url_for('auth.login'))
        
        # Create new user
        user = UserService.create_user_from_ms_data(ms_id, graph_data)
    else:
        # Update user profile picture on login
        graph_data = _get_user_info_from_graph(result['access_token'])
        if graph_data:
            UserService.update_user_profile(user, graph_data)
    
    # Update last login
    UserService.update_last_login(user)
    
    # Log in the user
    login_user(user)
    
    # Redirect to next page or home
    next_page = session.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('dashboard.index')
    
    return redirect(next_page)

def _get_user_info_from_graph(access_token):
    """Get user info from Microsoft Graph API."""
    graph_url = current_app.config['MS_GRAPH_API'] + '/v1.0/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(graph_url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        # Get profile photo
        photo_data = _get_profile_photo(access_token)
        if photo_data:
            user_data['profile_photo'] = photo_data
        
        return user_data
    except Exception as e:
        current_app.logger.error(f"Error getting user info from Graph API: {str(e)}")
        return None

def _get_profile_photo(access_token):
    """Get user profile photo from Microsoft Graph API."""
    photo_url = current_app.config['MS_GRAPH_API'] + '/v1.0/me/photo/$value'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(photo_url, headers=headers)
        if response.status_code == 200:
            # Convert photo to base64 for storage or direct display
            photo_base64 = base64.b64encode(response.content).decode('utf-8')
            return f"data:{response.headers.get('Content-Type', 'image/jpeg')};base64,{photo_base64}"
        else:
            current_app.logger.warning(f"Could not retrieve profile photo: {response.status_code}")
            return None
    except Exception as e:
        current_app.logger.error(f"Error getting profile photo: {str(e)}")
        return None

@bp.route('/profile')
@login_required
def profile():
    # Get fresh token for API calls if needed
    token = _get_token_from_cache(current_app.config['MS_SCOPES'])
    
    # If token is available, we can refresh user data
    if token:
        graph_data = _get_user_info_from_graph(token['access_token'])
        if graph_data:
            UserService.update_user_profile(current_user, graph_data)
    
    return render_template('auth/profile.html')

@bp.route('/profile-photo')
@login_required
def profile_photo():
    """Endpoint to serve user profile photo."""
    if not current_user.profile_picture:
        return redirect(url_for('static', filename='images/default-avatar.jpg'))
    
    # If the profile picture is a data URL, return it directly
    if current_user.profile_picture.startswith('data:'):
        # Extract content type and base64 data
        content_type = current_user.profile_picture.split(';')[0].split(':')[1]
        base64_data = current_user.profile_picture.split(',')[1]
        
        # Decode base64 data
        binary_data = base64.b64decode(base64_data)
        
        # Create response with correct content type
        response = Response(binary_data, mimetype=content_type)
        return response
    
    # If it's a URL, redirect to it
    return redirect(current_user.profile_picture)
