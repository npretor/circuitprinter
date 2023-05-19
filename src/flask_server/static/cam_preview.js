// From https://github.com/VolteraInc/camera/blob/InitialCommits/volteracamera/web_server/static/cam_preview.js
"use strict";



(function reload_image() {
var url = '/cam_image'
fetch(url, {cache: "no-store"}).then(function(response) {
  if(response.ok) {
    response.blob().then( function(blob) {
      var objectURL = URL.createObjectURL(blob);
      var img = document.getElementById('preview_image');
      img.src = objectURL;
      setTimeout (reload_image, 500);
      console.log("cam preview script")
    });
  } else {
    console.log('Network request for camera image failed with response ' + response.status + ': ' + response.statusText);
  }
});
})();
