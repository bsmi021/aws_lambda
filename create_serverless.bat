sls create --template aws-python --path %1 && cd %1 && call ..\servless_plugins.bat && mkdir %2 && type null > %2\__init__.py
