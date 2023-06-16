FROM python:3.11


COPY ./ ./
CMD [ "ls" ]
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

