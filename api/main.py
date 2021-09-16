from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import requests
import uuid
import json
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './files'


@app.route("/")
def home():
    # Test routing
    return "Hello world"


@app.route("/announce", methods=["POST"])
def announce():
    # Set existing post data
    postData = {
        "time": "",
        "id": str(uuid.uuid4()),  # Generate custom uid
        "content": "",
        "filesLink": []
    }

    # Setting time, using datetime module is more complex.
    postData["time"] = requests.get(
        "http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh").json()["datetime"]  # Mine is at Asia/Ho_Chi_Minh
    postData["content"] = request.form.get('note')  # Set content of the post
    # Processing files input and save it
    files = request.files.getlist('files')
    # Make directory or it will raise an error
    os.mkdir(f'./files/{postData["id"]}')

    for file in files:  # Looping through files
        filename = secure_filename(file.filename)  # Incase they are a hacker
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], postData["id"], filename))  # save file
        postData["filesLink"].append(
            f"http://127.0.0.1:5000/download?id={postData['id']}&filename={filename}")

    postsAndParsed = []
    with open("./database/posts.json", 'r') as posts:
        postsAndParsed = json.load(posts)
    with open('./database/posts.json', 'w') as posts:
        postsAndParsed.append(postData)
        json.dump(postsAndParsed, posts, ensure_ascii=False, indent=4)

    # Returning data and testing.
    return '''<h3>Response has been recieved</h3><h4>Close this window/tab</h4><p>Data:''' + str(postData)


@app.route("/download/")
def download():
    try:
        # Download file according to the post id and the filename
        announcementId = request.args["id"]
        filename = request.args["filename"]
        return send_file(f"./files/{announcementId}/{filename}")
    except Exception as e:
        return e
        # Sometime there is unknown file error, so we return it here


@app.route("/getposts")  # Get all posts
def getPosts():
    with open("./database/posts.json", "r") as posts:
        return str(json.load(posts))  # Return all existing posts


@app.route("/getpost/<int:no>")  # Get posts by the number, lastest is -1
def getPost(no):
    print(no)
    requested = []

    with open("./database/posts.json", "r") as posts:
        try:
            requested = json.load(posts)[no]
        except IndexError:
            # Sometimes it should be out of range error.( most of the time)
            requested = ["IndexError"]
        except Exception as e:
            requested = [e]

    return str(requested)


if __name__ == "__main__":
    app.run()
