# Resume AI

Resume AI is a project that demonstrates proficiency in various technologies and software design principles. This application uses _very_ rudimentary AI to analyze and score resumes.

## Technologies Used

- **Backend:**
  - Django
  - Celery (with Redis as message broker)
  - Flower (for Celery monitoring)
  - SQLite (for development, easily swappable with PostgreSQL)
- **AI Services:**
  - OpenAI
  - Llama

## Getting Started

To run the project after cloning, use Docker Compose:

```bash
docker-compose build
docker-compose up
```

**Required ENV Variables:**

- REPLICATE_API_TOKEN
- OPENAI_API_KEY
- DEBUG: True or False
- SECRET_KEY
- ALLOWED_HOSTS
- REDIS_URL

## Architecture

- **Django:** The main framework used for the application.
- **Celery:** Used for handling asynchronous tasks. Included webhook code in celery_webhook.txt for external observation.
- **Redis:** Acts as the message broker for Celery.
- **Flower:** Provides a web-based monitoring interface for Celery tasks.
- **SQLite:** Used as the database for quick development. Can be easily replaced with PostgreSQL for production use.

## Design Patterns and Principles

The project demonstrates proficiency in Object-Oriented Programming (OOP) design patterns and SOLID principles:

- **Factory Pattern:** Implemented in the user_scoring views to switch between different AI services (OpenAI or Llama) for resume scoring.
- **Abstraction:** Used throughout the project to separate concerns and improve code maintainability.
- **SOLID Principles:** Applied to ensure a robust and scalable codebase.

## Code Quality

- Comprehensive comments have been added to classes and methods containing significant logic.
- Unit testing of views and tasks.

## Future Improvements

- Implement user authentication and authorization.
- AI training for resume scoring.
- Develop a React.js front end.
- Implement unit testing for user_scoring services and serializers
- Implement unit testing for job_postings services and serializers
- Implement integration testing
