## Tech Stack 
- AWS Lambda
- Amazon DynamoDB
- Amazon EventBridge
- AWS Systems Manager (Parameter Store)
- CloudWatch (logging)
- Python

## Architecture Overview
Alpha Vantage API
↓
EventBridge 
↓
Ingestion Lambda
↓
DynamoDB
↓
Read API Lambda 
↓
Dashboard


## To run locally: 
pip install -r requirements.txt
streamlit run dashboard/app.py