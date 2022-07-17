FROM python:3.8-slim-buster
WORKDIR /workspace
COPY ./requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt
COPY . /workspace

ENTRYPOINT ["gunicorn"]
CMD ["app.views:app", "-w", "2", "--threads", "2", "--preload", "-b", "0.0.0.0:8000"]


