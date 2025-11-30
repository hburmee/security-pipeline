from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from secure DevSecOps pipeline!"

if __name__ == "__main__":
    # For local testing only; in Docker we'll use gunicorn or flask's dev server
    app.run(host="0.0.0.0", port=5000)


#Bearer N2VjYzI2YjMtZWQxNC00YjAxLWJiZTQtZWY3Yjc4M2YzMDc5YzllNmM5NTEtYjI4_P0A1_13494cac-24b4-4f89-8247-193cc92a7636
# 6d089b90-c051-11f0-b550-a16ba4dd4e16