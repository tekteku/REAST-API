# Library REST API Testing

## Test Structure

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests
│   ├── test_book_repository.py
│   ├── test_member_repository.py
│   ├── test_loan_repository.py
│   └── test_loan_service.py
└── integration/                # Integration tests
    ├── test_books_endpoints.py
    ├── test_members_endpoints.py
    └── test_loans_endpoints.py
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/unit/test_book_repository.py
```

### Run specific test class
```bash
pytest tests/unit/test_book_repository.py::TestBookRepository
```

### Run specific test
```bash
pytest tests/unit/test_book_repository.py::TestBookRepository::test_create_book
```

### Run with coverage report
```bash
pytest --cov=app tests/
```

### Run only unit tests
```bash
pytest tests/unit/
```

### Run only integration tests
```bash
pytest tests/integration/
```

## Test Coverage

### Unit Tests

**Book Repository** (11 tests)
- Create, read, update, delete books
- Search functionality
- Pagination
- Availability filtering

**Member Repository** (10 tests)
- Create, read, update, deactivate, activate members
- Search functionality
- Email uniqueness
- Active/inactive filtering

**Loan Repository** (9 tests)
- Create loans
- Get active/overdue loans
- Return books
- Loan history

**Loan Service** (10 tests)
- Business logic validation
- Max loans per member (3)
- Book availability
- Member status checks
- Fine calculation
- Error handling

### Integration Tests

**Books Endpoints** (10 tests)
- POST /books/ - create book
- GET /books/ - list all books
- GET /books/search - search functionality
- GET /books/{id} - get book details
- PUT /books/{id} - update book
- DELETE /books/{id} - delete book
- Pagination and filtering

**Members Endpoints** (7 tests)
- POST /members/ - create member
- GET /members/ - list members
- GET /members/search - search functionality
- GET /members/{id} - get member details
- PUT /members/{id} - update member
- DELETE /members/{id} - deactivate member

**Loans Endpoints** (8 tests)
- POST /loans/borrow - borrow book
- POST /loans/{id}/return - return book
- GET /loans/ - list loans
- GET /loans/member/{id} - active loans
- GET /loans/member/{id}/history - loan history
- GET /loans/overdue - overdue loans

## Fixtures

All tests use pytest fixtures from `conftest.py`:

- `db`: Fresh in-memory SQLite database for each test
- `client`: FastAPI TestClient
- `sample_book`: Pre-created test book
- `sample_member`: Pre-created test member
- `sample_loan`: Pre-created test loan
- `multiple_books`: Multiple test books for pagination

## Key Testing Patterns

1. **Error Handling**: Tests verify HTTP exceptions are raised with correct status codes
2. **State Validation**: Tests check database state after operations
3. **Business Rules**: Tests enforce borrowing limits, availability, etc.
4. **Edge Cases**: Tests cover duplicate entries, non-existent items, max limits

## Continuous Integration

Add to CI/CD pipeline:
```bash
pytest --cov=app --cov-report=xml --junitxml=test-results.xml tests/
```

## Future Enhancements

- [ ] Performance tests
- [ ] Load testing
- [ ] API contract testing
- [ ] Mutation testing
- [ ] Property-based testing with Hypothesis
