import { useState } from "react";

const MultipleCountersFunc = () => {

    const [count, setCount] = useState(0);
    let testCount = 0;

    const incrementCount = () => {
        setCount(count + 1);
        // setCount((prevState) => { return prevState + 1 });
        testCount++;

        console.log(`The test count is ${testCount}`);
        console.log(`The count is ${count}`);
    }

    return (
        <>
            <h3>The value of count is {count} </h3>
            <button onClick={incrementCount}>Click Me</button>
            <form>
                Enter email address : <input type="text" name="emailAddress" value="" />
            </form>
        </>
    );
}

export default MultipleCountersFunc;