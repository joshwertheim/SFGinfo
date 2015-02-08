# SFGinfo
Source for SF Giants web application hosted on Google App Engine.

Currently built using Google's webapp2 framework and Python. Code is loosely based on my earlier [sandlotbot](https://github.com/joshwertheim/sandlotbot) project.

Still very much a work in progress. I'm planning to make it look a lot nicer. It'll also be much more functional than just a simple news reader.

Upon opening, its root index is simple with just two links. One goes to the news page and the other goes to the roster page.

#### Libraries & Frameworks

Python:
* [webapp2](https://webapp-improved.appspot.com/)
* [jinja2](http://jinja.pocoo.org/docs/dev/)

HTML/CSS:
* [Bootstrap](http://getbootstrap.com/) 

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

- url: /.*
  script: main.application
```
