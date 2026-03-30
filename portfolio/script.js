(function(){
emailjs.init("_tgbVZ_6QvpqIQkwY");
})();

document.getElementById("contactForm").addEventListener("submit", function(event){

event.preventDefault();

emailjs.sendForm(
"service_xbmpzcu",   
"template_le5vdha",
this
)
.then(function() {
alert("Message sent successfully!");
}, function(error) {
alert("Failed to send message");
});

});