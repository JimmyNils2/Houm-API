# Houm API Project

This repository contains an API for managing employees, properties, and visits at Houm.

## Installation

To install dependencies, use Poetry:

```bash
poetry install
```
## Run Development Server
To run the development server with auto-reload, use Uvicorn:

```bash
uvicorn main:app --reload
```

## API Documentation
You can access the API documentation at the following links:

- [Redoc API Documentation](http://127.0.0.1:8000/redoc)
- [Swagger UI API Documentation](http://127.0.0.1:8000/docs)

## Endpoints
### Employees
- `GET` /employees: Get all employees.
- `GET` /employees/{employee_id}: Get an employee by ID.
- `POST` /employees: Create a new employee.
- `DELETE` /employees/{employee_id}: Delete an employee by ID.
- `PATCH` /employees/{employee_id}: Update an employee by ID.
- `GET` /employees/{employee_id}/report: Get report about employee visits.
### Properties
- `GET` /properties: Get all properties.
- `GET` /properties/{property_id}: Get a property by ID.
- `POST` /properties: Create a new property.
- `DELETE` /properties/{property_id}: Delete a property by ID.
- `PATCH` /properties/{property_id}: Update a property by ID.
### Visits
- `GET` /visits: Get all visits.
- `GET` /visits/{visit_id}: Get a visit by ID.
- `POST` /visits: Create a new visit.
- `DELETE` /visits/{visit_id}: Delete a visit by ID.
- `PATCH` /visits/{visit_id}: Update a visit by ID.

### Database Configuration
Make sure you have PostgreSQL installed and configured with the following details:

- **Host**: localhost
- **User**: postgres
- **Database**: houm
- **Password**: postgres
- **Port**: 5432


## Test
```bash
pytest
```