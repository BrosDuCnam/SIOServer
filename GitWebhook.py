import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Code pour traiter la requête webhook et effectuer un "git merge"
    git_marge()
    return "OK", 200

def git_marge():
    # Code to perform a git merge
    os.system("git fetch")
    os.system("git merge")
    os.system("git pull")
    os.system("screen -X -S vwm-server quit")
    os.system("pip install -r requirements.txt")
    os.system("screen -S vwm-server python3 main.py")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)