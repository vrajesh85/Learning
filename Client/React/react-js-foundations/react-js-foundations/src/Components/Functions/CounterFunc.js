import {useState} from "react";

    const CounterFunc = () => {

    const [count , setCount] = useState(0);

    const handleClick = () => setCount(count+1);    
    
    return(
        <button onClick={handleClick}>
            You pressed {count} times
        </button>
    );
}

export default CounterFunc;