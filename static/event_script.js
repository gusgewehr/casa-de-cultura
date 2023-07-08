

$('.thumbnail').click(function() {
    var $thumb = $(this);
    img_src = $thumb.find('img').attr('src');
    
    $("#modal_img").attr("src", img_src);


    $(".image_modal").attr("style", "display: flex");

  });


