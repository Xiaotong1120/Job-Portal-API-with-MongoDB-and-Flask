import pandas as pd
import json

# Load CSV files
tables = {
    "companies": pd.read_csv('./mp2-data/companies.csv'),
    "education_and_skills": pd.read_csv('./mp2-data/education_and_skills.csv'),
    "employment_details": pd.read_csv('./mp2-data/employment_details.csv'),
    "industry_info": pd.read_csv('./mp2-data/industry_info.csv'),
    "jobs": pd.read_csv('./mp2-data/jobs.csv')
}

# Merge Industry Info with Companies to add growth_rate
companies_df = tables['companies'].merge(tables['industry_info'][['id', 'growth_rate']], left_on='id', right_on='id', how='left')

# Convert Companies Schema to JSON
companies_json = companies_df.to_dict(orient='records')
with open('companies.json', 'w') as f:
    json.dump(companies_json, f, indent=4)

# Combine Jobs, Employment Details, Education and Skills into One Nested JSON
jobs_df = tables['jobs']
education_df = tables['education_and_skills']
employment_df = tables['employment_details']
industry_info_df = tables['industry_info']

# Merge tables
jobs_with_education = jobs_df.merge(education_df, left_on='id', right_on='job_id', suffixes=('', '_education'))
jobs_with_details = jobs_with_education.merge(employment_df, left_on='id', right_on='id', suffixes=('', '_employment'))
jobs_with_industry = jobs_with_details.merge(industry_info_df[['id', 'industry_skills']], left_on='id', right_on='id', how='left')

# Drop growth_rate and industry_skills from industry_info
industry_info_df = industry_info_df.drop(columns=['growth_rate', 'industry_skills'])

# Convert the cleaned industry_info DataFrame to JSON
industry_info_json = industry_info_df.to_dict(orient='records')

# Write industry_info JSON to a file
with open('industry_info.json', 'w') as f:
    json.dump(industry_info_json, f, indent=4)

# Nest education_and_skills, employment_details, and industry_skills inside jobs
nested_json = []
for _, row in jobs_with_industry.iterrows():
    job = {
        "id": row['id'],
        "title": row['title'],
        "description": row['description'],
        "years_of_experience": row['years_of_experience'],
        "detailed_description": row['detailed_description'],
        "responsibilities": row['responsibilities'],
        "requirements": row['requirements'],
        "education_and_skills": {
            "required_education": row['required_education'],
            "preferred_skills": row['preferred_skills']
        },
        "employment_details": {
            "employment_type": row['employment_type'],
            "average_salary": row['average_salary'],
            "benefits": row['benefits'],
            "remote": row['remote'],
            "job_posting_url": row['job_posting_url'],
            "posting_date": row['posting_date'],
            "closing_date": row['closing_date']
        },
        "industry_skills": row['industry_skills'],
        "industry_id": row['id'],
        "company_id": row['id']
    }
    nested_json.append(job)

# Convert to JSON
with open('jobs_nested.json', 'w') as f:
    json.dump(nested_json, f, indent=4)

print("Conversion completed successfully!")