# Task 1

## Task 1: Neural Network Development

Develop a simple neural network in Python using TensorFlow or any other machine learning framework of your choice. The network should be able to classify images from the MNIST dataset.

Train your model and assess its performance. Provide a report that includes accuracy and loss metrics.

Describe how you set up and trained your model, and explain the parameters you chose and why.

## Task 2: Working with Databases

Create a simple SQL or noSQL database (based on your preference) and write a Python script to interact with it.

Your script should be capable of adding, retrieving, updating, and deleting data.

Explain how you organized your database and why you chose such a structure.


## Task 3: Integration with Google API

Write a Python script that uses a Google API to fetch information. It can be any API you prefer to work with (e.g., Google Maps, Google Analytics, Google Sheets, etc.).

Your script should be able to send requests to the API and process the received data.

Explain how you structured your code and the approaches you chose for data processing.


## Task 4: Documentation

Write comprehensive documentation for each of the previous tasks. The documentation should include a description of what your code does, how to install and use it, and any other important details the user should know.


# Task 2

## Book Service API

### Overview

This project is a Python-based Book Service API designed for a Python/ML position. The Book Service API manages entities such as Books, Authors, and Clients, providing various API methods for tasks like adding/editing books, retrieving book lists, managing authors and clients, and handling book borrowing.

### Entities

#### Books
- **Book Title**
- **Author** (Additional attributes can be added as needed)

#### Authors
- **Full Name** (Additional attributes can be added as needed)

#### Client
- **Full Name** (Additional attributes can be added as needed)

### API Methods

1. **Add a Book**
2. **Edit Book**
   - Edit the book's title and author.
3. **Retrieve Books**
   - Retrieve a list of books with filtering options for:
     - The first letter of the book's title.
     - Author.
4. **Add Multiple Books by the Same Author**
5. **Add an Author**
6. **Create a Client**
7. **Retrieve Borrowed Books**
   - Retrieve a list of books borrowed by the client.
8. **Link/Unlink a Client to/from a Book**
   - Link a client to a book (client borrowed the book).
   - Unlink a client from a book (client returned the book).

### Considerations

- Authors stored in a separate PostgreSQL database table.
- API secured using an access token (Bearer authentication).
  - Token list can be static.
- Retrieve books borrowed by the client based on the access token.
  - Client identification based on the provided access token.
- Entire infrastructure deployed in Docker.

### Technologies

- **postgreSQL**
- **fastapi**
- **docker**


