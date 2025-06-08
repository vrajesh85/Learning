import CounterClass from './Components/Class/Counter';
import CounterFunc from './Components/Function/CounterFunc';
import ParentClass from './Components/Class/ParentClass';
import ParentFunction from './Components/Function/ParentFunction';
import './App.css';
import { useState } from 'react';
import PropsMutator from './Components/Function/PropsMutator';
import NewsFeed from './Components/Function/NewsFeedFunction';
import MultipleCounters from './Components/Class/MultipleCounters';
import MultipleCountersFunc from './Components/Function/MultipleCountersFunc';
import RefExampleParent from './Components/Class/RefExampleParent';
import NumberGuessing from './Components/Function/NumberGuessing';
import ButtonContainer , {Button} from './Components/Function/ButtonContainer';
import RenderCounter from './Components/Function/RenderCounter';
import TimerFunc from './Components/Function/TimerFunc';
import ReducerCounter from './Components/Function/ReducerCounter';
import CallMe from './Components/Function/UnnecessaryRenders';
import NewsToday from './Components/Class/NewsToday';
import NewsTodayFunc from './Components/Function/NewsTodayFunc';
import RestResponse from './Components/Function/RestResponse';

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
      <p>This is coming from news feed function component</p>
      <NewsFeed></NewsFeed>
      <p>This is from multiple counters class</p>
      <MultipleCounters></MultipleCounters>
      <p>This is from multiple counters function</p>
      <MultipleCountersFunc></MultipleCountersFunc>
      <p>This is RefExample from class</p>
      <RefExampleParent />
      <p>This is NumberGuessing from function</p>
      <NumberGuessing></NumberGuessing>  
      <p>This is button container</p> 
      <ButtonContainer />
      <h3>Render Counter Func</h3>
      <RenderCounter />
      <h3>Timer Func</h3>
      {/* <TimerFunc /> */}
      <h3>ReducerCounter</h3>
      <ReducerCounter />
      <h3> Call me Function</h3>
      <CallMe />
      <h3> News Today </h3>
      <NewsToday />
      <h3>News today func</h3>
      <NewsTodayFunc />
      <h3>Rest Response</h3>
      <RestResponse />
    </div>
  );
}

export default App;
