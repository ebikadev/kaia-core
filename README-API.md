# Kaia Data Validator — API Fundamentals

## Introduction

This document explains one of the most important concepts behind the Kaia Data Validator architecture: **APIs**.

Understanding APIs is essential not only for backend development but also for **data engineering systems**, because most modern data platforms communicate through APIs.

This document explains:

* What an API is
* Why APIs are used in modern systems
* How APIs work internally
* How a request travels through the backend
* Why the Kaia Data Validator uses an API architecture
* Real-world companies that build similar solutions for data validation

The goal is to provide a **clear mental model** of how APIs work in real production systems.

---

# What is an API?

API stands for **Application Programming Interface**.

An API is a **controlled interface that allows different systems to communicate with each other**.

Instead of interacting directly with a database or backend code, external systems interact through **well-defined endpoints** exposed by the API.

In simple terms:

An API is the **doorway to your system**.

It receives requests, executes logic, and returns responses.

---

# Example of API Communication

When a client system needs to interact with the backend, it sends an HTTP request.

Example:

POST /validation

The API receives this request, processes the file, and returns a response.

Example response:

```
{
  "filename": "sales.csv"
}
```

The client does not need to know how the validation works internally.
It only needs to know **how to call the API**.

---

# Why APIs are used in modern software

Modern systems are built using **separation of responsibilities**.

Instead of one monolithic application, systems are divided into layers:

```
User Interface (Frontend)
        │
        ▼
API Layer
        │
        ▼
Backend Logic
        │
        ▼
Database / Storage
```

This architecture allows:

* Independent development
* Easier scaling
* Integration with other systems
* Automation and pipelines

For example, a data pipeline could send files to Kaia through the API before loading them into a data warehouse.

---

# APIs in Data Engineering

APIs are widely used across the data ecosystem.

Examples include:

* Google BigQuery — query and ingestion APIs
* Google Analytics — reporting API
* Apache Airflow — orchestration APIs
* Snowflake — SQL and data ingestion APIs

Many pipelines work like this:

```
Extract data → send to API → validate → load to warehouse
```

The API acts as the **integration layer** between systems.

---

# Endpoints

An **endpoint** is a specific route of the API that performs an action.

Examples from Kaia:

GET /health
POST /validation

Each endpoint corresponds to a function in the backend.

Example:

```
@router.get("/health")
```

This means:

When a request arrives at `/health`, the associated function will execute.

---

# HTTP Methods

APIs use the HTTP protocol.

Common methods include:

GET — retrieve information
POST — create or submit data
PUT — update data
DELETE — remove data

Example:

GET /health
POST /validation

---

# FastAPI

The Kaia backend is built using FastAPI.

FastAPI is responsible for:

* receiving HTTP requests
* mapping them to Python functions
* validating inputs
* generating responses
* automatically generating API documentation

---

# Uvicorn

The application runs on Uvicorn.

Uvicorn is the server that:

* opens a network port
* listens for requests
* forwards them to the FastAPI application

The server is started using:

```
uvicorn app.main:app --reload
```

Explanation:

app.main → module where the application is defined
app → FastAPI instance
--reload → reloads automatically during development

---

# How a Request Travels Through the Backend

One of the most important concepts when learning APIs is understanding **how a request moves inside the system**.

Most tutorials stop at the endpoint, but real systems have multiple layers.

In Kaia the request flow looks like this:

```
Client
   │
   ▼
API Endpoint
   │
   ▼
Router
   │
   ▼
Service Layer
   │
   ▼
Database / Storage
```

Let's break this down step by step.

---

# Step 1 — Client Sends Request

The process begins when a client sends a request to the API.

Example:

POST /validation

The request may include a file upload.

---

# Step 2 — FastAPI Receives the Request

FastAPI receives the request and matches the URL with the correct endpoint.

Example:

```
@router.post("/validation")
```

If the route matches, FastAPI calls the corresponding function.

---

# Step 3 — Endpoint Executes

The endpoint receives the data from the request.

Example:

```
async def validate_file(file: UploadFile = File(...)):
```

This function is responsible for orchestrating the operation.

However, in well-designed systems, the endpoint **does not contain the business logic**.

Instead, it calls a service.

---

# Step 4 — Service Layer

The service layer contains the core business logic.

In the future, Kaia's validation engine will live here.

Example:

```
services/validation_service.py
```

This layer may:

* parse the file
* validate schema
* detect missing values
* check data types

---

# Step 5 — Database or Storage

If needed, the service may store results in a database or storage system.

Examples:

* validation reports
* uploaded files
* audit logs

---

# Step 6 — Response Returned

After processing is complete, the API returns a response to the client.

Example:

```
{
 "errors": [
   "column 'price' missing",
   "invalid date format"
 ]
}
```

The client receives the result and decides what to do next.

---

# Why This Architecture Matters

Separating the API into layers provides major benefits.

It makes the system:

Maintainable
Testable
Scalable
Extensible

For example, the validation engine can evolve independently from the API.

---

# Real Companies Solving Data Validation Problems

The problem Kaia is solving already exists in many companies.

Data validation and data quality are major challenges in modern data platforms.

Some companies that provide similar solutions include:

### Great Expectations

An open-source framework used to validate datasets.

Used by data teams to ensure data quality in pipelines.

---

### Soda Data

A platform focused on monitoring and validating data in warehouses.

Provides automated data checks and alerts.

---

### Monte Carlo

A data observability platform that detects anomalies in pipelines and datasets.

---

# How Kaia is Different

Many tools validate **data already inside the warehouse**.

Kaia aims to validate **data before it enters the system**.

This is extremely valuable because many issues originate at the **data input stage**.

---

# Real Problem Kaia Solves

Many companies rely on Excel or spreadsheets for data entry.

Users often enter inconsistent data.

Examples include:

wrong formats
missing values
incorrect column names
mixed data types

These errors break downstream systems such as BI dashboards.

For example:

Power BI dashboards may fail if the dataset schema changes.

---

# Kaia's Proposed Solution

Kaia can provide a controlled interface for data input.

Instead of allowing users to modify raw spreadsheets, the system would provide a UI where users input data.

The system validates the data before allowing submission.

Possible architecture:

```
User Interface
      │
      ▼
Kaia API
      │
      ▼
Validation Engine
      │
      ▼
Database or Structured Dataset
      │
      ▼
Power BI Dashboard
```

If the user enters invalid data, the system immediately blocks the submission.

This prevents data quality problems from propagating through the data pipeline.

---

# Possible Future Capabilities

Kaia could eventually support:

- schema validation
- data type enforcement
- missing value detection
- data lineage
- dataset versioning
- audit logs

This would position the system as a **data quality gateway** for analytics pipelines.

---

# Summary

An API is the **communication interface of a system**.

In the Kaia Data Validator architecture, the API acts as the bridge between users, applications, and the validation engine.

Understanding how requests move through the backend — from endpoint to service to storage — is fundamental for designing scalable and maintainable systems.

Kaia's API architecture allows the system to integrate easily with user interfaces, pipelines, and analytics platforms, making it a powerful foundation for a data validation platform.
