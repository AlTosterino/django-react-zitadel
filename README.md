# Django + React + Zitadel Example

This repository shows bare minimum for integrating Zitadel with Django and React

> Note that this is just an example, source code is not in the best shape

## Prerequisites
- Docker and docker-compose

## Running
- Run `docker-compose up`

## Configuring Zitadel

- Open `localhost:8080` 
- Login with:
  - Username: zitadel-admin@zitadel.localhost
  - Password: Password1!
- Open `Create Project`
- Name your project e.g. `Test`
- Click on `+` box to create new application
- Name your application e.g. `React`
- Choose `User Agent`
- Click `Continue`
- Choose `PKCE`
- Click `Continue`
- Put `http://localhost:5173/` into URLs
- Click `Continue` and `Create`
- Save client secret and put it into `clientId` under `frontend/src/main.jsx` at line 8
- Go to `Projects -> YOUR PROJECT NAME -> YOUR APP NAME -> Redirect Settings`
- Enable `Development Mode`
- Go back to `Projects` and choose `YOUR PROJECT NAME`
- Click on `+` box to create new application
- Name your application e.g. `Backend`
- Choose `API`
- Click `Continue`
- Choose `Basic`
- Click `Continue` and `Create`
- Copy `ClientId` and `ClientSecret` and put them in `docker-compose.yml` under `api` service

Now you are ready to open `http://localhost:5173` to play with React app