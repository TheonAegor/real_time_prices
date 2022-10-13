FROM snakepacker/python:all as transfer_builder

RUN python3 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /transfer_app/
RUN /usr/share/python3/app/bin/pip install -Ur /transfer_app/requirements.txt

COPY dist/ /transfer_app/dist/
RUN /usr/share/python3/app/bin/pip install /transfer_app/dist/* \
    && /usr/share/python3/app/bin/pip check

FROM snakepacker/python:3.10 as transfer_api

RUN mkdir /logs/

COPY --from=transfer_builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/pricetransfer-* /usr/local/bin/

CMD ["/usr/local/bin/pricetransfer-api"] 