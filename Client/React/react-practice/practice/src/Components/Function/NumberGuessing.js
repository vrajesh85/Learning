import { useState } from 'react';

const NumberGuessing = () => {

    const[number, setNumber] = useState(0);
    const[score, setScore] = useState(0);
   
    const checkScore = () => {
        let randomNumber = Math.floor(Math.random() * 10) + 1;
        if (number === randomNumber)
            setScore(score + 1);
    }
    
    return(
        <>
          Enter some number 
          <input value={number} type="number" onChange={(e) => setNumber(e.target.value)} />
          <br />
          <button onClick={checkScore} >Submit</button>
          Your score is {score}
        </>
    );
};

export default NumberGuessing;