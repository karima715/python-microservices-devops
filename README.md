# Python Microservices DevOps Project

This project demonstrates a complete DevOps pipeline with Python microservices.

## Services
- Backend API (Flask)
- Frontend (Flask with templates)
- Logger service
- PostgreSQL database

## Setup
1. Clone the repository
2. Run `docker-compose up` to start all services locally
3. Access the frontend at http://localhost:8080

## CI/CD
GitHub Actions is configured to build and push Docker images to DockerHub on every push to main.

## AWS Deployment
Terraform is configured to deploy the application to AWS EC2.

## Author
Karima Satkut (karimaji143@gmail.com)