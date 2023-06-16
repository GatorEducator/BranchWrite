FROM python:3.11
COPY ./ /app


RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir PyGithub


ENTRYPOINT ["python", "/app/main.py"]