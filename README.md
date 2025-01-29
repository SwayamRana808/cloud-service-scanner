# Python Cloud Security Dashboard

This is a Python-based web application that provides a Cloud Security Dashboard with an overview of security risks for cloud services (such as EC2, S3, IAM, and RDS). The dashboard visualizes risk levels for different services and allows users to assess high, medium, and low-risk issues. It also offers real-time updates via WebSocket and serves as both a backend API and a frontend dashboard.

## Features
- **Risk Monitoring**: Displays risk levels for cloud services (EC2, S3, IAM, RDS) based on user-defined data.
- **FastAPI**: Backend framework for serving the web application and APIs.
- **WebSocket Integration**: Real-time data updates via WebSocket, allowing dynamic risk status updates.
- **Frontend Dashboard**: A web interface built with HTML and CSS that displays the security dashboard.
- **Backend API**: Exposes various endpoints for interacting with cloud security data, including retrieving risk levels and services data.
- **Jinja2**: Templating engine for rendering HTML views.
- **Redis**: For caching and data storage.
- **AWS SDK (boto3)**: For interacting with AWS services.
- **APScheduler**: Used to schedule periodic security checks at user-defined intervals
## Setup and Installation

### 1. Clone the repository:
```bash
git clone https://github.com/SwayamRana808/cloud-service-scanner.git
cd cloud-service-scanner
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## AWS credentials
- MY_AWS_ACCESS_KEY=your-access-key
- MY_AWS_SECRET_KEY=your-secret-key
- AWS_REGION=your-region  # Example: us-east-1

## Redis connection details
- REDIS_HOST=your-redis-host
- REDIS_PORT=your-redis-port
- REDIS_DB=0
- REDIS_USERNAME=default
- REDIS_PASSWORD=your-redis-password
Replace the placeholder values with your actual AWS and Redis credentials.

Run the application:

``bash
uvicorn app.main:app --reload
``
This will start the server on http://127.0.0.1:8000.

How to Use
Home Page: Upon accessing the home page (/), you will see a "Go to Dashboard" button. Click it to navigate to the dashboard where you can view the risk levels of various cloud services.

Dashboard: The dashboard provides an overview of services like EC2, S3, IAM, and RDS. Each service shows the distribution of risks (high, medium, and low).

Service Details: For each service, click on the region to expand and view specific instances. Each instance has its risk tags and status.

Troubleshooting
Issue with Redis connection: If you're having issues connecting to Redis, check the credentials and host/port configurations in the .env file. Make sure your Redis instance is accessible from your local machine or server.

Missing or incorrect data: Ensure that the correct data format is used for each cloud service. You may need to adjust the service_data structure for each service accordingly.


Acknowledgements
Thanks to the authors of FastAPI, Redis, and AWS SDK (boto3) for their amazing libraries that helped build this project.
Feel free to customize the README further based on your specific needs.

-Swayam Rana(Creator)
