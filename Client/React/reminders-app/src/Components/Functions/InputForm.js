import { PropTypes } from 'prop-types';

const InputForm = (props) => {

    const handleOnTextChange = (e) => {
        const newUserInput = {...props.userInput , reminderText : e.target.value};

        props.setUserInput(newUserInput);
    };

    const handleOnDateChange = (e) => {
        const date = new Date(e.target.value);
        const formattedDate = date.toISOString().substring(0,10);
        const newUserInputDate = { ...props.userInput , dueDate : formattedDate };

        props.setUserInput(newUserInputDate);
    };

    const handleClick = (e) => {

        e.preventDefault();
        const itemToAdd = {...props.userInput , isComplete: false};
        props.addReminder(itemToAdd);
    }
 
    return(      
           <form>
                Enter task : <input type="text" id="reminderText" value={props.userInput.reminderText} 
                                placeholder="what do you want to do ?" onChange={handleOnTextChange} />
                Date : <input type="date" value={props.userInput.dueDate} onChange={handleOnDateChange} id="dueDate" />
                &nbsp;&nbsp;&nbsp;
                <button onClick={handleClick}>Add Task</button>
           </form>        
    );
};

InputForm.propTypes = {
    userInput : PropTypes.shape({
        reminderText : PropTypes.string,
        dueDate : PropTypes.string
    }),
    setUserInput : PropTypes.func,
    addReminder : PropTypes.func
}

const date = new Date();
const formattedDate = date.toISOString().substr(0,10);

InputForm.defaultProps = {
    userInput : {
        reminderText : "",
        dueDate : formattedDate
    }    
}

export default InputForm;