import { useState } from 'react';

const ButtonContainer = () => {
    const[count, setCount] = useState(0);

    return(
        <>
            <Button count={count} setCount = {setCount} />
            The count is {count}
        </>
    );
};

const Button = (props) => {
    return (
        <>
              <button onClick={ () => props.setCount((prevScore) => props.count + prevScore + 1) }>Add</button>
        </>
    );
};

export default ButtonContainer;