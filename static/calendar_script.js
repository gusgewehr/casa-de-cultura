
const MONTH_NAMES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
const DAYS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'];

const all_logged_dates = JSON.parse(document.getElementById('all_logged_dates').textContent);		

const all_dates_json = $.parseJSON("{ \"all_dates\": " + all_logged_dates + "}")



function create_registered_events_dates(){
    events = []


    all_dates_json["all_dates"].forEach(element => {
        var teste = element['fields']

        this.events.push({
                event_date: teste['start_date'],
                event_title: teste['evento']['nome'],
                event_theme: 'blue'
            });



    
    });

    return events
}



function app() {

    teste = create_registered_events_dates()
    
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

        openEventModal: false,

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



        addEvent() {

            if (this.event_title == '') {
                return;
            }

            dateParts = this.event_date.split("/")
            eventDate = new Date(dateParts[2], dateParts[1]-1, dateParts[0])

            this.events.push({
                event_date: eventDate,
                event_title: this.event_title,
                event_theme: this.event_theme
            });

            add_date(this.event_date, this.start_time, this.end_time, this.date_type)

            // clear the form data
            this.event_date = '';

            //close the modal
            this.openEventModal = false;
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
