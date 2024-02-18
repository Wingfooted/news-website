    
    if request.method == "POST":
        #generic form data - consisntent to form, as in all forms will have it
        #    author, category, publication
        #dynamic form data - different from form to form. 

        #construct article
        form = ast.literal_eval(request.form["form-data"])
        content = []
        content_type = []

        #getting generic form data
        publication = request.form["publication"]
        author = request.form["author"]
        category = request.form["category"]

        #dynamic form data
        title = request.form.get("title")
        summary = request.form.get("summary")

        print(form)
        for element in form:
            element_content = request.form.get(element)
            print(element, element_content)
            if element_content or (element.split('-')[0] == "img"):
                element_type = element.split('-')[0]
                if element_type == "text":
                    content.append(f"<p class='content-text'>{element_content}</p>")
                elif element_type == "sub":
                    content.append(f"<p class='subheading-text'>{element_content}</p>")
                elif element_type == "quote":
                    content.append(f"<p class='quote-text'>{element_content}</p>")
                elif element_type == "img":
                    print("image type detected")
                    print(request.files)
                    if element in request.files:
                        file = request.files[element]

                        if file.filename == '':
                            print("file here")
                        
                        elif file:
                            old_filename = file.filename.split(".")
                            filename = str(int(time.time())) + old_filename[1] + ".png"
                            print(os.path.join('static/images', filename))

                            file.save(os.path.join('static/images', filename))

                            print(os.access)
                            
                            print("uploaded file")

                            content.append(f"""
                            <div class='image-wrapper'> 
                                <img src='{os.path.join('/static/images', filename)}' alt='{filename}' class="image">
                            </div>
                            """)
                    else:
                        print("FSR no file in requests")
        
        if len(content) == 0:
            return redirect(url_for("manager")) #WIP make this unseccsessful/error screen
        else:
            print(publication, title, summary, author, category)
            db.create_article(
                publication=publication
                , title=title
                , summary=summary
                , author=author
                , category=category
                , content="\n".join(content) 
            )

            '''publication
                    , title
                    , sub_title
                    , summary
                    , author
                    , publish_date
                    , category
                    , content
                    , url
                    , live
                    , input_tags'''

            return redirect(url_for("landing"))
