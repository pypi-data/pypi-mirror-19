# `django-declaration-middleware`

Django application to force users to accept a declaration before accessing a set of urls.

## Usage

As well as adding the app to the projects settings file.
You will need to add a variable `PROTECTED_URL_PATTERNS`.
example:
    `PROTECTED_URL_PATTERNS = ['^']`

The url to include is `url('', include('declaration.urls', namespace='declaration')),`
and you will need to add `'declaration.middleware.DeclarationMiddleware',` to the end of the middleware list.
