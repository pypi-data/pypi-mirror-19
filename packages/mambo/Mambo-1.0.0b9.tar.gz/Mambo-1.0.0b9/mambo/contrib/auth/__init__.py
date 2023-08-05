import datetime
import flask_login
from flask_login import current_user
import flask_login
from flask import current_app
from mambo import (register_package, get_config, abort, send_mail, url_for, views, 
                   models, utils, request, redirect, flash, session, emit_signal, init_app)
from mambo.exceptions import AppError
from mambo.core import get_installed_app_options
import signals
import exceptions
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
import logging

register_package(__package__)

__version__ = "1.0.0"

ROLES_SUPERADMIN = ["SUPERADMIN"]
ROLES_ADMIN = ROLES_SUPERADMIN + ["ADMIN"]
ROLES_MANAGER = ROLES_ADMIN + ["MANAGER"]
ROLES_CONTRIBUTOR = ROLES_MANAGER + ["EDITOR", "CONTRIBUTOR"]
ROLES_MODERATOR = ROLES_CONTRIBUTOR + ["MODERATOR"]

JWT_TTL = 3600
JWT_SALT = "mambo.contrib.auth"


TOKENIZATION_SALTS = {
    "verify-email": "auth:verify-email",
    "reset-password": "auth:reset-password",
    "email": "auth:email"
}


_app_options = None

def main(app, **kwargs):
    @app.before_request
    def force_password_change():
        _ = _get_app_options().get("require_password_change_exclude_endpoints")
        _ = [] if not isinstance(_, list) else _

        exclude_endpoints = ["static", "ContactPage:index", "Index:index",
                             "AuthLogin:logout"] + _

        if current_user and current_user.is_authenticated:
            if request.endpoint \
                    and request.endpoint not in exclude_endpoints:
                if request.endpoint != "AuthAccount:change_password" \
                        and session_get_require_password_change():
                    flash("Password Change is required", "info")
                    return redirect(views.AuthAccount.change_password)


def _get_app_options():
    global _app_options
    if not _app_options:
        _app_options = get_installed_app_options(__name__)
    return _app_options


def is_authenticated():
    """ A shortcut to check if a user is authenticated """
    return current_user.is_authenticated


def not_authenticated():
    """ A shortcut to check if user not authenticated."""
    return not is_authenticated()

def get_random_password(length=8):
    return utils.generate_random_string(length)


# ------------------------------------------------------------------------------
#
def visible_to(*roles):
    """
    This is a @nav_menu specific function to set the visibility of menu based on
    roles
    :param roles:
    :return: callback fn
    """
    if is_authenticated():
        return True if current_user.has_any_roles(*roles) else False
    return False


# Alias to visible_to
visible_to_superadmins = lambda: visible_to(*ROLES_SUPERADMIN)
visible_to_admins = lambda: visible_to(*ROLES_ADMIN)
visible_to_managers = lambda: visible_to(*ROLES_MANAGER)
visible_to_contributors = lambda: visible_to(*ROLES_CONTRIBUTOR)
visible_to_moderators = lambda: visible_to(*ROLES_MODERATOR)
visible_to_authenticated = lambda: is_authenticated()
visible_to_notauthenticated = lambda: not_authenticated()

# ------------------------------------------------------------------------------

# TOKENIZATION


def get_jwt_secret():
    secret_key = get_config("JWT_SECRET") or get_config("SECRET_KEY")
    if not secret_key:
        raise exceptions.AuthError("Missing config JWT/SECRET_KEY")
    return secret_key


def make_jwt(user_id, expires_in=None):
    """
    Create a secure timed JWT token that can be passed. It save the user id,
    which later will be used to retrieve the data

    :param user_id: int - the user id
    :param expires_in: - time in second for the token to expire
    :param kw: **kw
    :return: string
    """
    secret_key = get_jwt_secret()

    data = {
        "id": user_id
    }
    s = utils.sign_jwt(data=data,
                       secret_key=secret_key,
                       salt=JWT_SALT,
                       expires_in=expires_in or JWT_TTL)
    return s


def get_jwt(token=None):
    """
    Return the user associated to the token, otherwise it will return None.
    If token is not provided, it will pull it from the headers: Authorization

    Exception:
    Along with AuthError, it may
    :param token:
    :return: User
    """

    if not token:
        if not 'Authorization' in request.headers:
            raise exceptions.AuthError("Missing Authorization Bearer in headers")
        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '').strip()

    secret_key = get_jwt_secret()

    s = utils.unsign_jwt(token=token,
                         secret_key=secret_key,
                         salt=JWT_SALT)
    if "id" not in s:
        raise exceptions.AuthError("Invalid Authorization Bearer Token")

    return get_user(int(s["id"]))


def make_user_login_url_safe(user_login_id, expires_in, salt):
    """
    Make an auth url safe token. usually to do some account action. It will
    connect to the UserLogin table
    It will set the user
    :param user_login_id:
    :param expires_in: 
    :param salt: 
    :return: 
    """
    secret_key = get_jwt_secret()
    data = {"id": user_login_id}
    return utils.sign_url_safe(data,
                               secret_key=secret_key,
                               salt=TOKENIZATION_SALTS[salt],
                               expires_in=expires_in)


def get_user_login_url_safe(token, salt):
    """
    Get the user and return the user object . 
    :param token: 
    :param salt: 
    :return: int : User 
    """
    secret_key = get_jwt_secret()
    data = utils.unsign_url_safe(token,
                                 secret_key=secret_key,
                                 salt=TOKENIZATION_SALTS[salt])
    if "id" not in data:
        raise exceptions.AuthError("Invalid Token")
    return get_user_login(int(data["id"]))


def make_email_url_safe(email):
    secret_key = get_jwt_secret()
    return utils.sign_url_safe(email,
                               secret_key=secret_key,
                               salt=TOKENIZATION_SALTS["email"])


def get_email_url_safe(email):
    secret_key = get_jwt_secret()
    return utils.unsign_url_safe(email,
                                 secret_key=secret_key,
                                 salt=TOKENIZATION_SALTS["email"])

# ------------------------------------------------------------------------------
# SIGNUP + LOGIN


def get_user(id):
    """
    To get a user by id
    :param id:
    :return: AuthUser object
    """
    return models.AuthUser.get(id)


def get_user_login(id):
    """
    To get a user by id
    :param id:
    :return: AuthUserLogin object
    """
    return models.AuthUserLogin.get(id)


def get_user_login_by_email(email):
    return models.AuthUserLogin.get_by_email(email)


def session_login(user_login):
    """
    Login the user to the session
    :param user_login: AuthUserLogin
    :return:
    """
    flask_login.login_user(user_login.user)


def login_with_email(email, password, require_verified_email=False, session=True):
    """
    To login with email and password
    Additionally, it may require_th
    :param email:
    :param password:
    :param require_verified_email:
    :param session:
    :return: on_login signal
    """
    def cb():
        userl = models.AuthUserLogin.get_by_email(email)
        if userl and userl.password_hash \
                and userl.password_matched(password):
            if require_verified_email and not userl.email_verified:
                raise exceptions.VerifyEmailError()
            userl.user.update(last_login=datetime.datetime.now())
            if session:
                session_login(userl)
            return userl
        return None
    return signals.on_login(cb)


def register_with_email(email, password, name, role=None):
    """
    To create a new email login
    :param email:
    :param password:
    :param name:
    :return: AuthUserLogin
    """
    def cb():
        return models\
            .AuthUserLogin.new(login_type=models.AuthUserLogin.TYPE_EMAIL,
                               email=email,
                               password=password.strip(),
                               user_info={
                                    "name": name,
                                    "contact_email": email,
                                    "role": role
                               })
    return signals.on_register(cb)


def reset_password(user_login):
    """
    Return the new random password that has been reset
    :param user_login: AuthUserLogin
    :return: string - the new password
    """
    def cb():
        return user_login.change_password(random=True)
    return signals.on_password_reset(cb)


def get_password_reset_token(user_login):
    pass

# ------------------------------------------------------------------------------
# EMAIL SENDING


def url_for_email(endpoint, base_url=None, **kw):
    """
    Create an external url_for by using a custom base_url different from the domain we
    are on
    :param endpoint:
    :param base_url:
    :param kw:
    :return:
    """
    base_url = base_url or get_config("MAIL_EXTERNAL_BASE_URL")
    _external = True if not base_url else False
    url = url_for(endpoint, _external=_external, **kw)
    if base_url and not _external:
        url = "%s/%s" % (base_url.strip("/"), url.lstrip("/"))
    return url


def send_mail_password_reset(email=None, user_login=None, base_url=None):
    """
    Reset a password and send the email to the user
    :param email:
    :param user_login:
    :param url_prefix:
    :return:
    """

    if email:
        user_login = get_user_login_by_email(email)
    if not user_login:
        raise exceptions.AuthError("Invalid account. Unable to send email")
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise exceptions.AuthError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    delivery = options.get("reset_password_method") or "token"
    email_template = options.get("reset_password_email_template") or "reset-password.txt"
    new_password = None

    if delivery.lower() == "token":
        # in minutes
        expires_in = get_config("reset_password_token_ttl") or 60
        expires_in = expires_in * 60

        token = make_user_login_url_safe(user_login.id,
                                         expires_in=expires_in,
                                         salt="reset-password")

        email = make_email_url_safe(user_login.email)
        url = url_for_email(views.AuthLogin.reset_password,
                            base_url=base_url,
                            token=token,
                            email=email)
    else:
        new_password = reset_password(user_login)
        url = url_for_email(views.AuthLogin.index, base_url=base_url)

    send_mail(template=email_template,
              method_=delivery.lower(),
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              url=url,
              new_password=new_password)


def send_mail_verification_email(user_login, base_url=None):

    options = _get_app_options()
    email_template = options.get("verify_email_template") or "verify-email.txt"

    url = _create_verify_email_token_url(user_login, base_url=base_url)

    send_mail(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url)


def send_mail_register_welcome(user_login, base_url=None):

    options = _get_app_options()
    verify_email = options.get("verify_email") or False
    email_template = options.get("verify_register_email_template") or "verify-register-email.txt"

    url = _create_verify_email_token_url(user_login, base_url=base_url)

    send_mail(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url,
              verify_email=verify_email)


def _create_verify_email_token_url(user_login, base_url=None):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise exceptions.AuthError(
            "Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    expires_in = options.get("verify_email_token_ttl") or (60 * 24)

    user_login.set_email_verified(False)
    token = make_user_login_url_safe(user_login.id,
                                     expires_in=expires_in,
                                     salt="verify-email")
    email = make_email_url_safe(user_login.email)
    return url_for_email(views.AuthLogin.verify_email,
                         token=token,
                         email=email,
                         base_url=base_url)



def session_set_require_password_change(change=True):
    session["auth:require_password_change"] = change


def session_get_require_password_change():
    return session.get("auth:require_password_change")




# ------------------------------------------------------------------------------
# CLI
from mambo.cli import MamboCLI

class CLI(MamboCLI):
    def __init__(self, command, click):
        @command("auth:create-super-admin")
        @click.argument("email")
        def create_super_admin(email):
            """
            To create a super admin by providing the email address
            """
            print("-" * 80)
            print("Mambo Auth: Create Super Admin")
            print("Email: %s" % email)
            try:
                password = get_random_password()
                nl = create_new_login(email=email,
                                      password=password,
                                      name="SuperAdmin",
                                      role=models.AuthRole.SUPERADMIN)
                nl.update(require_password_change=True)
                print("Password: %s" % password)
            except Exception as e:
                print("ERROR: %s" % e)

            print("Done!")

        @command("auth:reset-password")
        @click.argument("email")
        def reset_password(email):
            """
            To reset password by email
            """
            print("-" * 80)
            print("Mambo Auth: Reset Password")
            try:
                ul = models.AuthUserLogin.get_by_email(email)

                if not ul:
                    raise Exception("Email '%s' doesn't exist" % email)
                print(ul.email)
                password = get_random_password()
                ul.change_password(password)
                ul.update(require_password_change=True)
                print("Email: %s" % email)
                print("New Password: %s" % password)
            except Exception as e:
                print("ERROR: %s" % e)

            print("Done!")

        @command("auth:user-info")
        @click.option("--email")
        @click.option("--id")
        def reset_password(email=None, id=None):
            """
            Get the user info by email or ID
            """
            print("-" * 80)
            print("Mambo Auth: User Info")
            print("")
            try:
                if email:
                    ul = models.AuthUserLogin.get_by_email(email)
                    if not ul:
                        raise Exception("Invalid Email address")
                    user_info = ul.user
                elif id:
                    user_info = models.AuthUser.get(id)
                    if not user_info:
                        raise Exception("Invalid User ID")

                k = [
                    ("ID", "id"), ("Name", "name"), ("First Name", "first_name"),
                    ("Last Name", "last_name"), ("Signup", "created_at"),
                    ("Last Login", "last_login"), ("Signup Method", "register_method"),
                    ("Is Active", "is_active")
                ]
                print("Email: %s" % user_info.get_email_login().email)
                for _ in k:
                    print("%s : %s" % (_[0], getattr(user_info, _[1])))

            except Exception as e:
                print("ERROR: %s" % e)

            print("")
            print("Done!")


# ---

from .decorators import *
