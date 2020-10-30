FROM golang:1.15

WORKDIR /go/src
RUN git clone https://github.com/chrislusf/seaweedfs
WORKDIR /go/src/seaweedfs
RUN make install

EXPOSE 9333
EXPOSE 19333

CMD ["weed", "master"]
