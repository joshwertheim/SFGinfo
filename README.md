# SFGinfo
Source for SF Giants web application hosted on Google App Engine.

Currently built using Google's webapp2 framework and Python. Code is loosely based on my earlier [sandlotbot](https://github.com/joshwertheim/sandlotbot) project.

Still very much a work in progress. I'm planning to make it look a lot nicer. The code could definitely use refactoring. A couple points of interest to work on are the current 'player' module and the method in main.py responsible for re-loading player entities.

Upon opening, its root index is simple with just two links. One goes to the news page and the other goes to the roster page.

The roster page can currently handle a couple interesting situations:

1. When new versions of the app are uploaded to Google App Engine, there is code to check if Player entities already exist in the datastore and will use them without any other operations required.
2. As the data is being downloaded from MLB, there will be times when MLB's data is more current than what is currently stored in the App Engine datastore. To handle this scenario, a cron job has been set up to run every day at 3:30AM. Its task is to delete all Player entities in the datastore, and then run the relevant operation to download and store new data.

#### Libraries, Frameworks & and Tools 

Python:
* [webapp2](https://webapp-improved.appspot.com/)
* [jinja2](http://jinja.pocoo.org/docs/dev/)

Database:
* [Google Cloud Datastore (NoSQL)](https://cloud.google.com/datastore/docs)

Current hosted app can be found at:
[https://sfg-info.appspot.com/](https://sfg-info.appspot.com/)

### Note

This is the current app.yaml with application id censored:

```
application: ******
version: 1
runtime: python27
api_version: 1
threadsafe: true

libraries:
- name: webapp2
  version: latest
- name: jinja2
  version: latest

handlers:
- url: /static
  static_dir: static
  secure: always
- url: /js
  static_dir: js
  secure: always

- url: /.*
  script: main.application
```

This is the current cron.yaml with cronjob path censored:

```
cron:
- description: refresh cache
  url: /**********
  schedule: every day 03:30
  timezone: America/Los_Angeles
```
