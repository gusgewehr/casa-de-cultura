window.addEventListener("load", function(e){
    
  


});


number_of_dates = 0

function update_number_of_dates() {
    var num = document.getElementById("number_of_dates")
    console.log(number_of_dates)

    num.setAttribute("value", number_of_dates)
}

function add_date(date, start_time, end_time, type){
    console.log("entrou aqui mesmo")
    
    var pai = document.getElementById("date-fields")

    console.log(pai)

    var new_div = document.createElement("div")
    new_div.setAttribute("id",'date_group_'+number_of_dates)
    new_div.setAttribute("style", "display: none")
    pai.appendChild(new_div)

    var filho = document.getElementById("date_group_"+number_of_dates)
    var new_date_input = document.createElement("input")
    new_date_input.setAttribute("name", "date_"+number_of_dates)
    new_date_input.setAttribute("type", "hidden")
    new_date_input.setAttribute("value", date)
    new_div.appendChild(new_date_input)

    var start_time_input = document.createElement("input")
    start_time_input.setAttribute("type", "hidden")
    start_time_input.setAttribute("name", "start_time_"+number_of_dates)
    start_time_input.setAttribute("value", start_time)
    new_div.appendChild(start_time_input)

    var end_time_input = document.createElement("input")
    end_time_input.setAttribute("type", "hidden")
    end_time_input.setAttribute("name", "end_time_"+number_of_dates)
    end_time_input.setAttribute("value", end_time)
    new_div.appendChild(end_time_input)


    var type_input = document.createElement("input")
    type_input.setAttribute("type", "hidden")
    type_input.setAttribute("name", "type_"+number_of_dates)
    type_input.setAttribute("value", type)
    new_div.appendChild(type_input)  

    number_of_dates++
    update_number_of_dates()
}

function rm_date(value){
    var date = document.getElementById("data_groupo_"+value)

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
