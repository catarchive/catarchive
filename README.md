# Cat Archive

![cat](https://avatars2.githubusercontent.com/u/73047212?s=200&v=4)

Open-source, distributed, cat archive platform.

Work in progress.

## The client

To install, run `pip install .` inside of the repo.

To use, run:

```
catarchive -e <server:port> -t <token>
```

## The server stack

The server stack is comprised of three main elements:

- Client control server
- PostgreSQL database server
- Web server

Note that image storage takes place separately, in a distributed file store.

This entire stack can be seamlessly deployed and managed with Docker Compose.

### Quickstart guide (Linux)

You of course need `docker-compose` installed. You will also need `postgresql` in order to use the `psql` client for initializing a table (see last command).

```bash
git clone https://github.com/catarchive/catarchive
cd catarchive/server
cp default.env .env
vim .env # edit the .env file to set some required configuration
docker-compose build
docker-compose up -d # all the containers should start up (run 'docker ps' to see them)
psql -h localhost -U catarchive <rc.sql # create the schema and table for the database
```

Note that when running any `docker-compose` commands you must be root, or in the `docker` group.
