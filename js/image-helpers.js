
var loadFile = function(event) {
    var reader = new FileReader();
    reader.onload = function(){
        $(".img_div").hide();

        var big_preview = document.getElementById('big_preview_img');
        big_preview.src = reader.result;

        big_preview.onload = function() {
            var small_preview = document.getElementById('preview_scaled_img');
            small_preview.src = resize(big_preview.src);
            big_preview.onload = null;

            small_preview.onload = function() {
                testImage_NoVis(small_preview);
                small_preview.onload = null;
            }

        $(".img_div").show();
    }
};

reader.readAsDataURL(event.target.files[0]);
};

function centerCrop(src){
    var image = new Image();
    image.src = src;
    image.onload = function() {
        var max_width = Math.min(image.width, image.height);
        var max_height = Math.min(image.width, image.height);

        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext("2d");

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width = max_width;
        canvas.height = max_height;
        ctx.drawImage(image, (max_width - image.width)/2, (max_height - image.height)/2, image.width, image.height);
        return canvas.toDataURL("image/png");
    }
}

function resize(src){
    var image = new Image();
    image.src = src;

    var canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0, image.width, image.height);

    var dst = document.createElement('canvas');
    dst.width = image_dimension;
    dst.height = image_dimension;

    window.pica.WW = false;
    window.pica.resizeCanvas(canvas, dst, {
    quality: 2,
    unsharpAmount: 500,
    unsharpThreshold: 100,
    transferable: false
  }, function (err) {  });
    window.pica.WW = true;
    return dst.toDataURL("image/png");
}

