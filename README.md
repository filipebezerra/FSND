# Full-Stack Nanodegree projects

This public repository contains the products of my hard and determined work completing the Full-Stack Nanodegree program from Udacity.

## Fyyur: Artist Booking Site

> Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### The project

My job was to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

- Project URL: https://github.com/filipebezerra/FSND/tree/master/projects/01_fyyur/fyyur-app
- Built between December/19 and February/20

### Tech Stack:

- SQLAlchemy ORM library
- PostgreSQL database
- Python3 server language and Flask micro framework
- Flask-Migrate for creating and running schema migrations
- HTML, CSS, and Javascript with Bootstrap 3 for the website's frontend

## Trivia API

> Trivia API is the backend application that makes the Trivia web application works.

### The project

- Project URL: https://github.com/filipebezerra/FSND/tree/master/projects/02_trivia_api/trivia-api
- Built between March/20 and April/20

### Tech Stack:

- SQLAlchemy ORM library
- PostgreSQL database
- Python3 server language and Flask micro framework
- Flask-Migrate for creating and running schema migrations
- Unittest for unit and integration tests
- Swagger for documenting the API
- ReactJS for the website's frontend

## Coffee Shop Full Stack

> Coffee Shop is a new digitally enabled cafe for students to order drinks, socialize, and study hard.

### The project

- Project URL: https://github.com/filipebezerra/FSND/tree/master/projects/03_coffee_shop_full_stack/coffee-shop-full-stack-app
- Built between March/20 and May/20

### Tech Stack:

- SQLAlchemy ORM library
- PostgreSQL database
- Python3 server language and Flask micro framework
- python-jose for validating JWT
- Unittest for unit and integration tests
- Swagger for documenting the API
- Ionic for the website's frontend

### Learnings

The main challenge with this project it was to properly handle security concerns to user access and permissions using RBAC model and JSON Web Tokens (JWT for short) an open, industry standard RFC 7519.

Also integrating with Auth0 services to manage and authorize users within the application.

## Deploy Your Flask App to Kubernetes Using EKS

> Deploy Your Flask App to Kubernetes Using EKS was an practical hands on done for my Full Stack Developer formation in the Udacity's nanodegree program.

### The project

My job was to containerize and deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

- Project URL: https://github.com/filipebezerra/FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS
- Built between May/20 and June/20

### Tech Stack:

- Python3 server language and Flask micro framework
- Docker for containering the application
- Kubernetes for orchestrating the containers
- AWS EKS for the cluster
- AWS Systems Manager Parameter Store for securely storing secrets
- AWS CodePipeline pipeline triggered by GitHub (CD or Continuous Delivery)
- AWS CodeBuild for stage for building, testing, and deploying the code (CI or Continuous Integration)

### Learnings

The main challenge with this project it was to put all the pieces together since it's nothing trivial to automate all your software engineering processes, but in the end of the day having a full automated pipeline makes life easier.

## Capstone - TheCrew Casting Agency

> The TheCrew is a Casting Agency company that is responsible for creating movies and managing and assigning actors to those movies.

### The project

So TheCrew API is the backend application that serves and accepts JSON data for our applications and third-party applications.

- Project URL: https://github.com/filipebezerra/FSND/tree/feature/thecrew-capstone-solution/projects/capstone/thecrew_full_stack/thecrew-app-backend-api-python
- Built between August/20 and September/20

### Tech Stack:

- SQLAlchemy ORM library
- PostgreSQL database
- Redis NoSQL key/value database for caching API responses
- Python3 server language and Flask micro framework
- python-jose for validating JWT
- Unittest for unit and integration tests
- Swagger for documenting the API
- Bootstrap-Flask library for Bootstrap 4 helper for Flask/Jinja2
- Heroku where the applications is deployed

### Learnings

The main challenge with this project it was to build a real production-ready REST API.
