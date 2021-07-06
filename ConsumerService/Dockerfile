FROM python:3.7-slim

ADD . /deploy

RUN cd /deploy && \
    pip install .
#     rm -rf /build /deploy
EXPOSE 8080

CMD ["consumer"]
