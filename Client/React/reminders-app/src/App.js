import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

import InputForm from '../src/Components/Functions/InputForm';
import FilterTasks from './Components/Functions/FilterTasks';
import RemindersList from './Components/Functions/RemindersList';

function App() {

  const [reminder, setReminder] = useState();
  const [userInput , setUserInput] = useState();
  const [selectedFilter, setSelectedFilter] = useState('all'); 

  const addReminder = (itemToAdd) => {
    if(reminder === undefined){
      setReminder([itemToAdd]);
    }
    else {
      setReminder([...reminder, itemToAdd]);
    }     
  };

 const filteredList = filterList(reminder, selectedFilter);

 function filterList (reminders, selectedFilter) {
  if(selectedFilter == "all"){
    return reminders;
  }
  else {
    let numberOfDays;
    switch(selectedFilter){
       case "2day":
           numberOfDays = 2;
      break;
      case "1week":
            numberOfDays = 7;
      break;
      case "30days":
            numberOfDays = 30;
      break;
      default :
            numberOfDays = 0;
      break;
    }

    const result = reminder.filter(remind=>{

        const todaysDate = new Date().toISOString().substring(0,10);
        
        const todayTime = new Date(todaysDate).getTime();
        
        const dueTime = new Date(remind.dueDate).getTime();
        
        return dueTime < (todayTime + (numberOfDays * 86400000));  
      });
    
      return result;
  }
 }

 function setComplete (isComplete, index) {
  const newReminders = [...reminder.slice(0, index) , {...reminder , isComplete} , ...reminder.slice(index+1)];

  setReminder(newReminders);
 }

  return (
    <div style={{ textAlign:"center" }}>
        <h1> Reminder Tasks (Function Components)</h1>
        <InputForm userInput={userInput} setUserInput={setUserInput} addReminder={addReminder} ></InputForm>
        <FilterTasks selectedFilter={selectedFilter} setSelectedFilter={setSelectedFilter}></FilterTasks>
        <RemindersList reminders={filteredList} setComplete={setComplete}></RemindersList>
    </div>
  );
}

export default App;
