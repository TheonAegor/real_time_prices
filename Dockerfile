FROM snakepacker/python:all as builder

RUN python3 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /transfer_app/
RUN /usr/share/python3/app/bin/pip install -Ur /transfer_app/requirements.txt

COPY pricetransfer /transfer_app/app

WORKDIR /transfer_app/