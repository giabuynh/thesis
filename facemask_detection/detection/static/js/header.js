var upload = document.getElementById("nav-upload")
var realtime = document.getElementById("nav-realtime")

upload.onclick = function() {
    realtime.className = realtime.className.replace(" active", "");
    upload.className += " active";
};

realtime.onclick = function() {
    upload.className = upload.className.replace(" active", "");
    realtime.className += " active";
};