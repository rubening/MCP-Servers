# Project Knowledge Sample

## Project Overview
This is a sample project knowledge file for testing the MCP optimizer. The goal is to demonstrate how the analyzer works and what kind of feedback it provides.

## Technical Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI for web services
- **Database**: PostgreSQL with SQLAlchemy
- **Testing**: pytest for unit testing
- **Deployment**: Docker containers on AWS

## Current Status
The project is in early development phase. We have basic CRUD operations working but need to implement authentication and advanced features.

## Setup Instructions

### Local Development
1. Clone the repository
2. Install dependencies with `pip install -r requirements.txt`
3. Run the development server with `uvicorn main:app --reload`
4. Access the API at http://localhost:8000

### Database Setup
Create a PostgreSQL database and set the connection string in your environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Architecture Decisions

### Why FastAPI over Flask
We chose FastAPI because it provides automatic API documentation, built-in validation, and excellent performance. The async support is crucial for our use case.

### Database Design
We're using PostgreSQL because we need complex queries and transactions. The SQLAlchemy ORM provides good abstraction while still allowing raw SQL when needed.

## API Endpoints

### User Management
- `POST /users` - Create new user
- `GET /users/{id}` - Get user by ID  
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

## Testing Strategy
We use pytest for all testing with these key principles:
- Unit tests for business logic
- Integration tests for API endpoints
- Mock external dependencies
- Aim for 80%+ code coverage

## Deployment Process
1. Build Docker image
2. Push to AWS ECR
3. Deploy to ECS cluster
4. Run database migrations
5. Update load balancer configuration

## Security Considerations
- All API endpoints require authentication except `/health`
- Input validation using Pydantic models
- SQL injection prevention through ORM
- Rate limiting on all endpoints
- HTTPS only in production

## Performance Notes
Current benchmarks show:
- Average response time: 45ms
- 95th percentile: 120ms
- Throughput: 1000 requests/second
- Database connection pool: 20 connections

## Known Issues
1. Memory usage grows over time - needs investigation
2. Slow queries on user search - needs indexing
3. File upload occasionally fails - timeout issue

## Future Roadmap
- Q1: Implement caching layer with Redis
- Q2: Add real-time notifications with WebSockets  
- Q3: Multi-tenant architecture
- Q4: Advanced analytics dashboard
