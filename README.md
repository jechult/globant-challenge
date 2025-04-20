# Globant Challenge Data Engineering

A RESTful API to migrate data from files to database and get reports from it.

## 📁 Project structure


```

.
├── .gitignore                  # Prevent staging of unnecessary files to git
├── docker-compose.yml          # Config file to deploy both fastapi and mysql container
├── db_root_pass.txt            # Text file where root pass is stored
├── db_user_pass.txt            # Text file where user pass is stored
├── README.md                   # Project README
├── api                         # API folder
│   ├── app                     # API source 
│   │   ├── routers             # Routers section por API
│   │   │   ├── auth.py         # Authentication section for login purposes
│   │   │   ├── load_file.py    # Uploading files section for load data from CSV to MySQL DB
│   │   │   ├── reporting.py    # Reporting section to get insights from MySQL DB
│   │   ├── test_files          # Path with files for testing purposes
│   │   ├── constants.py        # Script where constants variables are defined
│   │   ├── main.py             # Main script where app is declared and attached to the routers
│   │   ├── oauth2.py           # Script where getting authentication token with its corresponding checking
│   │   ├── test_main.py        # Script where test unit cases are defined
│   ├── Dockerfile              # Config file to build a python container with api code
│   └── requirements.txt        # Packages list for api environment
└── ddl_script                  # Database scripts folder
    └── init_sql.sql            # Initialization script after db container creation

```

# Table of contents

## 0. MySQL Database Relational Model

<img src="https://github.com/jechult/globant-challenge/blob/c50e260123bf35354c203256e3d9fdf579be0286/db_relational_model.png" alt="Alt text" title="MySQL Database Relational Model">

## 1. 👩‍💻 Pre requisites

- If not installed, download Docker Desktop (https://www.docker.com/products/docker-desktop/)
- If not installed, download git (https://git-scm.com/downloads)
- Make sure docker client is up

## 2. 🖥 Build and run application

- To download the remote repository in local, run in terminal:

    ```shell
    git clone https://github.com/jechult/globant-challenge.git
    cd challenge-code
    ```
- Once you have downloaded the repository, run the following command to build and deploy the containers (api and mysql):

    ```shell
    docker-compose up --build
    ```

## 3. 🧪 Test running application

### 3.1 API Authentication

- For testing purpose, use the following credentials:

    ```shell
    USERNAME = jechult
    PASSWORD = admin
    ```

- As a first step, please authenticate on API using the credentials above by running the following command:

    ```shell
    curl -L -X POST 'http://localhost/login' \
    -F 'username=[USERNAME]' \
    -F 'password=[PASSWORD]'
    ```

    Parameters:
    - USERNAME: user displayed in 3.1
    - PASSWORD: password displayed in 3.1

- If everything's OK, as a result, you'll get an access token like this:

    ```shell
    {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiamVjaHVsdCIsImV4cCI6MTc0NTExMTExM30.pQZH517JIYfwkc-cXr-hgPMuSyEHdgQ92m_pRFT_tg8","token_type":"bearer"}
    ```

- Otherwise, you'll get the following message:

    ```shell
    {"detail":"Invalid credentials"}
    ```
### 3.2 Load files from CSV to MySQL Database

- ✔ Once you are correctly authenticated, you'll be able to test the api. Please, save the obtained access token,
you're going to need it for the following tests. ⚠ Warning: The obtained access token will expire in 60 minutes, so please be careful when making requests to the different endpoints.

- Now, it's time to upload data from CSV files to MySQL DB

- ⚠⚠⚠ Due to hired_employee table has two foreigns keys, it's mandatory to load job and department tables first.

- As you can see, previous data model has 3 tables which are department, job and hired_employee. Before testing reporting requests, you must upload data into tables. To do that, you should run the following command per table:

    ```shell
    curl -L -X POST 'http://localhost/loadfile' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer [ACCESS_TOKEN]' \
    -H 'Content-Type: multipart/form-data' \
    -F 'table_name="[TABLE_NAME]"' \
    -F 'table_content=@"[FILE_PATH]"'
    ```    

    Parameters:
    - ACCESS_TOKEN: obtained code in authentication process
    - TABLE_NAME: table name which 3 possible values (department, job, hired_employee)
    - FILE_PATH: path where file is stored.

    Here you have an example:

    ```shell
    curl -L -X POST 'http://localhost/loadfile' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiamVjaHVsdCIsImV4cCI6MTc0NTExMTExM30.pQZH517JIYfwkc-cXr-hgPMuSyEHdgQ92m_pRFT_tg8' \
    -H 'Content-Type: multipart/form-data' \
    -F 'table_name="department"' \
    -F 'table_content=@"/home/files/departments.csv"'
    ```

- Once the process ends, you'll see a message like this:

    ```shell
    {"message":"table department updated"}
    ```

### 3.3 Reporting

- Once we have our data into MySQL Database, it's time to get some reports:

    a) Number of hired employee per quarter

    ```shell
    curl -L -X GET 'http://localhost/reporting/hired_employee_per_quarter?reporting_year=[REPORTING_YEAR]' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer [ACCESS_TOKEN]'
    --output "[OUTPUT_FILE_PATH]"
    ```

    b) Departments with hired employees more than mean

    ```shell
    curl -L -X GET 'http://localhost/reporting/department_hired_employee_more_than_mean?reporting_year=[REPORTING_YEAR]' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer [ACCESS_TOKEN]'
    --output "[OUTPUT_FILE_PATH]"
    ```

    Parameters:
    - REPORTING_YEAR: year used to get the information
    - ACCESS_TOKEN: obtained code in authentication process
    - OUTPUT_FILE_PATH: file path where reporting data will be saved

-  If everything's OK, a file will be downloaded in your directory

### 3.4 Testing

- For test unit cases, we'll use Pytest with the following steps:

    a) Run this command to get api container ID

    ```shell
    docker ps --format '{"ID":"{{ .ID }}", "Image": "{{ .Image }}", "Names":"{{ .Names }}"}'
    ```

    ```json
    {"ID":"258001893e9a", "Image": "globant-challenge-app", "Names":"globant-challenge-app-1"}
    {"ID":"2a1ddb9bf5ac", "Image": "mysql:8", "Names":"globant-challenge-companydb-1"}
    ```

    b) Copy ID related to app ("globant-challenge-app-1" in this case), and run this command:

    ```shell
    docker exec -it [CONTAINER_ID] bash
    ```

    c) Once we are inside app environment, just run the following command:

    ```shell
    pytest
    ```
    If all went well, you will see something like this:

    ```
    =================================================================== test session starts ====================================================================
    platform linux -- Python 3.12.10, pytest-8.3.5, pluggy-1.5.0
    rootdir: /app
    plugins: anyio-4.9.0
    collected 7 items

    test_main.py .......                                                                                                                                 [100%]

    ===================================================================== warnings summary =====================================================================
    test_main.py::test_reporting_2
    /app/routers/reporting.py:52: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value 'N/A' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
        df.fillna(

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =============================================================== 7 passed, 1 warning in 8.05s ===============================================================
    ```
