# Engine
Engine is a custom CMS project built using Wagtail with additional modifications such as predefined page models and StreamField blocks.

Speed and efficiency are the main objectives. The aim is to build the fastest and most lightweight project, future projects can be built on top of Engine.

## Installation
### Prerequisites
Must have an installation of CPython 3.9 for best compatibility, newer Python installations can be used provided you check whether the code and dependencies are compatible. 

Remember to use a virtual environment before installing packages!

```python
pip install -r requirements.cpython.txt
```

## Usage
### Engine as a Template
This repository should be used as a template for others. The following have to be done before the project has started:

1. Create a new repository on Github using this repository as the template.
2. Make sure you have a compatible Python installation and starts a virtual environment
3. Install dependencies in requirements.txt (see Prerequisites)
4. Modify `__license__`, `__copyright__` and `__client__` in `engine/__init__.py`
5. Modify content in `engine/templates/engine/` (things like license, contact info, etc)

### Development
#### Making core changes
Core functionalities can be added/modified/removed depending on the clients' requirements. It's best not to remove any functionalities unless it is really needed as Engine only provides the bare minimum to have a basic website.

Engine provides basic HTML templates which are built using Bootstrap CSS. These templates need to be modified to fit the clients' requirements. It is best to use Bootstrap CSS as this is the easiest CSS library, but others can be used if really needed.

#### Running the development server

Engine can be run any time during development for any form of testing. When you've just clones the repository and the `db.sqlite` file is not in the root directory, you need to run the following:

```shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The `migrate` command syncronises any created migrations into the database, a database is created if one doesn't exist.

The `createsuperuser` command creates a user with administrative privileges. This user should only be used for testing and a different user should be created during production deployment.

The `runserver` command simply runs a Django development server. This server is only used in the development environment, during production, a different server will be used to serve the project.

After you make any changes which affect the database, make sure you run:

```shell
python manage.py makemigrations
python manage.py migrate
```
The `makemigrations` command creates migration files which the `migrate` command uses to create/modify/delete tables in the database. Always run `makemigrations` before `migrate` to not run into any issues or errors.

## Roadmap
- [x] v1.0.0-dev
- [ ] Non-critical fixes to code (See v1.0.0 dev project board)
- [ ] Production test and deploy v1.0.0
