import boto3

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table_name = "ReplayData"

table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {'AttributeName': 'battle_id', 'KeyType': 'HASH'},
    ],
    AttributeDefinitions=[
        {'AttributeName': 'battle_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST',
)

print("Creating table, please wait...")
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(f"Table '{table_name}' is active!")

replay_data = {
    "battle_id": "12345",
    "battle_at": 1698012345,
    "battle_type": 1,
    "game_version": 101,
    "p1_data": {
        "area_id": 10,
        "chara_id": 101,
        "lang": "EN",
        "name": "Player1",
        "polaris_id": "POL12345",
        "power": 5000,
        "rank": 10,
        "region_id": 5,
        "rounds": 3,
        "user_id": 1001,
    },
    "p2_data": {
        "area_id": 20,
        "chara_id": 202,
        "lang": "FR",
        "name": "Player2",
        "polaris_id": "POL54321",
        "power": 4900,
        "rank": 12,
        "region_id": 6,
        "rounds": 3,
        "user_id": 1002,
    },
    "stage_id": 1,
    "winner": 1,
}

table.put_item(Item=replay_data)
print("sample replay data inserted successfully!")

res = table.scan()

items = res.get("Items", [])

for item in items:
    print(item)