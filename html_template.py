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
        const modalTITLE_ID = document.getElementById("myModal-TITLE_ID");
        const btnTITLE_ID = document.getElementById("openBtn-TITLE_ID");
        const spanTITLE_ID = modalTITLE_ID.querySelector(".close");

        btnTITLE_ID.onclick = () => modalTITLE_ID.style.display = "block";
        spanTITLE_ID.onclick = () => modalTITLE_ID.style.display = "none";
        window.onclick = (event) => {
            if(event.target === modalTITLE_ID) modalTITLE_ID.style.display = "none";
        }
    </script>
</div>
<!-- END OF TITLE_NAME -->
""")
