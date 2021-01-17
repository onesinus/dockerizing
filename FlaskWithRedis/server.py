from flask import Flask, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello_world():
    name = request.args.get('name', 'Anonym')
    existing_value = redis.get('/') or ""
    new_value = f"{existing_value},{name}"
    redis.set("/", new_value)
    return f'Hello, {name}!'    

@app.route('/get-data')
def redis_data():
    data = redis.get('/') or ""
    return data

@app.route('/delete-data')
def redis_remove():
    redis.delete('/')
    return "ok"

@app.route('/flush-data')
def redis_flush():
    redis.flushall()
    return "ok"

@app.route('/bom-data')
def bom_bayah():
    data = []
    for i in range(99999):
        data.append(i)
    
    redis.set('/', str(data))
    return "ok"
