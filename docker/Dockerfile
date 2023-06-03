FROM python:3.11.3-bullseye

WORKDIR /grau_app

# Copying the files needed to install the grau app package
COPY env.py app.py pyproject.toml MANIFEST.in requirements.txt ./
COPY grau ./grau

# Installing the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Installing the grau app package
RUN pip install .

# Copying the files needed to create the database
COPY alembic ./alembic
COPY alembic.ini ./

# On container start run
# 1) Run env.py to update alembic db_url
# 2) Running the server
CMD python env.py &&  alembic upgrade head && flask run --host=0.0.0.0
