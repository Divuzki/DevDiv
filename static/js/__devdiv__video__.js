var devdivVideo, devdivVideo_juice, devdivVideo_btn, currentTime, durationTime, devdivVideo__seek;

function initalizeDevDivPlayer() {
  devdivVideo = document.querySelector("#devdiv__video");
  devdivVideo__seek = document.querySelector("#devdiv__videoBar__seek");
  devdivVideo_juice = document.querySelector(".devdiv__videoBar__juice");
  devdivVideo_btn = document.querySelector("#devdiv__play__pause");
  currentTime = document.querySelector("#current-time");
  durationTime = document.querySelector("#duration-time");
  devdivVideo_btn.addEventListener("click", devdiv__togglePlayPause, false);
  devdivVideo__seek.addEventListener("change", devdiv__vidSeek, false);
  devdivVideo.addEventListener("timeupdate", devdiv__timeUpdate, false);
}

window.onload = initalizeDevDivPlayer;

// Pause and Play Toggle
function devdiv__togglePlayPause() {
  if (devdivVideo.paused) {
    devdivVideo_btn.className = "pause";
    devdivVideo.play();
  } else {
    devdivVideo_btn.className = "play";
    devdivVideo.pause();
  }
}
// Player Seeker
function devdiv__vidSeek(){
  var seekTo = devdivVideo.duration * (devdivVideo__seek.value / 100);
  devdivVideo.currentTime = seekTo;
}

// Video Timing
function devdiv__timeUpdate () {
  var curmins = Math.floor(devdivVideo.currentTime / 60);
  var cursecs = Math.floor(devdivVideo.currentTime - curmins * 60);
  var durmins = Math.floor(devdivVideo.duration / 60);
  var dursecs = Math.round(devdivVideo.duration - durmins * 60);
  var juicePos = devdivVideo.currentTime / devdivVideo.duration;
  devdivVideo_juice.style.width = juicePos * 100 + "%";
  devdivVideo__seek.value = juicePos * 100;
  if (devdivVideo.ended) {
    devdivVideo_btn.className = "play";
  }
  if(cursecs < 10){
    cursecs = "0"+cursecs;
  }
  if(dursecs < 10){
    dursecs = "0"+dursecs;
  }
  if(curmins < 10){
    curmins = "0"+curmins;
  }
  if(durmins < 10){
    durmins = "0"+durmins;
  }
  currentTime.innerHTML = curmins+":"+cursecs;
  durationTime.innerHTML = durmins+":"+dursecs;
};
