/*
 * ---------------------------------------------------------------------------
 * - Define variables
 * - Calculate the document height and set the offset to a quarter of that value
 * - Add event listeners for scroll and click
 * ----------------------------------------------------------------------------
 */

var btn = document.querySelector(".back-to-top"),
  body = document.body,
  npc = document.querySelector(".npc"),
  top_header = document.querySelector(".top"),
  docElem = document.documentElement,
  cd_header = document.querySelector(".cd-header"),
  offset = 200,
  scrollPos,
  docHeight,
  isFireFox = navigator.userAgent.toLowerCase().indexOf("firefox") > -1;

//  Calculate the document
docHeight = Math.max(
  body.scrollHeight,
  body.offsetHeight,
  docElem.clientHeight,
  docElem.scrollHeight,
  docElem.offsetHeight
);
if (docHeight != "undefined") {
  offset = docHeight / 5;
}

//  Add scroll Event lisner
body.addEventListener("scroll", function (event) {
  scrollPos = body.scrollTop || docElem.scrollTop;
  if (btn) btn.className = scrollPos > offset ? "back-to-top visible" : "back-to-top";
  npc.className = scrollPos > offset ? "nav npc change" : "nav npc";
  top_header.className = scrollPos > offset ? "top change" : "top";
  cd_header.className = scrollPos > offset ? "cd-header change" : "cd-header";
});

if (btn) {
  btn.addEventListener("click", function (e) {
    e.preventDefault();

    if (isFireFox) {
      docElem.scrollTop = "0";
    } else {
      body.scrollTop = 0;
    }
  });
}
var logout_show_btn = document.querySelectorAll(".logout");
var logout_popup = document.querySelector(".logout-popup");

function logout_show() {
  logout_popup.classList.add("show");
}
function logout_close() {
  logout_popup.classList.remove("show");
}
