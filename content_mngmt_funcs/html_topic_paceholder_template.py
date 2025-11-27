import textwrap
import random

tilt_number = random.randint(1, 5)

content_template = textwrap.dedent(f"""\
<!-- TITLE_NAME -->
<div class="grid-item">
    <button id="openBtn-TITLE_ID" class="tilt{tilt_number}">TITLE_NAME</button>
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
