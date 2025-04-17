from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import create_engine
from constants import SQLALCHEMY_DATABASE_URL, DEFAULT_REPORTING_YEAR
import pandas as pd
from oauth2 import get_current_user
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix = "/reporting",
    tags = ["Reporting"]
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def download_file(
        input_df: pd.DataFrame,
        sheet_name: str,
        filename: str
):

    buffer = BytesIO()

    with pd.ExcelWriter(buffer) as writer:
        input_df.to_excel(
            writer,
            index = False,
            sheet_name = sheet_name
        )

    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get('/hired_employee_per_quarter')
def get_hired_employee_per_quarter(
    current_user: Annotated[str, Depends(get_current_user)],
    reporting_year: int = DEFAULT_REPORTING_YEAR
):

    """
        This get request computes the number of employees hired for each job
        and department in specific year divided by quarter. The result are ordered alphabetically
        by department and job.
    Args:
        current_user: parameter to ensure user is correctly authenticated
        reporting_year: year used to get the information
    Returns:
        downloaded file containing information regarding required report
    """

    print(current_user)

    query = f'''
        SELECT
            b.department_name,
            c.job_name,
            a.employee_id,
            CONCAT('Q',QUARTER(STR_TO_DATE(hiring_datetime,'%%Y-%%m-%%dT%%TZ'))) as hiring_quarter,
            YEAR(STR_TO_DATE(hiring_datetime,'%%Y-%%m-%%dT%%TZ')) as hiring_year
        FROM hired_employee a
        LEFT JOIN department b
        ON a.department_id = b.department_id
        LEFT JOIN job c
        ON a.job_id = c.job_id
    '''

    df = pd.read_sql(
        query,
        con = engine
    )

    df = df.loc[
        df['hiring_year'] == reporting_year
    ]

    df.fillna(
        'N/A',
        inplace = True
    )

    final_df = pd.pivot_table(
        df,
        values = 'employee_id',
        index = [
            'department_name',
            'job_name'
        ],
        columns = ['hiring_quarter'],
        aggfunc = 'count'
    )

    final_df.reset_index(
        inplace=True
    )

    final_df.fillna(
        0,
        inplace = True
    )

    return download_file(
        final_df,
        f'reporting_{reporting_year}',
        f'hired_employee_per_quarter_{reporting_year}.xlsx'
    )

@router.get('/department_hired_employee_more_than_mean')
def get_department_hired_employee_more_than_mean(
    current_user: Annotated[str, Depends(get_current_user)],
    reporting_year: int = DEFAULT_REPORTING_YEAR
):

    """
        This get request computes the list of ids, name and number of employees
        hired of each department that hired more employees than the mean of employees
        hired in 2021 for all the departments, ordered by the number of
        employees hired (descending).
    Args:
        current_user: parameter to ensure user is correctly authenticated
    Returns:
        downloaded file containing information regarding required report
    """

    print(current_user)

    query = '''
        
    '''

    pass