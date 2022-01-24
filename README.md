[![codecov](https://codecov.io/gh/Jaspreet-singh-1032/open_analyse_backend/branch/master/graph/badge.svg?token=3R0VNJD9QP)](https://codecov.io/gh/Jaspreet-singh-1032/open_analyse_backend)

## openAnalyse is an open-source application that helps users to analyse how they are investing their time.

### Live Website : https://openanalyse.netlify.app/

**Frontend at** https://github.com/Jaspreet-singh-1032/openAnalyse-frontend

STILL IN DEVELOPMENT, CONTRIBUTIONS ARE WELCOME

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/Jaspreet-singh-1032/open_analyse_backend.git
```

and `cd` into the project directory:

```sh
cd open_analyse_backend/
```

Then install the dependencies. Make sure to first create a virtual environment and run:

```sh
pip install -r requirements.txt
```

Migrate the database:

```sh
python manage.py migrate
```

Then run the server:

```sh
python manage.py runserver
```

The server will be running at `http://127.0.0.1:8000/`

## Tests

To run the tests:

```sh
python manage.py test
```

## Coding style

This project follows [pep8](https://www.python.org/dev/peps/pep-0008/)
and [django coding styles](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)

Use [flake8](https://pypi.org/project/flake8/) to check for problems in this area.

Run:

```sh
flake8
```

Use [pre-commit hooks](https://pre-commit.com/) to identify simple coding issues before committing code:

To setup pre-commit hooks run:

```sh
pre-commit install
```
