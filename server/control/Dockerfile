FROM golang:1.15

WORKDIR /go/src/control
COPY . .
RUN mkdir -p ./log

RUN go install .

ARG control_port=9908
ARG control_token=token

ENV CA_CONTROL_PORT=$control_port
ENV CA_CONTROL_TOKEN=$control_token

EXPOSE $port

CMD ["control"]
