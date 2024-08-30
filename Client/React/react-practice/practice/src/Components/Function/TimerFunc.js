import { useEffect, useState } from "react";

function TimerFunc() {

   const[count, setCount] = useState(0);
   const[gameChanger, setGameChanger] = useState(0);
    
   useEffect(() => {
    let time = 0;
    const interval = setInterval(() => { 
        console.log(`time is ${time}`);  
        time++ ;          
        }, 1000);
    
    return () => clearInterval(interval);
    },[gameChanger]);

    useEffect(() => {

    },[]);

    return(
        <> 
            <p>Check the timer in console</p> and game changer is {gameChanger}
            <button onClick={ () => setCount(count + 1)}>Click Me</button>
            <button onClick={ () => setGameChanger(gameChanger + 1) }>Game Changer</button>
        </>
    )
}

export default TimerFunc;