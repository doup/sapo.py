pyvenv .
source bin/activate
pip3 install xxx

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt