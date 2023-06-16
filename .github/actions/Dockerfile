FROM python:3.11
COPY ./ ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir PyGithub
RUN ls
ENTRYPOINT ["python", "BranchWrite/.github/actions/main.py"]