# Project's back-end
Requirements:
- Python 3.9.6
- pip-tools
- fastapi

Run these commands in your terminal to setup project in local.
```sh
python -m venv venv
source venv/bin/activate
make install
```

Run this command to start the server in dev environment.
```sh
make dev
```

Run this command to start the server.
```sh
make start
```

Run this command to start the service in docker environment
```sh
docker-compose up --build
```
To stop the service running in docker environment
```sh
docker-compose down
```