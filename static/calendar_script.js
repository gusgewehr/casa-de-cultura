
const MONTH_NAMES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
const DAYS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'];

const all_logged_dates = JSON.parse(document.getElementById('all_logged_dates').textContent);		

const all_dates_json = $.parseJSON("{ \"all_dates\": " + all_logged_dates + "}")




function create_registered_events_dates(){
    events = []

    var dict = {
        "AP": "purple",
        "EN": "green",
        "MNT": "yellow",
        "DMNT": "yellow",
        "aprovado": "red",
    }


    all_dates_json["all_dates"].forEach(element => {
        var date = element['fields']

        if(date["evento"]["aprovado"] =="True" && date['uso'] == "AP"){
            cor = "aprovado"
        }
        else{
            cor = date["uso"]
        }
        

        start_date = new Date(date["start_date"])
        this.events.push({
                id: -1,
                event_date: date['start_date'],
                event_title: start_date.getHours()+":"+start_date.getMinutes()+" "+date['evento']['nome'],
                event_theme: dict[cor]
            });



    
    });

    return events
}

function get_registered_dates_for_editd_event(){
    var added_dates = []

    try{
        const event_dates = JSON.parse(document.getElementById('event_dates').textContent);		

        const event_dates_json = $.parseJSON("{ \"event_dates\": " + event_dates + "}")

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


            added_dates.push( {
                    date: day+"/"+month+"/"+start_date.getFullYear(), 
                    start_time: start_hour+":"+start_min, 
                    end_time: end_hour+":"+end_min, 
                    type: date["uso"]
                }
            )
        })

        return added_dates
    }
    catch{
        return added_dates
    }
}

function app() {

    teste = create_registered_events_dates()

    event_edit_added_dates = get_registered_dates_for_editd_event()

           
    return {
        month: '',
        year: '',
        no_of_days: [],
        blankdays: [],
        days: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
        events: teste,
        event_date_id: '',
        event_title: 'Seu evento',
        start_time: '',
        event_date: '',
        end_time: '',
        date_type: 'AP',
        event_theme: 'blue',
        number_of_dates: 0,
        added_dates: event_edit_added_dates,
        openEventModal: false,
        tried: false,

        getCurrentDateId(date){
            return date.id
        },

        generateElementName(element_type, date){

            // type_input.setAttribute("name", "type_"+number_of_dates)
            // end_time_input.setAttribute("name", "end_time_"+number_of_dates)
            // start_time_input.setAttribute("name", "start_time_"+number_of_dates)
            // new_date_input.setAttribute("name", "date_"+number_of_dates)
            
            var cur_pos = this.added_dates.indexOf(date)

            return element_type+cur_pos
        },


        initDate() {
            let today = new Date();
            this.month = today.getMonth();
            this.year = today.getFullYear();
            this.datepickerValue = new Date(this.year, this.month, today.getDate()).toDateString();
        },

        isToday(date) {
            const today = new Date();
            const d = new Date(this.year, this.month, date);

            return today.toDateString() === d.toDateString() ? true : false;
        },

        showEventModal(date) {
            // open the modal
            this.openEventModal = true;
            this.event_date = new Date(this.year, this.month, date).toLocaleDateString("pt-BR");
        },

        getShowingMonth() {
            
                var today = new Date()
                today = new Date(today.setMonth(0, 1))
                var newDate = new Date(today.setMonth(today.getMonth()+this.month))

                var i = newDate.getMonth()			

                return MONTH_NAMES[i];
        },
        getShowingYear() {
            
            var today = new Date()
            today = new Date(today.setMonth(0, 1))
            var newDate = new Date(today.setMonth(today.getMonth()+this.month))

            return newDate.getFullYear();
        },

        blockPastDates(){
            
            var date = new Date()
            var yearStart = new Date(date.setMonth(0, 1))
            var newDate = new Date(yearStart.setMonth(yearStart.getMonth()+this.month))

            var is_past = false

            var today = new Date()					

            if(newDate.getMonth() <= today.getMonth() && newDate.getFullYear() <= today.getFullYear()){
                is_past = true
            }


            return is_past;
        },

        rmDate(date){

            this.added_dates.pop(date)

            for(var event of this.events){
                if(event.id == date.id){
                    this.events.pop(event)
                }
            }

            this.number_of_dates--

        },

        checkTimeDelta(){

            var dateParts = this.event_date.split("/")
            var eventDate = new Date(dateParts[2], dateParts[1]-1, dateParts[0])

            var start_time_split = this.start_time.split(":")
            var end_time_split = this.end_time.split(":")
            
            var start_datetime = eventDate.setHours(start_time_split[0])
            var start_datetime = eventDate.setMinutes(start_time_split[1])

            var end_datetime = eventDate.setHours(end_time_split[0])
            var end_datetime = eventDate.setMinutes(end_time_split[1])

            if(end_datetime - start_datetime <= 0){
                return true
            }
            else{
                return false
            }


        },

        addEvent() {           
            
            this.tried = true

            var checkTimeDelta = this.checkTimeDelta()
            
            if(this.start_time == "" | this.end_time == ""){
                return
            }

            else if(checkTimeDelta){
                return
            }

            dateParts = this.event_date.split("/")
            eventDate = new Date(dateParts[2], dateParts[1]-1, dateParts[0])
        
            this.added_dates.push({
                id: this.number_of_dates,
                date: this.event_date,
                start_time: this.start_time,
                end_time: this.end_time,
                type: this.date_type
            }) 

            this.events.push({
                id: this.number_of_dates,
                event_date: eventDate,
                event_title: this.event_title,
                event_theme: this.event_theme
            });

                  
            // clear the form data
            this.event_date = '';
            this.start_time = '';
            this.end_time = '';

            //close the modal
            this.openEventModal = false;
            
            this.tried = false;
            this.number_of_dates++
        },

        
        getNoOfDays() {
            
            let daysInMonth = new Date(this.year, this.month + 1, 0).getDate();

            // find where to start calendar day of week
            let dayOfWeek = new Date(this.year, this.month).getDay();
            let blankdaysArray = [];
            for ( var i=1; i <= dayOfWeek; i++) {
                blankdaysArray.push(i);
            }

            let daysArray = [];
            for ( var i=1; i <= daysInMonth; i++) {
                daysArray.push(i);
            }

            
            
            this.blankdays = blankdaysArray;
            this.no_of_days = daysArray;
        }
    }
}
