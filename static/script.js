function close_modal(){
    $("#modal").attr("style", "display: none");
    $("#tiny_modal").attr("style", "display: none")
}

document.addEventListener(
    "click",
    function(event) {
      // If user either clicks X button OR clicks outside the modal window, then close modal by calling closeModal()
        if ( event.target.matches(".btn_close_modal") ||
            event.target.matches(".modal")
        ) {
          close_modal()
        }
    },
    false
  )



function free_event_check(){
    if (document.getElementById("gratuito").checked) {
        document.getElementById("preco").disabled = true
        document.getElementById("preco").value = ''

        document.getElementById("meia").disabled = true
        document.getElementById("comunitario").disabled = true
    } else {
        document.getElementById("preco").disabled = false
        document.getElementById("meia").disabled = false
        document.getElementById("comunitario").disabled = false
    }
}

function close_toast(){
    try{
        var toast = document.getElementById("toast-success")
    
        toast.setAttribute("style", "display: none")
    }
    catch{
        var toast2 = document.getElementById("toast-danger")
    
        toast2.setAttribute("style", "display: none")
    }
}


function imagePreview() {
    const pictureImage = document.querySelector(".picture__image");

    const inputFile = document.querySelector("#picture__input");
    const file = inputFile.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener("load", function (reader) {
            const readerTarget = reader.target;

            const img = document.createElement("img");
            img.src = readerTarget.result;
            img.classList.add("picture__img");

            pictureImage.innerHTML = "";
            pictureImage.appendChild(img);
        });

        reader.readAsDataURL(file);
    } else {
        pictureImage.innerHTML = "Escolha uma imagem para o banner";
    }
}

function horizontalScroll (event) {
    event.preventDefault();

    const element = document.querySelector("#event-images");
    element.scrollBy({
      left: event.deltaY < 0 ? -50 : 50,
    })

}


function imageAddEvents() {
    
    var eventImages = document.querySelector("#event-images");
    
    var inputFile = document.querySelector("#pictures_event_input");

    
    eventImages.innerHTML = '';

    for(var i = 0; i< inputFile.files.length ; i++) {
        file = inputFile.files[i]        

        if (file) {
            const reader = new FileReader();
    
            reader.addEventListener("load", function (reader) {
                const readerTarget = reader.target;
    
                const img = document.createElement("img");
                img.setAttribute("class", "block max-h-full p-1")
    
                img.src = readerTarget.result;
    
                eventImages.append(img); 
            });
    
            reader.readAsDataURL(file);
        } else {
            pictureImage.innerHTML = "Escolha outras imagens para o evento (você pode selecionar mais de uma imagem de uma vez)";
        }
    };

}
