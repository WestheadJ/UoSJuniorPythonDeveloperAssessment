# UoS Junior Python Developer Assessment
This repository is for my application to the University of Sheffield junior python developer role. I have been given 3 tasks to develop on and this repository holds my solutions to the tasks given.

This README contains:

## Introduction
This assessment is designed to evaluate my core development and thinking skills
in a practical context. It includes three tasks followed by a written explanation of my
work. I have chose Python using 3 main libraries these are:
-  `FastAPI`
- `SQLite`
- `Pandas`

## Tasks

- Task 1 - Database Setup
- Task 2 - REST API
- Task 3 - ETL Script

### Task 1 - Database Setup

#### Brief:
> Write a script that creates tables in the database and the data (please refer to data
requirements section) is loaded into them.
The script should be repeatable so that running it again should not cause duplicates
or errors. You may use any database you are comfortable with.

##### Data Requirements:
> You are not provided with any data files. Part of this assessment is for you to create
your own sample data. Your data should represent a simple scenario involving
Customers and their Orders

> Guidelines:
> - You should have two datasets: Customers and Orders
> - Keep the data to a maximum of 50 rows per dataset.
> - Each Customer should have at least: a unique identifier, a first name, a surname, an email, and a status e.g., archived/active/suspended
> - Each Order should have at least: a unique identifier, a link to the customer who placed it, a product name, a quantity, and a unit price.
> - You are free to add any additional fields you think are useful.

### Task 2 - REST API
> Build a simple API on the data you loaded in Task 1. The API should have an endpoint that returns Customer and Order data for a single Customer, looked up by their customer id.

### Task 3 - ETL Script
> Write a standalone script that could be run on a schedule (for example, as a batch job or scheduled task). This script should query the database you created in Task 1 directly and carry out the following steps:
> - Extract - Query the database to retrieve all active customers along with their orders
> - Transform - Concatenate the first name and surname fields into a single name field. Calculate a total value for each order (quantity × unit price)
> - Export - Write the results to a CSV file saved in an output folder locally

## How to Run the Application

