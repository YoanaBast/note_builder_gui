These are my python + CS notes, sorted as pop-up buttons on an HTML page. 
They are focused on things I have struggled with or found amusing and may not bee entirely useful to a new learner. 

As I don't want to type new code for each section, I have created a basic thinker app to do it for me, 
it only takes my input - category name and content. 

My goal here is to encounter real project issues, as well as come back and optimize or recreate stuff as I learn and grow. 

Web page: https://yoanabast.github.io/note_builder_gui/
The GUI app runs when staring the gui_main.py file. 

How it works:
    The thinker app adds categories and content using the methods in the AddContentToPage class. 
    They add templated HTML code as strings, replacing the category name and content.

    The addition of categories happens by replacing the placeholder below:
        "<!-- INSERT_CATEGORIES_HERE -->",

    The placeholder is replaced by content and added below it to allow adding new categories to the HTML file.
    
    The addition of contect in a category happens via the placeholder below, using similar logic:
        f"<!--CONTENT-{category_name}-->"

    The css is magic and I'm just happy it works.   