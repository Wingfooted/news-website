import ast
import hashlib

def hash_string(input_string):
    # Using SHA-256 hash function
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

    # Truncate to 8 characters
    truncated_hash = sha256_hash[:9].replace("/", "g")

    return truncated_hash

def format(article):
    pass

def write(db, title, summary, content, author_name, category_id, article_thumbnail, tags=[]):
    
    #author_id

    author_name_id_dict = {
        "Alexander Wells": 1,
        "Daniel Tran": 2
    }

    if author_name_id_dict[author_name]:
        author_id = author_name_id_dict[author_name]
    else:
        author_id = 2


    db.write_article(title, summary, content, author_id, author_name, category_id, article_thumbnail, tags)

def id(input_string):
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

    # Convert hex to decimal (base 10)
    decimal_string = str(int(sha256_hash, 16))

    return decimal_string

def get_homepage(db):

    category_ids= {
    "Analysis": 1,
    "Opinion": 2,
    "Culture": 3, 
    "Literature": 4,
    "Markets": 5,
    "Philosophy": 6
    }
    category_colours = {
    "Analysis": "#FF0000",  # Red
    "Opinion": "#00FF00",   # Green
    "Culture": "#0000FF",   # Blue
    "Literature": "#FFFF00",  # Yellow
    "Markets": "#FF00FF",   # Magenta
    "Philosophy": "#00FFFF"  # Cyan
    }
    flipped_category_ids = {v: k for k, v in category_ids.items()}
    
    content = db.get_homepage()
    #print('content', content)

    output = {}

    for entry in content:
        if entry["section"] in output:
            #new position previously unidentified
            output[entry["section"]].append(entry["article_id"])
        
        elif entry["section"] not in output:
            #position previously not listed
            output[entry["section"]] = [entry["article_id"]]

    formatted_output = {}
    for key, value in output.items():
        print(key, value)
        if key not in formatted_output:
            formatted_output[key] = [get_article(db, article_id) for article_id in value]
        elif key in formatted_output:
            formatted_output[key].append(get_article(db, value))

    formatted_output_export = {}
    formatted_output_export["sections"] = []
    #grouping sections
    for key, value in formatted_output.items():
        print(key, value)
        scaffold = {
            "category_id": None,
            "category": None,
            "articles": []
        }
        if len(key) == 1:
            scaffold["category_id"] = int(key)
            scaffold["category"] = flipped_category_ids[int(key)]
            scaffold["articles"] = value

            formatted_output_export['sections'].append(scaffold)
            
        else:
            formatted_output_export[key] = value

    return formatted_output_export

def get_article(db, article_id):

    category_ids= {
    "Analysis": 1,
    "Opinion": 2,
    "Culture": 3, 
    "Literature": 4,
    "Markets": 5,
    "Philosophy": 6
    }
    category_colours = {
    "Analysis": "#1eb5a4",  
    "Opinion": "#af3f88",   
    "Culture": "#66b374",   
    "Literature": "#cf250b",  
    "Markets": "#f2a70d",   
    "Philosophy": "#0A1082"  
    }
    flipped_category_ids = {v: k for k, v in category_ids.items()}
    content = db.get_article(article_id)
    if content:
        content = content[0]
        view = {
            "thumbnail": content["article_thumbnail"],
            "title": content["title"],
            "summary": content["summary"],
            "author_id": content["author_id"],
            "category_id": content["category_id"],
            "article_id": article_id
        }
        
        metadata = {
            "article_id": content["article_id"],
            "category_id": content["category_id"],
            "category" : flipped_category_ids[content["category_id"]],
            "category_colour": category_colours[flipped_category_ids[content["category_id"]]]
        }

        #author_content = db.get_author(int(view["author_id"]))
        author_collection = {
            1: {
                "name": "Alexander Wells",
                "password": "W",
                "email": "alexanderjwells04@gmail.com",
                "summary": "I am Alexander"
            },
            2: {},
            3: {}
        }
        status = 404
        author_content = None
        if 1==1:
            print(int(view['author_id']))
            author_content =[ author_collection[int(view['author_id'])]]
            if author_content:

                status = 200
                print(author_content)
                author = {
                    "status": status,
                    "name": author_content[0]["name"],
                    "author_id": view["author_id"],
                    "author_summary": author_content[0]['summary']
                }
            else:
                author = {"status": status}
        
        print(content["content"])
        upload_content = [ast.literal_eval(line) for line in content["content"].split("\n")]
        print("upload_content", upload_content)
        return {
            "status": 200,
            "view": view,
            "metadata": metadata,
            "author": author,
            "content": upload_content
        }
    else: 
        return {
            "status": 404
        }