import CounterClass from './Components/Class/Counter';
import CounterFunc from './Components/Function/CounterFunc';
import ParentClass from './Components/Class/ParentClass';
import ParentFunction from './Components/Function/ParentFunction';
import './App.css';
import { useState } from 'react';
import PropsMutator from './Components/Function/PropsMutator';

function App() {

  const [theNumber, setTheNumber] = useState(0);

  return (
    <div className="App">
      <p> This is from Counter class Component </p>
      <CounterClass></CounterClass>
      <p>This is from Counter func component</p>
      <CounterFunc></CounterFunc>
      <p>This is coming from Parent class</p>
      <ParentClass></ParentClass>
      <p>This is coming from Parent function</p>
      <ParentFunction></ParentFunction>
      <p>This is coming from Props Mutator</p>
      <PropsMutator theNumber={theNumber} setTheNumber={setTheNumber} />
    </div>
  );
}

export default App;
