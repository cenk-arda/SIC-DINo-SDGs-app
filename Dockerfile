FROM python:3.8-slim-buster
WORKDIR /workspace
COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /workspace

ENTRYPOINT ["gunicorn"]

# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["app.views:app", "-w", "1", "--threads", "8", "--preload", "-b", "0.0.0.0:8000", "-t", "0"]