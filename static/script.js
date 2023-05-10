window.addEventListener("load", function(e){
    
  


});


number_of_dates = 0

function add_date(){
    var pai = document.getElementById("form_body_general")

    var new_div = document.createElement("div")
    new_div.setAttribute("id",'data_groupo_1')
    new_div.setAttribute("class", 'flex gap-x-4 sm:col-span-3')
    pai.appendChild(new_div)

    var filho = document.getElementById("data_groupo_1")
    var new_date_input = document.createElement("input")
    new_date_input.setAttribute("class", "block w-full rounded-md border-0 px-3.5 py-2 pl-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6")
    filho.appendChild(new_date_input)


    number_of_dates++


}
