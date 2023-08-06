
# local settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

ALLOWED_HOSTS = ['localhost', 'peer', 'ws-eperez']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',      # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'peer',                     # Or path to database file if using sqlite3.
        'USER': 'peer',
        'PASSWORD': 'peer'
    }
}

TIME_ZONE = 'Europe/Madrid'

RECAPTCHA_PUBLIC_KEY = 'B3f9AMzXIRKf4g3P+i6DdlhEwPDktpwPXgIWIU84'
RECAPTCHA_PRIVATE_KEY = 'znBQ2p15czPwqtfc0INtZu9TJtc8Ya1ukwfhXAh3'

SAML_ENABLED = False
SAML_CONFIG = {}
REMOTE_USER_ENABLED = False

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
