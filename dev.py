from app import app
import os

port = 8888
if os.getenv('PORT'):
    port = int(os.environ['PORT'])

app.run(host='0.0.0.0', port=port)
