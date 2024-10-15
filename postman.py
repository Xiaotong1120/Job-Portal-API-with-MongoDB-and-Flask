'''Module for serving API requests'''

from flask import Flask, request, jsonify
import json
import ast  # helper library for parsing data from string
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Initialize the Flask app
app = Flask(__name__)

# 1. Connect to the MongoDB client
client = MongoClient(host="localhost", port=27017)

# 2. Select the database
db = client.careerhub
# Select the collection
jobs = db.jobs
companies = db.companies
industry = db.industry

# Create a Job Post
# http://localhost:5001/
@app.route("/")  # '/' for directing all default traffic to this function get_initial_response()
def get_initial_response():
    # Message to the user
    message = {
        'name': 'Xiaotong Ma',
        'Greetings': 'Welcome!'
    }
    resp = jsonify(message)
    # Returning the object
    return resp

# View Job Details with Industry and Company Information
# http://localhost:5001/search_by_job_id/<job_id>
@app.route('/search_by_job_id/<job_id>', methods=['GET'])
def get_by_id(job_id):
    try:
        # Convert string to ObjectId
        obj_id = ObjectId(job_id)

        # Query the job document
        job_result = jobs.find_one({"_id": obj_id})

        # If job document not found
        if not job_result:
            return jsonify({"message": "Job document not found"}), 404

        # Convert ObjectId to string for JSON serialization
        job_result['_id'] = str(job_result['_id'])

        # Fetch industry information if industry_id is present
        if "industry_id" in job_result:
            industry_id = job_result["industry_id"]
            industry_result = industry.find_one({"id": industry_id})
            if industry_result:
                industry_result['_id'] = str(industry_result['_id'])
                job_result['industry'] = industry_result

        # Fetch company information if company_id is present
        if "company_id" in job_result:
            company_id = job_result["company_id"]
            company_result = companies.find_one({"id": company_id})
            if company_result:
                company_result['_id'] = str(company_result['_id'])
                job_result['company'] = company_result

        return jsonify(job_result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Create a Job Post
# http://localhost:5001/create/jobPost
@app.route('/create/jobPost', methods=['POST'])
def create_job_post():
    try:
        # Get the request data
        data = request.get_json()

        # Separate data into jobs, industry, and company
        job_data = {}
        industry_data = {}
        company_data = {}

        # Populate job data
        job_fields = ['id', 'title', 'description', 'industry_id', 'years_of_experience', 'detailed_description',
                      'responsibilities', 'requirements', 'education_and_skills', 'industry_skills']
        for field in job_fields:
            if field in data:
                job_data[field] = data[field]

        # Extract fields from employment_details if present
        if 'employment_details' in data:
            employment_details = data['employment_details']
            if 'average_salary' in employment_details:
                job_data['average_salary'] = employment_details['average_salary']
            if 'employment_type' in employment_details:
                job_data['employment_type'] = employment_details['employment_type']
            if 'benefits' in employment_details:
                job_data['benefits'] = employment_details['benefits']
            if 'job_posting_url' in employment_details:
                job_data['job_posting_url'] = employment_details['job_posting_url']
            if 'posting_date' in employment_details:
                job_data['posting_date'] = employment_details['posting_date']
            if 'closing_date' in employment_details:
                job_data['closing_date'] = employment_details['closing_date']
            if 'remote' in employment_details:
                job_data['remote'] = employment_details['remote']

        # Populate industry data if available
        if 'industry' in data:
            industry_data = data['industry']
            if 'id' in industry_data:
                job_data['industry_id'] = industry_data['id']

        # Populate company data if available
        if 'company' in data:
            company_data = data['company']
            if 'id' in company_data:
                job_data['company_id'] = company_data['id']

        # Validate required fields for job data
        required_fields = ['title', 'industry_id', 'description', 'average_salary', 'id']
        for field in required_fields:
            if field not in job_data or not job_data[field]:
                return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

        # Insert or update industry data if provided
        if industry_data:
            industry_result = industry.find_one({"id": industry_data['id']})
            if industry_result:
                industry.update_one({"id": industry_data['id']}, {"$set": industry_data})
            else:
                industry.insert_one(industry_data)

        # Insert or update company data if provided
        if company_data:
            company_result = companies.find_one({"id": company_data['id']})
            if company_result:
                companies.update_one({"id": company_data['id']}, {"$set": company_data})
            else:
                companies.insert_one(company_data)

        # Insert the job data into the jobs collection
        result = jobs.insert_one(job_data)

        # Return the newly created job post with its ID
        job_data['_id'] = str(result.inserted_id)
        return jsonify(job_data), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update Job Details by Job Title
# http://localhost:5001/update_by_job_title
@app.route('/update_by_job_title', methods=['PUT'])
def update_job_by_title():
    try:
        # Get the request data
        data = request.get_json()

        # Validate that the job title is provided
        if 'title' not in data or not data['title']:
            return jsonify({"error": "'title' is required to update a job"}), 400

        # Search for the job by title
        job_result = jobs.find_one({"title": data['title']})

        # If job not found
        if not job_result:
            return jsonify({"message": "Job not found"}), 404

        # Prepare the fields to be updated in the jobs collection
        job_update_fields = ['description', 'average_salary', 'years_of_experience', 'detailed_description',
                             'responsibilities', 'requirements', 'education_and_skills', 'industry_skills',
                             'employment_type', 'benefits', 'job_posting_url', 'posting_date', 'closing_date', 'remote']
        update_job_fields = {field: data[field] for field in job_update_fields if field in data and data[field]}

        # Update the job document if there are fields to update
        if update_job_fields:
            jobs.update_one({"title": data['title']}, {"$set": update_job_fields})

        # Update industry data if present
        if 'industry' in data:
            industry_data = data['industry']
            if 'id' in industry_data:
                industry.update_one({"id": industry_data['id']}, {"$set": industry_data}, upsert=True)

        # Update company data if present
        if 'company' in data:
            company_data = data['company']
            if 'id' in company_data:
                companies.update_one({"id": company_data['id']}, {"$set": company_data}, upsert=True)

        # Return success message
        return jsonify({"message": "Job updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Remove Job Listing by Job Title
# http://localhost:5001/delete_by_job_title
@app.route('/delete_by_job_title', methods=['DELETE'])
def delete_job_by_title():
    try:
        # Get the request data
        data = request.get_json()

        # Validate that the job title is provided
        if 'title' not in data or not data['title']:
            return jsonify({"error": "'title' is required to delete a job"}), 400

        # Search for the job by title
        job_result = jobs.find_one({"title": data['title']})

        # If job not found
        if not job_result:
            return jsonify({"message": "Job not found"}), 404

        # Display job details and ask for confirmation
        job_result['_id'] = str(job_result['_id'])
        confirmation = data.get('confirm', False)

        if not confirmation:
            return jsonify({"message": "Job found. Please confirm deletion.", "job_details": job_result}), 200

        # Delete the job from the collection upon confirmation
        jobs.delete_one({"title": data['title']})

        # Return success message
        return jsonify({"message": "Job deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Salary Range Query
# http://localhost:5001/query_by_salary_range?min_salary=<min_salary>&max_salary=<max_salary>
@app.route('/query_by_salary_range', methods=['GET'])
def query_by_salary_range():
    try:
        # Get query parameters
        min_salary = request.args.get('min_salary', type=int)
        max_salary = request.args.get('max_salary', type=int)

        # Validate salary range
        if min_salary is None or max_salary is None:
            return jsonify({"error": "Both min_salary and max_salary are required."}), 400

        # Ensure average_salary in employment_details is stored as an integer
        for doc in jobs.find({}):
            if "employment_details" in doc and "average_salary" in doc["employment_details"]:
                avg_salary = doc["employment_details"]["average_salary"]
                if isinstance(avg_salary, (str, float, dict)):
                    try:
                        average_salary = int(avg_salary)
                        jobs.update_one({"_id": doc["_id"]}, {"$set": {"employment_details.average_salary": average_salary}})
                    except ValueError:
                        continue

        # Query jobs within the salary range
        query = {"employment_details.average_salary": {"$gte": min_salary, "$lte": max_salary}}
        job_results = list(jobs.find(query))

        # Convert ObjectIds to strings for JSON serialization
        for job in job_results:
            job['_id'] = str(job['_id'])

        # Return the job results
        return jsonify(job_results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Job Experience Level Query
# http://localhost:5001/query_by_experience_level?experience_level=<experience_level>
@app.route('/query_by_experience_level', methods=['GET'])
def query_by_experience_level():
    try:
        # Get query parameter
        experience_level = request.args.get('experience_level', type=str).lower()

        # Validate experience level
        if not experience_level:
            return jsonify({"error": "Experience level is required."}), 400

        # Define experience level ranges
        experience_mapping = {
            "entry level": {"$lte": 2},
            "mid level": {"$gte": 3, "$lte": 5},
            "senior level": {"$gte": 6}
        }

        # Check if the provided experience level is valid
        if experience_level not in experience_mapping:
            return jsonify({"error": "Invalid experience level. Valid options are 'Entry Level', 'Mid Level', 'Senior Level'."}), 400

        # Query jobs based on experience level
        query = {"years_of_experience": experience_mapping[experience_level]}
        job_results = list(jobs.find(query))

        # Convert ObjectIds to strings for JSON serialization
        for job in job_results:
            job['_id'] = str(job['_id'])

        # Return the job results
        return jsonify(job_results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)