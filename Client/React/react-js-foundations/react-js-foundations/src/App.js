import React from 'react';
import './App.css';
import HelloWorld  from './Components/Functions/HelloWorld';
import Child from './Components/Functions/Child';
import Counter from './Components/Class/Counter';
import TodoComponent from './Components/Class/TodoClass';
import CounterFunc  from './Components/Functions/CounterFunc';
import Countries from './Components/Functions/Countries';

function App() {
  const [personName , setPersonName] = React.useState('');
  let header3 = <h3> Header 3</h3>;
  let header4 = <h4> Header 4</h4>;
  let flag = true;
  return (
    <div className="App">           
      { flag ? header4 : header3}

      {flag && header3}

      { 20+20 }
      <h1> Hello {personName} </h1>
      <input type="text" onChange={ (e) => setPersonName(e.target.value) } />
      
      {(() => <h2> header 2 </h2>)()}

      <HelloWorld />

      <Child name="Rajesh Vemulakonda"
              age="39" 
              companies={["Wipro","Deloitte","UHG"]} />

      <Counter></Counter>

      <TodoComponent></TodoComponent>

      <CounterFunc></CounterFunc>

      <Countries>
        <ul>
          <li>
            India
          </li>
          <li>
            UK
          </li>
          <li>
            USA
          </li>
        </ul>
      </Countries>

    </div>
  );
}

export default App;
