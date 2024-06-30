# Project's back-end
Requirements:
- Python 3.9.6
- pip-tools
- fastapi

Run these commands in your terminal to setup project in local.
```sh
python -m venv venv
source venv/bin/activate
pip-sync
```

Run this command to start the server
```sh
fastapi run app/main.py
```