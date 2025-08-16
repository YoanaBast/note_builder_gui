Python + CS Notes

These are my Python + CS notes, sorted as pop-up buttons on an HTML page.
They are focused on things I have struggled with or found amusing and may not be entirely useful to a new learner.

As I don't want to type new code for each section, I have created a basic Thinker app to do it for me.
It only takes my input—category name and content.

My goal here is to encounter real project issues, as well as come back and optimize or recreate stuff as I learn and grow.

How it works

The Thinker app adds categories and content using the methods in the AddContentToPage class.

They add templated HTML code as strings, replacing the category name and content.

Adding categories:

The addition of categories happens by replacing the placeholder below:

<!-- INSERT_CATEGORIES_HERE -->


The placeholder is replaced by content and added below it to allow adding new categories to the HTML file.

Adding content in a category:

The addition of content in a category happens via the placeholder below, using similar logic:

<!--CONTENT-{category_name}-->


The CSS is magic, and I'm just happy it works.
