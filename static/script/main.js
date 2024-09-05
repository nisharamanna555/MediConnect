if (document.getElementById("index.html")) {  // index.html
    console.log("index.html")
} else {    // user page
    let userIcon = document.getElementById("userIcon");
    userIcon.addEventListener("click", (e) => {
        let hiddenBar = document.getElementById("hiddenBar");
        if (hiddenBar.style.display === "block") {
            hiddenBar.style.display = "none";
        } else {
            hiddenBar.style.left = userIcon.offsetLeft + "px";
            hiddenBar.style.top = (userIcon.offsetTop + 50) + "px";
            hiddenBar.style.display = "block";
        }
    });
}