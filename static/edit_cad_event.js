window.addEventListener("load", function(e){
    
    //console.log(document.getElementById('event_images').textContent)

    const event_images = document.getElementById('event_images').textContent;		

    const event_images_json = $.parseJSON( event_images)

    teste = event_images_json["banner"]

    var banner = document.createElement("img")
    banner.src =  teste
 
    var pictureImage = document.querySelector(".picture__image")
    pictureImage.innerHTML = "";
    pictureImage.appendChild(banner);
        

    event_images_json["event_images"].forEach( element => {

                
        var image_event = document.createElement("img")
        image_event.src = element

        
        var eventImages = document.querySelector("#event-images")
        image_event.setAttribute("class", "block max-h-full p-1")
    
        eventImages.append(image_event); 
        


        
        
    })

    




});