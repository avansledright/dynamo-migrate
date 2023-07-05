import sys
import boto3
from botocore.exceptions import ClientError

## USAGE ############################################################################
## python3 dynamo.py <Source_Table> <destination table>                            ## 
## Requires two profiles to be set in your AWS Config file "source", "destination" ##
#####################################################################################
def dynamo_bulk_reader():
    session = boto3.session.Session(profile_name='source')
    dynamodb = session.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table(sys.argv[1])

    print("Exporting items from: " + str(sys.argv[1]))

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    print("Finished exporting: " + str(len(data)) + " items.")
    return data

def dynamo_bulk_writer():
    session = boto3.session.Session(profile_name='destination')
    dynamodb = session.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table(sys.argv[2])
    print("Importing items into: " + str(sys.argv[2]))
    table_items = dynamo_bulk_reader()
    total_records = len(table_items)
    for table_item in table_items:
        count = 1
        with table.batch_writer() as batch:
            try:
                print("Importing:", str(count), "/", str(total_records))
                print(table_item)
                response = batch.put_item(
                Item=table_item
                )
                count = count + 1
            except ClientError as e:
                print("Failed to import item")
                print(e)

    print("Finished importing items...")
if __name__ == '__main__':
    print("Starting Dynamo Migrater...")
    dynamo_bulk_writer()
    print("Exiting Dynamo Migrator")