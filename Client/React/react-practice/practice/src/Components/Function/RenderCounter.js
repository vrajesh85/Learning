import { useState, useEffect } from 'react';

const RenderCounter = () => {
    const[count, setCount] = useState(0);    
    
    useEffect(() => console.log(`count is ${count}`));

    return (
        <>
            <pre>This component will render every time we call input    </pre>
            <button onClick={() => setCount(count + 1)}>Count is {count}</button>
        </>
    );
};

export default RenderCounter;