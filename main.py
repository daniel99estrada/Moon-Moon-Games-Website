from flask import Flask, request, render_template
import boto3

AWS_ACCESS_KEY = "AKIA5UD2B5HDXF5XQUMR"
AWS_SECRET_KEY = "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"
AWS_REGION_NAME = "us-east-1"

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    newsletter = request.form.get('newsletter', False)

    # Create an AWS session
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION_NAME
    )

    # Save the response values in AWS DynamoDB table
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('Messages')
    table.put_item(
        Item={
            'name': name,
            'email': email,
            'message': message,
            'newsletter': newsletter
        }
    )
    return 'Message submitted successfully!'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
