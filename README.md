# Cat Archive

![cat](https://avatars2.githubusercontent.com/u/73047212?s=200&v=4)

Open-source, distributed, cat archive platform.

Work in progress.

## The client

To install, run `python3 -m pip install .` inside of the repo.

To use, run:

```
catarchive -e <server:port> -t <token>
```

If you have trouble installing due to PyTorch, go to [pytorch.org](https://pytorch.org/get-started/locally/) and follow their guide to install PyTorch for your specific setup.
After installing PyTorch you can rerun the `pip` command to install the client.

## The server stack

The server stack is comprised of four main services:

- Client control server
- PostgreSQL database server
- SeaweedFS master server
- Web server

This entire stack can be seamlessly deployed and managed with Docker Compose.

### Quickstart guide (Linux)

You will need Docker Compose and PostgreSQL (for the `psql` client) installed.

With most Linux package managers these are called `docker-compose` and `postgresql`, respectively.

```bash
git clone https://github.com/catarchive/catarchive
cd catarchive/server
cp default.env .env
vim .env # edit the .env file to set some required configuration
docker-compose build
docker-compose up -d # all the containers should start (run 'docker ps' to see them)
psql -h localhost -U catarchive <rc.sql # create the schema and table for the database
```

When running any `docker-compose` commands you must be root, or in the `docker` group.
