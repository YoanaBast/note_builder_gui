import textwrap

content_template = textwrap.dedent("""\
<!-- TITLE_NAME -->
<div class="grid-item">
    <button id="openBtn-TITLE_ID">TITLE_NAME</button>
    <div id="myModal-TITLE_ID" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>TITLE_NAME</h2>
            <p><!--START-CONTENT-TITLE_ID--></p>
            <p><!--CONTENT-TITLE_ID--></p>
        </div>
    </div>
    <script>
        setupModal("myModal-TITLE_ID", "openBtn-TITLE_ID");
    </script>
</div>
<!-- END OF TITLE_NAME -->
""")
