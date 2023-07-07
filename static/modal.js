$('.del_event').click(function() {
    var $thumb = $(this);
    event_id = $thumb.attr('value');

    $("#delete_event").attr("value", event_id);

    $("#tiny_modal").attr("style", "display: flex");

  });


function open_tiny_modal(event_id = none){

    $("#delete_event").attr("value", event_id);

    $("#tiny_modal").attr("style", "display: flex");
}