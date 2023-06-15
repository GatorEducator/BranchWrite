FROM python:3.11


COPY requirements.txt ./
COPY main.py .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt



CMD [ "python", "main.py", "insight", "cool/insight.json", "branch-and-path", "main/README.md" ]