FROM python:3.7-slim

ADD . /deploy

RUN cd /deploy && \
    pip install .

RUN chmod -R 777 /deploy
#    rm -rf /build /deploy
CMD ["publisher"]
