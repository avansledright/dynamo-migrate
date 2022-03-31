# Dynamo Migration Tool
This is a simple Python script that will migrate existing data from one DynamoDB table to another DynamoDB table.

## Usage:
1. Clone the repository
2. Setup your AWS Configuration file with two profiles. One called 'source' and one called 'destination'.
3. Run the script: (Replacing source_table and dest_table)
`python3 dynamo-migrate.py source_table dest_table`
4. Verify your data has been migrated.