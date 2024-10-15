# Job Portal API with MongoDB and Flask

This project is part of the **DS5760 NoSQL for Modern Data Science Applications** course, where I build a mini job portal API using MongoDB and Flask. The project includes transforming CSV data into JSON format for MongoDB, developing API endpoints for job listings, and setting up the deployment with Docker.

## Project Structure

- **app.py**: Main codebase for handling the API logic, including endpoints for creating, updating, deleting, and querying job posts.
- **csv_to_json.py**: Script for transforming CSV files into JSON format and importing the data into the MongoDB database.
- **docker-compose.yaml**: Docker configuration file for containerized deployment of the application.
- **MiniProject2.pdf**: Instructions detailing the project requirements and tasks.

## Features

The API supports the following operations:

1. **Homepage** (`GET /`): Displays a welcome message for users.
2. **Create Job Post** (`POST /create/jobPost`): Allows users to create a new job post with fields such as title, description, industry, average salary, and location.
3. **View Job Details** (`GET /search_by_job_id/<job_id>`): Retrieves job details by job ID.
4. **Update Job Details** (`PUT /update_by_job_title`): Updates a job post by title.
5. **Remove Job Listing** (`DELETE /delete_by_job_title`): Deletes a job listing by title after confirmation.
6. **Salary Range Query** (`GET /jobs_by_salary_range`): Queries jobs within a specified salary range.
7. **Job Experience Level Query** (`GET /jobs_by_experience_level`): Filters jobs based on experience level.
8. **Top Companies in Industry (Extra Credit)** (`GET /top_companies_by_industry`): Lists top companies in a specific industry based on the number of job posts.

## Data Transformation

The `csv_to_json.py` script handles the following:

- Reads CSV data files.
- Transforms the data into a nested JSON structure.

## Deployment

This project uses Docker for deployment. The `docker-compose.yaml` file handles the setup of the required containers, including MongoDB and the Flask application.

To deploy:

1. Clone the repository.
2. Run `docker-compose up` to start the services.

## Setup

### Prerequisites

- Python 3.x
- Docker
- MongoDB

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app locally:

   ```bash
   python app.py
   ```

### Docker Deployment

1. Ensure Docker is installed and running.
2. Run the following command to start the app and MongoDB in Docker:

   ```bash
   docker-compose up
   ```

   This will start the Flask app at `http://localhost:5001` and MongoDB for data storage.

### Data Import

To transform and import CSV files into MongoDB:

1. Run `csv_to_json.py` to convert the CSV data to JSON format.

   ```bash
   python csv_to_jso.py
   ```
2. use shell to import the data into mongodb.
   ```bash
   mongoimport --db careerhub --collection jobs --file jobs_nested.json --jsonArray

   mongoimport --db careerhub --collection companies --file companies.json --jsonArray

   mongoimport --db careerhub --collection industry --file industry_info.json --jsonArray

   ```
4. Verify the data has been imported successfully into the `careerhub` database by using a MongoDB client.

### API Testing

Use Postman or any HTTP client to test the API endpoints.
