**Python Flask Login Demo** 

# How to setup  - Requires conda to be installed for the enviroment.

* Type `conda env create --file environment.yaml`
* Edit 'config.yml' and add email address and 'App password' (default gmail config)

# How to setup

1) type `export FLASK_APP=app`
1) type `flask shell`
1) type `from app import db, Username`
1) type `db.create_all()`
1) Press CTRL-D
1) `flasklogin.sqlite3` created in folder `flaskdemologin/instance`

# How to Run
* Type `flask run`
* using a web browser on the local machine visit `http://127.0.0.1:5000`
