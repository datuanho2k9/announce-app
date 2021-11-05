from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import requests
import uuid
import json
from flask_cors import CORS
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./files"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000
CORS(app)


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
        "http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh").json()[
            "datetime"]  # Mine is at Asia/Ho_Chi_Minh
    postData["content"] = request.form.get("note")  # Set content of the post
    # Processing files input and save it
    files = request.files.getlist("files")
    # Make directory or it will raise an error
    os.mkdir(f"./files/{postData['id']}")
    for file in files:  # Looping through files
        if file.filename != '':
            # Incase they are a hacker
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], postData["id"],
                             filename))  # save file
            postData["filesLink"].append({
                "link": f"https://127.0.0.1:5000/download?id={postData['id']}&filename={filename}",
                "name": f"{filename}"
            }
            )

    postsAndParsed = []
    with open("./database/posts.json", "r") as posts:
        postsAndParsed = json.load(posts)
    with open("./database/posts.json", "w") as posts:
        postsAndParsed.append(postData)
        json.dump(postsAndParsed, posts, ensure_ascii=False, indent=4)

    # Returning data and testing.
    return postData


@app.route("/download/")
def download():
    try:
        # Download file according to the post id and the filename
        announcementId = request.args["id"]
        filename = request.args["filename"]
        return send_file(f"./files/{announcementId}/{filename}")
    except Exception as e:
        return str(e)
        # Sometime there is unknown file error, so we return it here


@app.route("/getposts")
def getPosts():
    request = None
    with open("./database/posts.json", "r") as posts:
        request = str(json.dumps(json.load(posts)))
    return request


@app.route("/lastpost")
def lastPost():
    request = None
    with open("./database/posts.json", "r") as posts:
        data = json.load(posts)[-1]
        request = json.dumps(data)
    return request


@app.route("/getpost/<int:no>")  # Get posts by the number, lastest is -1
def getPost(no):
    requested = None
    no = no - 1
    with open("./database/posts.json", "r") as posts:
        try:
            data = json.load(posts)[no]
            requested = json.dumps(data)
        except IndexError:
            # Sometimes it should be out of range error.(most of the time)
            requested = ["IndexError"]
        except Exception as e:
            requested = [e]

    return requested


if __name__ == "__main__":
    if(os.path.exists(os.getcwd() + "/database/posts.json") == False):
        with open("./database/posts.json", "w") as posts:
            json.dump([], posts)
    if(os.path.exists(os.getcwd() + "files/") == False):
        os.mkdir(os.getcwd() + 'files')
    app.run(debug=True)
