FROM snakepacker/python:all as builder

RUN python3 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /producer_app/
RUN /usr/share/python3/app/bin/pip install -Ur /producer_app/requirements.txt

COPY dist/ /producer_app/dist/
RUN /usr/share/python3/app/bin/pip install /producer_app/dist/* \
    && /usr/share/python3/app/bin/pip check

# api это target build stage
FROM snakepacker/python:3.10 as api

RUN mkdir -p /log/priceproducer && touch /log/priceproducer/log.txt

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/priceproducer-* /usr/local/bin/


# RUN if test -f "/log/priceproducer/log.txt"; then priceproducer-main &> /log/priceproducer/log.txt; else echo "No file"; fi
CMD ["ls -la"]

CMD ["/usr/local/bin/priceproducer-main"] 