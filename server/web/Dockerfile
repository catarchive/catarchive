FROM golang:1.15

WORKDIR /go/src/web
COPY . .
RUN mkdir -p ./log

RUN go install .

ARG web_port=8000

ENV CA_WEB_PORT=$web_port

EXPOSE $web_port

CMD ["web"]
