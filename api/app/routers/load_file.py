from fastapi import APIRouter, Depends, File, Form, UploadFile
from oauth2 import get_current_user
from constants import SQLALCHEMY_DATABASE_URL, DATE_FORMAT, CHUNKSIZE, TABLE_COLUMNS
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from io import BytesIO
from typing import Annotated

router = APIRouter(
    prefix = "/loadfile",
    tags = ['Load files']
)

@router.post('/')
def load_file(
    current_user: Annotated[str, Depends(get_current_user)],
    table_name: str = Form(...),
    table_content: UploadFile = File(...)
):

    """This post request receives a csv file to be processed and insert into a mysql table
    Args:
        current_user: parameter to ensure user is correctly authenticated
        table_name: table name where file data will be inserted
        table_content: file data to be processed before inserting into a table
    Returns:
        message: informaton about data ingestion process
    """

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    current_dt = datetime.strftime(datetime.now(), DATE_FORMAT)

    print(f'UserID-{current_user} / {current_dt}: Inserting rows in table {table_name}', flush=True)

    try:

        start_datetime = datetime.now()

        dfIter = pd.read_csv(
            BytesIO(table_content.file.read()),
            header = None,
            chunksize = CHUNKSIZE
            )

        row_count = 0

        for df in dfIter:

            df.columns = TABLE_COLUMNS.get(table_name)

            df.to_sql(
                table_name,
                engine,
                index = False,
                if_exists = 'append'
            )

            row_count+=df.shape[0]
        
        end_datetime = datetime.now()
        elapsed_time = (end_datetime - start_datetime).total_seconds()

        print(f'''{datetime.strftime(end_datetime, DATE_FORMAT)}: \
    {row_count} rows were inserted in table {table_name} in {elapsed_time} seconds.''',
            flush=True)

        return {'message': f'table {table_name} updated'}
    
    except Exception as e:

        return {f'message: {e}'}