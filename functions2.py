
def hash_string(input_string):
    # Using SHA-256 hash function
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

    # Truncate to 8 characters
    truncated_hash = sha256_hash[:8].replace("/", "g")

    return truncated_hash

def get_articles(hash_list):
    output = []
    color_dict = {
        'Literature': '#FF5733',
        'Analysis': '#024f9c',
        'Foreign Policy': '#33FF57',
        'Agriculture': '#029c5c',
        'Opinion': '#9c021c'
    }

    for article_hash in [a.replace("\n", "") for a in hash_list]:
        element = {}
        element["hash"] = article_hash
        with open(f"static/metad/{article_hash}.txt") as file:
            metadata = file.readlines()
            element["summary"] = metadata[0]
            element["category"] = metadata[1]
            element["title"] = metadata[2]
            element["author"] = metadata[3]
            element["color"] = color_dict[metadata[1].replace("\n", "")]

        output.append(element)
    return output

    '''<!--meta.write(summary + '\n')
            meta.write(category + '\n')
            meta.write(title + '\n')
            meta.write(author)-->'''


