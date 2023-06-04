window.addEventListener("load", function(e){
    
  


});


number_of_dates = 0
dates_list = []

function update_number_of_dates() {
    var num = document.getElementById("number_of_dates")

    num.setAttribute("value", number_of_dates)
}

function add_date(date, start_time, end_time, type){
    
    var pai = document.getElementById("date-fields")


    var new_div = document.createElement("div")
    new_div.setAttribute("id",'date_group_'+number_of_dates)
    
    pai.appendChild(new_div)


    var rm_date = document.createElement("button")
    rm_date.setAttribute("id", 'rm_date_'+number_of_dates)
    rm_date.setAttribute("value", number_of_dates)
    rm_date.setAttribute("onclick", `rm_date(${number_of_dates})`)
    rm_date.setAttribute('type', 'button')
    rm_date.textContent = "-"
    rm_date.setAttribute("class", "bg-transparent hover:bg-red-500 text-red-700 font-semibold hover:text-white py-2 px-4 border border-red-500 hover:border-transparent rounded")
    new_div.appendChild(rm_date)




    var filho = document.getElementById("date_group_"+number_of_dates)
    var new_date_input = document.createElement("input")
    new_date_input.setAttribute("name", "date_"+number_of_dates)
    new_date_input.readOnly = true
    new_date_input.setAttribute("type", "text")
    new_date_input.setAttribute("value", date)
    new_div.appendChild(new_date_input)

    var start_time_input = document.createElement("input")
    start_time_input.setAttribute("type", "text")
    start_time_input.readOnly = true
    start_time_input.setAttribute("name", "start_time_"+number_of_dates)
    start_time_input.setAttribute("value", start_time)
    new_div.appendChild(start_time_input)

    var end_time_input = document.createElement("input")
    end_time_input.setAttribute("type", "text")
    end_time_input.readOnly = true
    end_time_input.setAttribute("name", "end_time_"+number_of_dates)
    end_time_input.setAttribute("value", end_time)
    new_div.appendChild(end_time_input)


    var type_input = document.createElement("input")
    type_input.setAttribute("type", "text")
    type_input.readOnly = true
    type_input.setAttribute("name", "type_"+number_of_dates)
    type_input.setAttribute("value", type)
    new_div.appendChild(type_input)  

    
    number_of_dates++ 
    update_number_of_dates()   
    
}

function close_toast(){
    var toast = document.getElementById("toast-success")

    toast.setAttribute("style", "display: none")

    var toast2 = document.getElementById("toast-danger")

    toast2.setAttribute("style", "display: none")
}

function rm_date(value){
    var date = document.getElementById("date_group_"+value)

    date.remove()

    number_of_dates--
    update_number_of_dates()
}

function free_event_check(){
    if (document.getElementById("gratuito").checked) {
        document.getElementById("preco").disabled = true
        document.getElementById("meia").disabled = true
        document.getElementById("comunitario").disabled = true
    } else {
        document.getElementById("preco").disabled = false
        document.getElementById("meia").disabled = false
        document.getElementById("comunitario").disabled = false
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