window.addEventListener("load", function(e){
    
    const event_dates = JSON.parse(document.getElementById('event_dates').textContent);		

    const event_dates_json = $.parseJSON("{ \"event_dates\": " + event_dates + "}")

    console.log(event_dates_json)

    event_dates_json["event_dates"].forEach(element => {
        date = element["fields"]

        start_date = new Date(date["start_date"])
        end_date = new Date(date["end_date"])

        day = start_date.getDate()
        if(parseInt(day) < 10){
            day = '0'+day
        }

        
        month = start_date.getMonth()+1
        if(parseInt(month) < 10){
            month = '0'+month
        }

        start_hour = start_date.getHours()
        if(parseInt(start_hour) < 10){
            start_hour = '0'+start_hour
        }


        end_hour = end_date.getHours()
        if(parseInt(end_hour) < 10){
            end_hour = '0'+end_hour
        }

        start_min = start_date.getHours()
        if(parseInt(start_min) < 10){
            start_min = '0'+start_min
        }


        end_min = end_date.getHours()
        if(parseInt(end_min) < 10){
            end_min = '0'+end_min
        }


        add_date(
            day+"/"+month+"/"+start_date.getFullYear(), 
            start_hour+":"+start_min, 
            end_hour+":"+end_min, 
            date["uso"],
            element["pk"]
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