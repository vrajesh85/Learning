import { useState, useEffect } from "react";

const CounterFunc = () => {

    const [count, setCount] = useState(0);

    const handleClick = () => setCount(count + 1);

    return (
        <>
            <p>
                The count is {count}
            </p>
            <button type="button" onClick={handleClick}>Add 1</button>
        </>
    );

};

export default CounterFunc;