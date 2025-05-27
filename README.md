# Bookstore API Automation

This project contains an automated test suite for the Online Bookstore REST API, implemented in Python 3.11 using Poetry, pytest, and JSON Schema validation.

## API Endpoints

### Books API

1. `GET  /api/v1/Books` – Retrieve a list of all books.
2. `GET  /api/v1/Books/{id}` – Retrieve details of a specific book by its ID.
3. `POST /api/v1/Books` – Add a new book to the system.
4. `PUT  /api/v1/Books/{id}` – Update an existing book by its ID.
5. `DELETE /api/v1/Books/{id}` – Delete a book by its ID.

### Authors API

1. `GET  /api/v1/Authors` – Retrieve a list of all authors.
2. `GET  /api/v1/Authors/{id}` – Retrieve details of a specific author by their ID.
3. `POST /api/v1/Authors` – Add a new author to the system.
4. `PUT  /api/v1/Authors/{id}` – Update an existing author’s details.
5. `DELETE /api/v1/Authors/{id}` – Delete an author by their ID.

## Prerequisites

* **Python 3.11** installed: download from [python.org](https://www.python.org/downloads/release/python-3119/).
* **Poetry** for dependency management: follow the [Poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer).
* **Git** for cloning the repository.

## Installation & Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/praetorio/bookstore.git
   cd bookstore
   ```
2. **Configure Poetry Environment**
    
    Follow the PyCharm guide [PyCharm Poetry Setup](https://www.jetbrains.com/help/pycharm/poetry.html#poetry-env) or different IDEs' documentation for setting up Poetry environments.

3. **Install dependencies**

   ```bash
   poetry install --no-root --no-interaction --only main
   ```

## Configuration

By default, the tests target `https://fakerestapi.azurewebsites.net`. To override:

```bash
export BOOKSTORE_API_URL="https://my-api.example.com"
```

## Running Tests

Run all tests with:

```bash
poetry run pytest
```
By default, this will generate a test report in `report.html` in the root directory. Open `report.html` in your browser for results.

If you want to change the output location, you can specify the `--html` option:

```bash
poetry run pytest --html=custom_location/custom_report_name.html
```

### Running Specific Tests

* **Books only**:

  ```bash
  poetry run pytest -m books
  ```
* **Authors only**:

  ```bash
  poetry run pytest -m authors
  ```

## Project Structure

```
bookstore/
├── README.md
├── pyproject.toml
├── poetry.lock
├── conftest.py
├── report.html
├── .gitignore
├── configs/
├── src/
│   ├── clients/
│   └── schemas/
├── tests/
│   ├── data/
│   │   ├── authors/
│   │   └── books/
│   ├── authors/
│   └── books/
├── utils/
└── .github/
    └── workflows/
```

## Extending & Maintenance

* **Add endpoints**: Update `src/clients/`, `src/schemas/`, and add tests under `tests/`.
* **Utilities**: Add reusable functions in `utils/`.
* **Configuration**: Modify `configs/` for environment-specific settings.
* **Test data**: Use `tests/data/` for JSON files containing test data
* **Custom markers**: Add to `pyproject.toml`.
