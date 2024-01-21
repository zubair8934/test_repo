from app import app
from flask import render_template
import boto3
import os

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_REGION', 'us-east-1')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cat')
def cat():
	dynamodb = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	table = dynamodb.Table('ServerCount')
	table.update_item(Key={'server_id': 1},
        UpdateExpression=f"SET {'cat_server_count'} = {'cat_server_count'} + :val", 
        ExpressionAttributeValues={':val': 1})
	cat_image_url = get_s3_url('cat.jpg')
	return render_template('cat.html', cat_image_url=cat_image_url)

@app.route('/dog')
def dog():
	dynamodb = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	table = dynamodb.Table('ServerCount')
	table.update_item(Key={'server_id': 1},
        UpdateExpression=f"SET {'dog_server_count'} = {'dog_server_count'} + :val",
        ExpressionAttributeValues={':val': 1})
	dog_image_url = get_s3_url('dog.jpg')
	return render_template('dog.html', dog_image_url=dog_image_url)

@app.route('/count')
def count():
    dynamodb = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    table = dynamodb.Table('ServerCount')
    response = table.get_item(Key={'server_id': 1})
    if 'Item' in response:
        cat_server_count = response['Item'].get('cat_server_count')
        dog_server_count = response['Item'].get('dog_server_count')
        return render_template('request_count.html', cat_server_count=cat_server_count, dog_server_count=dog_server_count)
    else:
        return "Item not found"
	
def get_s3_url(object_key):
    s3 = boto3.client('s3', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    url = s3.generate_presigned_url('get_object', Params={'Bucket': "flask-s3-8934", 'Key': object_key}, ExpiresIn=3600)
    return url

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
