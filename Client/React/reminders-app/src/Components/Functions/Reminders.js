import { PropTypes } from "prop-types";

const Reminders = (props) => {

    const handleChange = (e) => {
        props.setComplete(!props.isComplete , props.id);
    };

    return(
        <div>
            item : {props.reminderText}
            due Date : {props.dueDate}
            Completed ? : {String(props.isComplete)}
            <input type="checkbox" checked={props.isComplete} onChange={handleChange} />
        </div>
    );
};


Reminders.propTypes = {
    reminderText : PropTypes.string,
    dueDate : PropTypes.string,
    isComplete : PropTypes.bool
};

const date = new Date();
const formattedDate = date.toISOString().substring(0,10);

Reminders.defaultProps = {
    reminderText : "No Reminder Set",
    dueDate : formattedDate,
    isComplete : false
};

export default Reminders;