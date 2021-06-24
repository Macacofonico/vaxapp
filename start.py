import os
from flask import Flask
app = Flask("demm2021")


@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/esempio')
def esempio():
  return  '{"message":"sono nella route esempio"}'



if __name__ == "__main__":
  port =  int(os.getenv("WEBPORT",5000))
  host = os.getenv("WEBHOST",'0.0.0.0')
  app.run(host=host, port=port)



