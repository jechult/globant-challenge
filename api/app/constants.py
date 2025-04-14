DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
API_USER = 'jechult'
API_PASSWORD = 'admin'
SQLALCHEMY_DATABASE_URL = "mysql://jechu:password@companydb:3306/companydb"
CHUNKSIZE = 10000
TABLE_COLUMNS = {
    "department": [
        "department_id",
        "department_name"
    ],
    "job": [
        "job_id",
        "job_name"
    ],
    "hired_employee": [
        "employee_id",
        "employee_name",
        "hiring_datetime",
        "department_id",
        "job_id"
    ]
}