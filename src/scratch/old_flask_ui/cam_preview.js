"use strict";

console.log('is this even running?')

(function reload_image() {
  //console.log('reload_image was run')
  var url = '/cam_image'
  fetch(url, {cache: "no-store"}).then(function(response) {
    if(response.ok) {
      response.blob().then( function(blob) {
          //console.log('camPreview was run')
          var objectURL = URL.createObjectURL(blob);
          console.log(objectURL)
          var img = document.getElementById('preview_image');
          img.src = objectURL;
          console.log(img.src)
          setTimeout (reload_image, 500);
      });
    } else {
      console.log('Network request for camera image failed with response ' + response.status + ': ' + response.statusText);
    }
});
})();