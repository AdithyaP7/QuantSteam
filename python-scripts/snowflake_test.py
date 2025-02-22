'''
for verifying connections
'''

import snowflake.connector

conn = snowflake.connector.connect(
    user='<YOUR_USERNAME>',
    password='<YOUR_PASSWORD>',
    account='<YOUR_ACCOUNT>.snowflakecomputing.com'
)
cursor = conn.cursor()
cursor.execute("SELECT CURRENT_VERSION()")
result = cursor.fetchone()
print("Snowflake Version:", result[0])
