# Cat Archive

*A cat:*

![cat](https://avatars2.githubusercontent.com/u/73047212?s=200&v=4)

Open-source, distributed, cat archive platform.

Work in progress.

## The client

To install, run `pip install .` inside of the repo.

To use, run:

```
catarchive -e <server:port> -t <token>
```

## The control server

To compile, `cd` into `server/control/` and run `go build`.

To start it, run:

```
./control -p <port> -t <token>
```
