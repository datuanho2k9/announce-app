# Annoucements  API
## How to install
1. You are going to need Python 3.x with Flask module installed.
2. Run main.py

## How to use
We have the following routes:
1. / GET
2. /announce POST
3. /download GET
4. /getposts GET
5. /getpost/`interger` GET

### /
**POST** \
The main route, return `Hello world`
### /announce
**POST** \
It is used with the following HTML form
```html
    <form target="_blank" action="/announce" method="POST" enctype="multipart/form-data">
        <input type="text" name="note" />
        <input type="file" name="files" multiple />
        <button type="submit">Submit</button>
    </form>
```
It will return a friendly message and at the bottom it will shows the processed data.
### /download
**GET** \
Use with `/download?id="postId"?filename="filename"` with **postId** is the id of the annoucement generated in `/announce`, **filename** is the name of the uploaded file.
### /getposts
**GET** \
Get all of the existing posts in `./database/posts.json`, returning them as an array string.
### /getpost/`interger`
**GET**
Read `./database/posts.json`, and then return with specifed index in `interger` given in the route.

