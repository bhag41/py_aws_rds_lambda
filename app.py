import json 
import boto3
import pymysql

#Constants 
SECRET_NAME = ""
REGION_NAME = "us-east-1"
DB_NAME = "ExampleDB"
TABLE_NAME = "Person"
HOSTNAME = "exampledb.cqjxqjxjx.us-east-1.rds.amazonaws.com" #fix this 
USERNAME = "admin"

#global variables to store the database connection and cursor
connection = None
cursor = None

def get_secret():
    client = boto3.client('secretsmanager', region_name=REGION_NAME)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    secret_data = json.loads(response['SecretString'])
    return secret_data

def get_database_connection():
    global connection,cursor

    if connection is None:
        secret_data = get_secret()
        db_host = HOSTNAME
        db_user = USERNAME
        db_password = secret_data['password']

        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=DB_NAME)
        cursor = connection.cursor()

def lambda_handler(event, context):
    try:
        get_database_connection()
        query = f"SELECT * FROM {TABLE_NAME}"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)

        return{
            "statusCode": 200,
            "body": "Data fetched successfully"
        }
    except pymysql.Error as e:
        return{
            "statusCode": 500,
            "body": f"Error fetching data {str(e)}"
        }
