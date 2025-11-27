import textwrap

category_template = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=0.6, maximum-scale=3.0">
<title>{CATEGORY_NAME} topics</title>
<link rel="stylesheet" href="style.css">
</head>
    <body>
    <script src="scripts/modal.js"></script>
        <h1 class="content">Welcome to my fridge door! </h1>
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
    <script src="scripts/magnets.js"></script> 
    <script src="scripts/gridColors.js"></script>
    <script src="scripts/navColors.js"></script>

    </body>

</html>
""")
