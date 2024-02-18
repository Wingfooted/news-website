from flask import Flask, render_template, session, redirect, url_for, request
import base64
import os
import hashlib
import ast
import time
from database import Database
from functions import get_article, write, get_homepage, hash_string

app = Flask(__name__)

app.secret_key = "VGTYJKNIJ03MS77O@J#MSOIK49MDK53F722JISD<FN58029KSAANGG3B5F0NMA11MKFUHNAM"

db_connection = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mariaw57!', 
    'database': 'anthropologie'
}

app.config["db"] = Database( **db_connection )

app.config["category_ids"] = {
    "Analysis": 1,
    "Opinion": 2,
    "Culture": 3, 
    "Literature": 4,
    "Markets": 5,
    "Philosophy": 6
}

@app.route("/", methods=["GET", "POST"])
def index():
    db = app.config["db"]
    homepage = get_homepage(db)
    print(homepage)
    return render_template("main.html", articles=homepage)

@app.route("/a/<article_id>")
def article(article_id):
    db = app.config['db']
    #rendering the article
    article = get_article(db, article_id)
    if article['status'] == 200:
        print(article)
        return render_template('article.html', article=article)

    else: 
        return redirect(url_for("index"))

@app.route("/c/<category>")
def category(category):
    return render_template("category.html")

@app.route("/editor", methods=["GET", "POST"])
def editor():
    
    if request.method == "GET":
        if not 'user' in session:
            return redirect(url_for('login'))

    elif request.method == "POST":
        if not 'user' in session:
            return redirect(url_for('login'))
        
        author = request.form['author']
        category = request.form["category"]
        title = request.form.get("title")
        summary = request.form.get("summary")

        article_hash = hash_string(title)
        #thumbnail
        thumbnail = request.files["thumbnail"] if "thumbnail" in request.files else None
        if thumbnail:
            thumbnail.save(os.path.join('static/images', f"{article_hash}.png"))

        content = []

        form = ast.literal_eval(request.form["form-data"])
        img_count = 1
        for id_element in form:
            #all element id's follow the format where it is first name, then the UID
            element_content = request.form.get(id_element)
            element_type = id_element.split("-")[0]
            if element_content or element_type== "img":
                if element_type == "text":
                    content.append(("t", element_content))
                elif element_type == "sub":
                    content.append(("s", element_content))
                elif element_type == "quote":
                    content.append(("q", element_content))
                elif element_type == "img":
                    if id_element in request.files:
                        img = request.files[id_element]
                        if img:
                            img.save(os.path.join('static/articleimages', f"{article_hash}_{img_count}.png"))
                            content.append(("i",os.path.join('/static/articleimages', f"{article_hash}_{img_count}.png")))
                            img_count+=1
                            
        #write the article file
        if article_hash == hash_string(""):
            #no article title
            return redirect(url_for("editor"))
        elif f"{article_hash}.t xt" in os.listdir('static/articles'):
            #article title allready exists
            return redirect(url_for("editor"))
        else:
            #article can be created

            db = app.config["db"]
            get_category_id = app.config["category_ids"]
            print("content", content)
            write(db, 
                title=title,
                summary=summary,
                content='\n'.join([str(element_tuple) for element_tuple in content]),
                author_name=author,
                category_id=get_category_id[category],
                article_thumbnail=(
                    os.path.join('static/images', f"{article_hash}.png")
                ),
                tags=[]
            )

            #title, summary, content, author_name, category_id, article_thumbnail, tags=[]

            #OLD code
            '''with open(f"static/articles/{article_hash}.txt", "w") as article:
                for line in content:
                    article.write(str(line) + '\n')
            
            with open(f"static/metad/{article_hash}.txt", "w") as meta:
                meta.write(summary + '\n')
                meta.write(category + '\n')
                meta.write(title + '\n')
                meta.write(author)'''

        
        return redirect(url_for('article', article_id=article_hash, _external=True))

    return render_template('editor.html', author=session['user'])     

@app.route("/login", methods=["GET", "POST"])
def login():
    
    #WIP Authenticate User Method

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            with open("static/usernames.txt", "r") as file:
                for line in file.readlines():
                    if username == "alexander" and password == "wells":
                        session["user"] = line.split(",")[2]
                        return redirect(url_for("editor"))

    elif request.method == "GET":
        pass
    
    return render_template("login.html")

@app.route("/maintenance")
def maintenance():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True, port=8000)

