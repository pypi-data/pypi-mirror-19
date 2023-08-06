# Shaft

import os

# ------------------------------------------------------------------------------
# A convenient utility to access data path from your application and config files

# The application directory
# /apps
APP_DIR = os.path.dirname(__file__)

# Data directory
# apps/var
VAR_DIR = os.path.join(APP_DIR, "var")


def get_var_path(path):
    """
    get the path stored in the 'apps/var' directory
    :param path: string
    :return: string
    """
    return os.path.join(VAR_DIR, path)

# ------------------------------------------------------------------------------
#
# AVAILABLE APPS
# Dict of available apps to be used in your app config
# To activate apps, just place each one of them in the
# INSTALLED_APPS config. ie
#
# INSTALLED_APPS = [
#     AVAILABLE_APPS["ERROR_PAGE"],
#     AVAILABLE_APPS["AUTH"],
#     ...
# ]
#
# The order is important. If an app depends on another app to work
# that must be placed before the calling app.
#
# Multiple app config of the same app can also be set to be used by different
# app. ie:
#
# AVAILABLE_APPS = {
#     "AUTH_ADMIN": {...},
#     "AUTH_WWW": {...}
# }
#
#
# INSTALLED_APPS = [
#     AVAILABLE_APPS["AUTH_WWW"],
#     ...
# ]
#
#

AVAILABLE_APPS = {
    # Error Page. Create a friendly page when an error occurs
    "ERROR_PAGE": "shaft.contrib.error_page",

    # Maintenance page. When uncommented, the whole site will show a maintenance page
    "MAINTENANCE_PAGE": "shaft.contrib.maintenance_page",

    "AUTH":
    # AUTH: Authentication system to signup, login, manage users,
    # give access etc
    # Require to run `shaft syncdb` to setup the db
    # Also, run once `shaft auth:create-super-admin email@xyz.com` to
    # create the super admin
        {
            "app": "shaft.contrib.auth",
            "modules": {
                "login": {
                    "route": "/account/",
                    "nav_menu": {
                        "title": "Signin",
                        "align_right": True
                    }
                },
                "account": {
                    "route": "/account/",
                },
                "admin": {
                    "route": "/admin/users/"
                }
            },
            "options": {
                # for login and logout view
                "login_view": "Index:index",
                "logout_view": "Index:index",

                # permission
                "allow_register": True,
                "allow_login": True,
                "allow_social_login": False,

                # Verification
                "verify_email": False,
                "verify_email_token_ttl": 60 * 24,
                "verify_email_template": "verify-email.txt",
                "verify_signup_email_template": "verify-signup-email.txt",

                # reset password
                "reset_password_method": "token",  # token or password
                "reset_password_token_ttl": 60,  # in minutes
                "reset_password_email_template": "reset-password.txt",

                # # When a user is required to change password, list endpoints
                # # that could still be accessed without requiring password
                # # change page
                # "require_password_change_exclude_endpoints": []
            }
        },
    "CONTACT_PAGE":
    # CONTACT PAGE: Creates a page for users to contact admin.
    # MAIL_* config must be setup
        {
            "app": "shaft.contrib.contact_page",
            "route": "/contact/",
            "nav_menu": {
                "title": "Contact",
                "visible": True,
                "order": 100
            },
            "options": {
                "title": "Get in touch!",
                "return_to": "Index:index",
                "recipients": "",
                "template": "contact-us.txt",
                "success_message": "Thank you so much for sending this message. "
                                   "We'll contact you within the next 72 hours"
            }
        },

    "ADMIN":
    # ADMIN: Creates and admin interface for the application.
    # Use when creating admin site
        {
            "app": "shaft.contrib.admin",
            # For additional roles in the whole admin page, uncomment below
            #"decorators": ["shaft.contrib.auth.accepts_manager_roles"],
            "options": {
                "brand": "The Admin",
                "theme": "yeti"  # Recommended: yeti, superhero, amelia
            }

        },

    "APP_DATA": {
        "app": "shaft.contrib.app_data",
        "modules": {
            "admin": {}
        }
    }
}

