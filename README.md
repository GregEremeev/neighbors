## Implementation for task `find nearest neighbors`

### API

    GET|POST /api/v1/users/
    GET|PATCH|DELETE /api/v1/users/:id/
    GET /api/v1/users/:id/nearest_neighbors/?limit=n&radius=k

### Installation for development (ubuntu-16.04)

##### Install prerequisites

    sudo apt-get install python3-dev git python3-pip python3-venv;
    sudo apt-get install postgresql postgresql-contrib postgis libpq-dev;

##### Generate locale

    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    sudo dpkg-reconfigure locales

##### Clone repository

    git clone <address of repository>
    cd neighbors

##### Create .gitignore

    .gitignore
    __pycache__/
    local
    *.py[cod]
    *.mo

##### Create database

    sudo -u postgres psql << EOF
    CREATE USER neighbor WITH SUPERUSER CREATEDB UNENCRYPTED PASSWORD 'neighbor';
    CREATE DATABASE neighbors OWNER neighbor;
    EOF

##### Create and activate virtual environment

    python3 -m venv ~/neighbors_venv
    source ~/neighbors_venv/bin/activate

##### Create local configuration file ./local/neighbors_settings.py in root directory with the following content

    mkdir local
    cat << EOF > ./local/neighbors_settings.py
    DEBUG = True
    SECRET_KEY = 'your_secret_key'

    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
    DATABASES['default']['NAME'] = 'neighbors'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['USER'] = 'neighbor'
    DATABASES['default']['PASSWORD'] = 'neighbor'

    EOF

##### Run upgrade commands

    pip install --upgrade -e .
    python -m neighbors.manage migrate --noinput


### Start services

##### Run Django development server

    python -m neighbors.manage runserver

##### Run tests

    python -m neighbors.manage test -v 2
