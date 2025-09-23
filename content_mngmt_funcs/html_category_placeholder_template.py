import textwrap

category_template = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{CATEGORY_NAME} topics</title>
<link rel="stylesheet" href="style.css">
</head>
    <body>
    <script src="scripts/modal.js"></script>
    <script src="scripts/responsive.js"></script>
        <h1>Programming sticky notes! &#x1F49C;</h1>
        <header>
            <nav>
                <a href="index.html">Python</a> |
                <a href="SQL.html">SQL</a> |
                <a href="CS.html">CS</a> |
            </nav>
        </header>
        
        <div id="grid">
        
        
        <!-- INSERT_CATEGORIES_HERE -->
        
        </div>
    
    <script src="scripts/modalColors.js"></script>
    </body>
</html>
""")
