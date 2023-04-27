### (Fast)API

Run the app locally

`uvicorn api.main:app --reload`

Update the API on the web-server:

- Update the repository (master branch)

`git pull`

- Intall the package

`pip install .`

- Update gunicorn service

`sudo systemctl restart gunicorn`

Note: 

the gunicorn service is defined in `/lib/systemd/system/gunicorn.service`.
