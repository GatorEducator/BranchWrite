FROM python:3.11
COPY ./ ./
WORKDIR .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir PyGithub


ENTRYPOINT ["python", "main.py"]