from generate_acip_schema import GoogleSheets
from tests.config import gs, mysql
from tests.acip_catalogs_utils import set_up_data_frame, create_column_mapper, create_page_numbers
from pandas import concat, DataFrame
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# params ------------------------------------------------------
threshold = 0.99
test = True

# 1. Connectors ##################################
# connect to MySQL --------------------------------------------
engine = create_engine(mysql.db_url, echo=False)
try:
    cnx = engine.connect()
    print(f"Successful connection to MySQL at {mysql.conf_mysql['host']}")
except SQLAlchemyError as e:
    sys.exit(f"Error on connecting to MySQL, {str(e.__dict__['orig'])}")


# connect to GS -----------------------------------------------
gs_instance = GoogleSheets(config=gs.conf_gs)
title_catalog_worksheets = []
[wb, wks] = gs_instance.get_worksheets()

if test:
    title_catalog_worksheets.append('ACIP_Title_Test')  # ACIP_TEST_Title_Catalog
else:
    [title_catalog_worksheets.append(key) for key, value in wks.items() if 'ACIP_Title_Catalog' in key]

print(f"Title Catalogs: {title_catalog_worksheets}")

# 2. TRANSFORM --------------------------------------------------
# create single data table of all title catalog worksheets
data_list = []
for name in title_catalog_worksheets:
    # get data, transform to data frame
    ws = gs_instance.get_worksheet_data(ws=name)
    data = set_up_data_frame(ws)
    # map out new column names
    m = create_column_mapper(gs.target_columns, list(data.columns), threshold=threshold)
    new_cols = list(m.values())
    data = data.rename(columns=m)
    data = data[new_cols]  # only keep column names that match target
    print(f"{name}: {data.shape[0]}, {data.shape[1]}")
    data_list.append(data)
    del data

final_data = concat(data_list)
del data_list

print(f"Final table has shape: {final_data.shape[0]}, {final_data.shape[1]} "
      f"and is type {isinstance(final_data, DataFrame)}")


# add pages --------------------------------------------------------
altered_data = create_page_numbers(final_data)

print(f"Writing table to MySQL: {altered_data.name} ({len(altered_data)} records)")


# 4. load into MySQL -----------------------------------------------
# write the data frame to MySQL, using replace if table exists
altered_data.to_sql(altered_data.name, con=cnx, if_exists='replace', index=False)
# #########################################################

# CLOSE CONNECTION -------------------------------------------------
cnx.detach()
cnx.close()
# #########################################################

# gs_instance.write_listing(data=altered_data, ws='This_One', header=altered_data.columns)

# print(altered_data)
