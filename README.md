# Word Similarity Service

This project is a containerized service for querying similar words in the English language based on letter permutations. It provides APIs to fetch similar words, add new words to the dictionary, and retrieve statistics about the service usage.

## Features

- **Find Similar Words**: Identify words that are letter permutations of a given word.
- **Add Words**: Add a word to the service DB.
- **Service Statistics**: View statistics for the `/api/v1/similar` endpoint, including request count and average processing time.

## Algorithm for Finding Similar Words

To determine if two words are similar, the updated approach uses a **letter frequency signature**:

1. **Compute Letter Frequency**: Normalize the word (convert to lowercase, strip whitespace) and compute a frequency signature for its characters.
2. **Query the Database**: Use the frequency signature to fetch words with the same signature from the database, excluding the word itself.
3. **Efficient Async Execution**: Use asynchronous database queries with indexing at the searching columns.

### Time Complexity

- **Word Normalization**: O(n)\, where \(n\) is the length of the word.
- **Frequency Signature Computation**: O(n), for creating a frequency signature.
- **Database Query**: O(log(m)), where \(m\) is the number of entries in the database.

Overall, the algorithm achieves an efficient \(O(n + \log(m))\) complexity for querying similar words, making it suitable for real-time applications.

### Database Migrations

Alembic migration scripts are used for version-controlled schema updates, ensuring consistency and seamless upgrades. To apply migrations, use:

```bash
docker exec -it word_service alembic upgrade head
````

## Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.8+

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd similarWords
   ```

2. Create a `.env` file in the project root with the following environment variables:

   ```env
   POSTGRES_HOST=postgres_service
   POSTGRES_DB=words_db
   POSTGRES_USER=words_user
   POSTGRES_PASSWORD=securepassword
   WORD_MAX_LENGTH=200
   API_VERSION=v1
   [Optional] 
   SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@postgres_service/<POSTGRES_DB>
   ```

3. Build and start the services:

   ```bash
   docker-compose up --build
   ```

4. The frontend service will be accessible at `http://localhost:3000`.

## API Endpoints

### 1. Find Similar Words

- **GET** `/api/v1/similar?word=<word>`
- **Query Parameter**: `word=<word>`
- **Response**: A JSON object containing a list of similar words.
- **Example**:
  ```bash
  curl -X GET "http://localhost:8000/api/v1/similar?word=apple"
  ```
  **Response**:
  ```json
  {
      "similar": ["appel", "pepla"]
  }
  ```

### 2. Add a Word

- **POST** `/api/v1/add-word`
- **Request Body**:
  ```json
  {
      "word": "<word to add>"
  }
  ```
- **Response**: HTTP 200 on success, HTTP 400 on failure.
- **Example**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"word": "littleendian"}' http://localhost:8000/api/v1/add-word
  ```

### 3. Get Statistics

- **GET** `/api/v1/stats`
- **Optional Query Parameters**:
  - `from`: Start of the time frame.
  - `to`: End of the time frame.
- **Response**: A JSON object containing the statistics.
- **Example**:
  ```bash
  curl -X GET "http://localhost:8000/api/v1/stats"
  ```
  **Response**:
  ```json
  {
      "totalWords": 351075,
      "totalRequests": 9,
      "avgProcessingTimeMs": 5616
  }
  ```

### API Documentation

You can read detailed API documentation at `http://localhost:8000/docs`.

## Common cmds

1. Run the application locally:

   ```bash
   docker-compose up --build -d
   ```

2. Run tests:

   ```bash
   docker exec -it word_service pytest
   ```

3. View logs:

   ```bash
   docker-compose logs -f
   ```

