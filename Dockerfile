FROM python:3

RUN mkdir /sber_test

COPY poetry.lock pyproject.toml /

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./ /sber_test

WORKDIR /sber_test/app
RUN python manage.py migrate

CMD ["python3", "manage.py", "runserver", "0:8000"]