import textwrap

content_template = textwrap.dedent("""\
        <!-- TITLE -->
        <div class="grid-item">
            <button id="openBtn-TITLE">TITLE</button>
            <div id="myModal-TITLE" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>TITLE</h2>
                    <p><!--CONTENT-TITLE--></p>
                </div>
            </div>
            <script>
                const modalTITLE = document.getElementById("myModal-TITLE");
                const btnTITLE = document.getElementById("openBtn-TITLE");
                const spanTITLE = modalTITLE.querySelector(".close");

                btnTITLE.onclick = () => modalTITLE.style.display = "block";
                spanTITLE.onclick = () => modalTITLE.style.display = "none";
                window.onclick = (event) => {
                    if(event.target === modalTITLE) modalTITLE.style.display = "none";
                }
            </script>
        </div>
        <!-- ENF OF TITLE -->
    """)