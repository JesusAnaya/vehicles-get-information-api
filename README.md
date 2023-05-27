
## Vehicles Get Information API

For this exercise, I wanted to use a soft implementation of the design pattern Hexagonal (Ports & Adapters) Architecture.

In this version, the application comprises 3 layers split into different Python modules.

The API module contains the code referred to as the interface layer, also called the primary adapter, under the hexagonal pattern. Here is all the logic for exposing the services by a REST API, for this case, using Fast API. No other logic different from the implementation of a web interface layer is added to this module.

The db module contains the code called the infrastructure layer, also called the secondary adapter. Here is all the logic for interacting with the database, for this case, using SQLAlchemy.

The resources module is part of the secondary adapter, here could be included different interfaces to communicate with external services, like the vPIC API.

The services module for this application is where most of the business logic is implemented. Here, the application is decoupled from the infrastructure and interface layers. This way, changing the interface layer to a GraphQL, or gRPC communication, for example, doesn't require changes in the business logic.

The tests are separated into their module. This way, they can be easily identified and run for different purposes, like CI/CD, for example, and they could be excluded simply from the production package generated after the deployment process.

### Requirements

The application was developed using Python 3.9.1, and the dependencies are managed using pipenv. To install the dependencies, run the following command:

```bash
pipenv install
```

### Run the application

```bash
uvicorn main:app --port 8000 --reload
```

### Call the different endpoints

Retrieve information about a vehicle by VIN

```bash
curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/lookup/1XP5DB9X7YN526158
```

Delete a vehicle by VIN from the cache and database

```bash
curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/remove/1XP5DB9X7YN526158
```

Export all vehicles from the cache and database

```bash
curl -X GET -H "Content-Type: application/json" --output /tmp/file.parquet http://localhost:8000/api/v1/export
```

### Review the documentation

```bash
http://localhost:8000/docs
```

### Run tests

```bash
pytest -v tests/
```

My contact information is:

- Email: [jesus@armandoanaya.com](mailto:jesus@armandoanaya.com)
- LinkedIn: [https://www.linkedin.com/in/jesusanaya/](https://www.linkedin.com/in/jesusanaya/)
