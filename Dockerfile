FROM python:3.12.1


COPY ./app  /root/app
COPY ./requirements.txt /root/app/requirements.txt
WORKDIR /root/

RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
