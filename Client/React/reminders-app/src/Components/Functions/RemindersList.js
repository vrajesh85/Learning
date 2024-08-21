import {PropTypes} from 'prop-types';
import Reminders from "./Reminders";


const RemindersList = (props) => {

    const listReminders = props.reminders.map((reminder , index) => {
        return(
            <Reminders reminderText={reminder.reminderText} dueDate={reminder.dueDate} isComplete={reminder.isComplete} setComplete={props.setComplete}
            id={index} key={index} />);
    }); 
    return(
        <div>
            {listReminders}
        </div>
    );
};


RemindersList.propTypes = {
    reminders : PropTypes.array
}

const date = new Date();
const formattedDate = date.toISOString().substring(0,10);

RemindersList.defaultProps = {
    reminders : [{
        reminderText : "NA",
        dueDate : formattedDate,
        isComplete : false
    }]
};

export default RemindersList;