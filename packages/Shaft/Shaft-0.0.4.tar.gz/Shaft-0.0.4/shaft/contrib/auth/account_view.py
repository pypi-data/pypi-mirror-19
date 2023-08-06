import datetime
import uuid
import arrow
import exceptions
from flask_login import fresh_login_required
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
                   utils,
                   decorators as shaft_deco,
                   utils)
from . import (current_user,
               register,
               authenticated,
               logout_user,
               is_authenticated,
               not_authenticated,
               require_login_allowed,
               require_register_allowed,
               require_social_login_allowed,
               send_password_reset_email,
               send_email_verification_email,
               send_registration_welcome_email,
               session_set_require_password_change)

def main(**kwargs):

    options = kwargs.get("options", {})
    nav_title_partial = "AuthAccount/nav_title_partial.html"
    nav_kwargs = kwargs.get("nav_menu", {})
    verify_email = options.get("verify_email") or False

    @shaft_deco.menu_title(
        title=nav_kwargs.pop("title", "My Account") or "My Account",
        visible=is_authenticated,
        css_id=nav_kwargs.pop("css_id", "auth-account-menu"),
        css_class=nav_kwargs.pop("css_class", "auth-account-menu"),
        align_right=nav_kwargs.pop("align_right", True),
        title_partial=nav_kwargs.pop("title_partial", nav_title_partial),
        **nav_kwargs)
    class AuthAccount(Shaft):
        base_route = kwargs.get("route") or "/"
        decorators = Shaft.decorators + [authenticated] + kwargs.get("decorators")

        def _confirm_password(self):
            user_login = current_user.user_login("email")
            password = request.form.get("confirm-password")
            if not user_login.password_matched(password):
                raise exceptions.AuthError("Invalid password")
            return True

        @shaft_deco.menu_title("Logout", endpoint="AuthLogin:logout", order=100)
        def _(self): pass

        @shaft_deco.menu_title("Account Info", order=1)
        def account_info(self):
            page_meta(title="Account Info")

        @shaft_deco.menu_title("Edit Account Info", visible=False)
        @shaft_deco.accept_post_get
        def edit_account_info(self):
            page_meta(title="Edit Account Info")

            if request.method == "POST":
                try:
                    data = {
                        "name": request.form.get("name"),
                        "first_name": request.form.get("first_name"),
                        "last_name": request.form.get("last_name"),
                        "address": request.form.get("address"),
                        "address_city": request.form.get("address_city"),
                        "address_state": request.form.get("address_state"),
                        "address_country": request.form.get("address_country"),
                        "address_zip_code": request.form.get("address_zip_code"),
                        "telephone": request.form.get("telephone"),
                    }
                    dob = request.form.get("dob")
                    if dob:
                        data["date_of_birth"] = arrow.get(dob, models.AuthUser.DOB_FORMAT).datetime
                    current_user.update(**data)

                    flash_success("Account info updated successfully!")

                except exceptions.AuthError as ae:
                    flash_error(ae.message)
                except Exception as e:
                    logging.exception(e)
                    flash_error("Unable to edit account info")
                return redirect(self.account_info)

        @shaft_deco.menu_title("Change Login", order=2)
        @shaft_deco.accept_post_get
        def change_email(self):
            page_meta(title="Change Login Email")

            user_login = current_user.user_login("email")
            if not user_login:
                abort(400, "Require and Email account login to continue")

            if request.method == "POST":
                try:
                    self._confirm_password()

                    email = request.form.get("email")
                    if utils.is_email_valid(email):
                        user_login.change_email(email)
                        flash_success("Login Email changed successfully!")
                        return redirect(self.account_info)
                    else:
                        raise exceptions.AuthError("Invalid email")
                except exceptions.AuthError as ex:
                    flash_error("Error: %s" % ex)
                    return redirect(self)
                except Exception as e:
                    logging.exception(e)
                    flash_error("Unable to change email")
                    return redirect(self)

            return {
                "user_login": user_login
            }

        @shaft_deco.menu_title("Change Password", order=3)
        @shaft_deco.accept_post_get
        def change_password(self):
            page_meta(title="Change Password")

            user_login = current_user.user_login("email")
            if not user_login:
                abort(400, "Require and Email account login to continue")

            if request.method == "POST":
                try:
                    self._confirm_password()
                    password = request.form.get("password")
                    password2 = request.form.get("password2")
                    if password != password2:
                        raise exceptions.AuthError("Passwords don't match")
                    elif utils.is_password_valid(password):
                        user_login.change_password(password.strip())
                        session_set_require_password_change(False)
                        flash_success("Password updated successfully!")
                        return redirect(self.account_info)
                    else:
                        raise exceptions.AuthError("Invalid password")
                except exceptions.AuthError as ex:
                    flash_error("Error: %s" % ex)
                    return redirect(self.change_password)
                except Exception as e:
                    logging.exception(e)
                    flash_error("Unable to change password")
                    return redirect(self)

        @shaft_deco.menu_title("Change Profile Image", order=4)
        @shaft_deco.accept_post_get
        def change_profile_image(self):
            page_meta(title="Change Profile Image")

            if request.method == "POST":
                file = request.files.get("file")
                if file:
                    name = "%s" % uuid.uuid4().hex
                    extensions = ["jpg", "jpeg", "png", "gif"]
                    my_photo = storage.upload(file,
                                              name=name,
                                              prefix="profile-images/",
                                              allowed_extensions=extensions)
                    if my_photo:
                        url = my_photo.url
                        current_user.update(profile_image_url=url)
                        flash_success("Profile Picture updated successfully!")
                return redirect(self.account_info)

        @shaft_deco.menu_title("Setup Login", visible=False)
        @shaft_deco.accept_post_get
        def setup_login(self):
            user_login = current_user.user_login("email")
            if user_login:
                return redirect(self.account_info)

            if request.method == "POST":
                try:
                    email = request.form.get("email")
                    password = request.form.get("password")
                    password2 = request.form.get("password2")

                    if not password.strip() or password.strip() != password2.strip():
                        raise exceptions.AuthError("Passwords don't match")
                    else:
                        new_login = models.AuthUserLogin.new(login_type="email",
                                                             user_id=current_user.id,
                                                             email=email,
                                                             password=password.strip())
                        if verify_email:
                            send_registration_welcome_email(new_login.user)
                            flash_success("A welcome email containing a confirmation link has been sent to your email")
                            return redirect(self.account_info)
                except exceptions.AuthError as ex:
                    flash_error(ex.message)
                    return redirect(self.setup_login)
                except Exception as e:
                    logging.exception(e)
                    flash_error("Unable to setup login")
                    return redirect(self)

    return AuthAccount



