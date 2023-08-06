import datetime
import logging
import exceptions
from shaft.exceptions import AppError
from shaft import utils
from shaft import decorators as shaft_deco
from shaft import (Shaft,
                   models,
                   page_meta,
                   init_app,
                   get_config,
                   session,
                   request,
                   redirect,
                   url_for,
                   flash_success,
                   flash_error,
                   abort,
                   recaptcha,
                   storage,
                   decorators as shaft_deco,
                   utils)
from flask_login import (LoginManager,
                         login_user,
                         current_user,
                         fresh_login_required)
from . import (logout_user, 
               is_authenticated,
               not_authenticated,
               send_password_reset_email,
               send_email_verification_email,
               send_registration_welcome_email,
               require_login_allowed, 
               require_register_allowed,
               require_social_login_allowed,
               session_set_require_password_change, 
               _get_app_options,
               get_user_url_safe,
               get_email_url_safe,
               login, 
               register)


def main(**kwargs):
    """
    This plugin allow user to login to application

        - options:
            - login_view
            - logout_view
            - verify_email

    """

    options = kwargs.get("options", {})

    login_view = options.get("login_view") or "Index:index"
    logout_view = options.get("logout_view") or "Index:login"
    verify_email = options.get("verify_email") or False

    login_manager = LoginManager()
    login_manager.login_view = "AuthLogin:login"
    login_manager.login_message_category = "error"
    init_app(login_manager.init_app)

    @login_manager.user_loader
    def load_user(userid):
        return models.AuthUser.get(userid)

    def menu_title_visible_register():
        if not _get_app_options().get("allow_register", False):
            return False
        return not_authenticated()

    def menu_title_visible_login():
        if not _get_app_options().get("allow_login", False):
            return False
        return not_authenticated()

    navigation = kwargs.get("menu_title", {})
    navigation.setdefault("title", None)
    navigation.setdefault("visible", True)
    navigation.setdefault("order", 100)
    navigation["visible"] = not_authenticated

    Shaft.g(__AUTH_ENABLED__=True)

    @shaft_deco.menu_title(**navigation)
    class AuthLogin(Shaft):
        base_route = kwargs.get("route") or "/"

        @shaft_deco.menu_title("Login", visible=menu_title_visible_login)
        @shaft_deco.accept_post_get
        @require_login_allowed
        @logout_user
        def login(self):
            page_meta(title="Login")

            if request.method == "POST":
                if request.form.get("method") == "email":
                    return self._post_login_email()
                elif request.form.get("method") == "social":
                    return self._post_login_social()
                else:
                    abort(400, "Invalid login method")

            return {
                "email": request.args.get("email"),
                "login_url_next": request.args.get("next", ""),
                "allow_register": options.get("allow_register"),
                "show_verification_message": True if request.args.get("v") == "1" else False
            }

        def _post_login_email(self):
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()

            try:
                if not email or not password:
                    flash_error("Email or Password is empty")
                    return redirect(self.login, next=request.form.get("next"))

                user = login(email=email, password=password, require_verified_email=verify_email)
                if user:
                    userl = user.get_login()
                    if userl.require_password_change is True:
                        flash("Password change is required", "info")
                        session_set_require_password_change(True)
                        return redirect(views.AuthAccount.change_password)
                    return redirect(request.form.get("next") or login_view)
                else:
                    flash_error("Email or Password is invalid")
                    return redirect(self.login, next=request.form.get("next"))

            except exceptions.VerifyEmailError as ve:
                return redirect(self.login, email=email, v="1")

            except Exception as e:
                logging.exception(e)
                flash_error("Unable to login")
                return redirect(self.login, next=request.form.get("next"))

        def _post_login_social(self):
            return redirect(self.login)

        @shaft_deco.menu_title("Logout", visible=False)
        @shaft_deco.accept_get
        @logout_user
        def logout(self):
            session_set_require_password_change(False)
            return redirect(logout_view or self.login)

        @shaft_deco.menu_title("Lost Password", visible=False)
        @shaft_deco.accept_post_get
        @require_login_allowed
        @logout_user
        def lost_password(self):
            page_meta(title="Lost Password")

            if request.method == "POST":
                email = request.form.get("email")
                user_l = models.AuthUserLogin.get_by_email(email)
                if user_l:
                    send_password_reset_email(user=user_l.user)
                    flash_success("A new password has been sent to '%s'" % email)
                    return redirect(self.login)
                else:
                    flash_error("Invalid email address")
                    return redirect(self.lost_password)

        @shaft_deco.menu_title("Signup", visible=menu_title_visible_register)
        @shaft_deco.accept_post_get
        @require_login_allowed
        @require_register_allowed
        @logout_user
        def register(self):
            """
            For Email Signup
            :return:
            """
            page_meta(title="Signup")
            if request.method == "POST":
                if request.form.get("method") == "email":
                    return self._post_register_email()
                elif request.form.get("method") == "social":
                    return self._post_register_social()
                else:
                    abort(400, "Invalid register method")

            return dict(login_url_next=request.args.get("next", ""),)

        def _post_register_email(self):
            if not recaptcha.verify():
                flash_error("Invalid Security code")
                return redirect(self.register, next=request.form.get("next"))
            try:
                name = request.form.get("name")
                email = request.form.get("email")
                password = request.form.get("password")
                password2 = request.form.get("password2")

                if not name:
                    raise exceptions.AuthError("Name is required")
                elif not password.strip() or password.strip() != password2.strip():
                    raise exceptions.AuthError("Passwords don't match")
                else:
                    session = True if not verify_email else False
                    user = register(email=email,
                                    password=password,
                                    name=name)
                    if verify_email:
                        send_registration_welcome_email(user)
                        flash_success("A welcome email containing a confirmation link has been sent")

                    return redirect(request.form.get("next") or login_view)
            except exceptions.AuthError as ex:
                flash_error(ex.message)
            except Exception as e:
                logging.exception(e)
                flash_error("Unable to register")
            return redirect(self.register, next=request.form.get("next"))

        @shaft_deco.menu_title("Reset Password", visible=False)
        @shaft_deco.route("/reset-password/<token>/<email>/", methods=["POST", "GET"])
        @require_login_allowed
        @logout_user
        def reset_password(self, token, email):
            """
            :param token: token
            :param email: tokenized email
            :return:
            """
            page_meta(title="Reset Password")
            user_login = get_user_url_safe(token, "reset-password")
            emailT = email
            email = get_email_url_safe(email)
            if user_login and email:
                if user_login.email != email:
                    flash_error("Verification Invalid!")
                    return redirect(self.login)

                if request.method == "POST":
                    try:
                        password = request.form.get("password", "").strip()
                        password2 = request.form.get("password2", "").strip()
                        if not password:
                            raise exceptions.AuthError("Password is missing")
                        elif password != password2:
                            raise exceptions.AuthError("Password don't match")

                        user_login.change_password(password)
                        user_login.clear_temp_login()
                        user_login.set_email_verified(True)
                        session_set_require_password_change(False)

                        flash_success("Password updated successfully!")
                        return redirect(login_view)
                    except exceptions.AuthError as ex:
                        flash_error("Error: %s" % ex.message)
                        return redirect(self.reset_password, token=token)
                    except Exception as e:
                        logging.exception(e)
                        flash_error("Unable to reset password")
                        return redirect(self.login)
                return {"token": token, "email": emailT}

            return redirect(self.login)

        @shaft_deco.menu_title("Confirm Email", visible=False)
        @shaft_deco.accept_post_get
        @require_login_allowed
        @logout_user
        def confirm_email(self):
            if not verify_email:
                return redirect(self.login)

            if request.method == "POST":
                email = request.form.get("email")
                if email and utils.is_email_valid(email):
                    userl = models.AuthUserLogin.get_by_email(email)
                    if userl:
                        if not userl.email_verified:
                            send_email_verification_email(userl.user)
                            flash_success("A verification email has been sent to %s" % email)
                        return redirect(self.login, email=email)
                flash_error("Invalid account")
                return redirect(self.confirm_email, email=email)

            page_meta(title="Confirm Email")
            return {
                "email": request.args.get("email"),
            }

        @require_login_allowed
        @logout_user
        def verify_email(self, token, email):
            try:
                user_login = get_user_url_safe(token, "verify-email")
                email = get_email_url_safe(email)
                if user_login and email:
                    if user_login.email != email:
                        flash_error("Verification Invalid!")
                    else:
                        user_login.set_email_verified(True)
                        flash_success("Account verified. You can now login")
                        return redirect(self.login, email=user_login.email)
            except Exception as e:
                logging.exception(e)
                flash_error("Verification Failed!")
            return redirect(self.login)
            
    return AuthLogin
