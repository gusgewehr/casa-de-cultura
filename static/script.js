window.addEventListener("load", function(e){
    
  


});


number_of_dates = 0

function add_date(){
    var pai = document.getElementById("date-fields")

    var new_div = document.createElement("div")
    new_div.setAttribute("id",'data_groupo_1')
    new_div.setAttribute("class", 'flex gap-x-4 sm:col-span-3')
    pai.appendChild(new_div)

    var filho = document.getElementById("data_groupo_1")
    var new_date_input = document.createElement("input")
    new_date_input.setAttribute("name", "data")
    new_date_input.setAttribute("type", "date")
    new_date_input.setAttribute("class", "block w-full rounded-md border-0 px-3.5 py-2 pl-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6")
    new_div.appendChild(new_date_input)

    var new_time_input = document.createElement("input")
    new_time_input.setAttribute("type", "time")
    new_time_input.setAttribute("name", "hora")
    new_time_input.setAttribute("class", "block w-full rounded-md border-0 px-3.5 py-2 pl-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6")
    new_div.appendChild(new_time_input)

    var new_type_select = document.createElement("select")
    new_type_select.setAttribute("name", "tipo")
    new_type_select.setAttribute("class", "h-full rounded-md border-0 bg-transparent bg-none py-0 pl-4 pr-9 text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm")


    var selectOptions = {"AP": "Apresentação", "EN":"Ensaio", "MNT":"Montagem do Palco", "DMNT":"Desmontagem do Palco"}
    for (const [key, value] of Object.entries(selectOptions)) {
        var option = document.createElement("option");
        option.text = value;
        option.setAttribute("value", key)
        new_type_select.add(option);
    }
    new_div.appendChild(new_type_select)

    number_of_dates++
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

    number_of_dates++
}
