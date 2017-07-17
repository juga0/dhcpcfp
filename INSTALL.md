Install dhcpcfp
=================

Installation in Debian testing/sid or Ubuntu XXX
-------------------------------------------------

Use your favorite package manager or run:
    sudo apt install dhcpcfp

Installation in Debian/Ubuntu from source code
----------------------------------------------

### Install system dependencies

    sudo apt install python-dev

### Install dhcpcfp dependencies with virtualenv

#### Obtain virtualenv

Check <https://virtualenv.pypa.io/en/latest/installation.html> or if
Debian equal/newer than Jessie (virtualenv version equal or greater than
1.9), then:

    sudo apt install python-virtualenv

#### Create a virtual environment

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/dhcpcfpenv source
    ~/.virtualenvs/dhcpcfpenv/bin/activate

#### Install dependencies in virtualenv

    git clone https://github.com/juga0/dhcpcfp
    cd dhcpcfp
    pip install -r requirements.txt

or run:

    python setup.py install

or run:

    pip install dhcpcfp
