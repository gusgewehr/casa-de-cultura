window.addEventListener("load", function(e){
    
    const event_dates = JSON.parse(document.getElementById('event_dates').textContent);		

    const event_dates_json = $.parseJSON("{ \"event_dates\": " + event_dates + "}")

    event_dates_json["event_dates"].forEach(element => {
        date = element["fields"]

        start_date = new Date(date["start_date"])
        end_date = new Date(date["end_date"])



        add_date(
            start_date.getDate()+"/"+start_date.getMonth()+"/"+start_date.getFullYear(), 
            start_date.getHours()+":"+start_date.getMinutes(), 
            end_date.getHours()+":"+end_date.getMinutes(), 
            date["uso"]
        )
    });
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