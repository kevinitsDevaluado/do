var toggler = document.getElementsByClassName("hijo");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".padre").classList.toggle("active");
    this.classList.toggle("hijo-down");
    
  });
}