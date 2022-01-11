# Context

We have deployed a (**remote**) Mock CRUD **API**, with the following models structure:

![Screenshot 2022-01-10 at 11.31.10.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9021aa0f-c95f-4ce1-aacd-ee5ad066b95f/Screenshot_2022-01-10_at_11.31.10.png)

The root URL will be provided you by one of our colleague.

Each model (Campaigns, Adsets, Keywords) has the following URL conventions:

- Read all: `GET /campaigns`
- Read one: `GET /campaigns/:id`
- Create one: `POST /campaigns`
- Update one: `PUT /campaigns/:id`
- Delete one: `DELETE /campaigns/:id`

# Requirements

- Create a Github project, with a **MongoDB** backend and **MongoEngine** as ORM
- Create the MongoDB (**local**) **models** corresponding to the models above
- Create a **sync down recurring process** (cron-like), that would query the remote API and backport changes in remote, to local models
  - Add **tests** for that
- Add a way to support that **local changes** (done by local users) can be **backported** to the remote API
  - In practice: be able to tell what model was changed - so we can backport said changes to remote
  - Add **tests** for that

# Time limit

We’ll ask you to not spend more than 4 hours
