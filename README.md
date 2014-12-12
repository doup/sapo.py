# Setup

## Virtual environment

Create virtual environment on project folder:

    $ pyvenv env

Activate environment (do it on every session, especially before installing new packages):

    $ source env/bin/activate

## Dependencies

Install requirements:

    $ pip install -r requirements.txt

Freeze the requirements (only after installing new packages):

    $ pip freeze > requirements.txt
