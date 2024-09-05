import { useCallback, useEffect, useRef, useState } from 'react';

function CallMe(props){
    const[phoneNumber , setPhoneNumber] = useState();
    const[currentNumber , setCurrentNumber] = useState();

    const phoneNumberRef = useRef();

    const handleClick = (e) => {
        setPhoneNumber(phoneNumber);
    };

    const placeCall = useCallback(() => {
        if (phoneNumber){
            console.log(`dailing ${phoneNumber}`);
        }
    },[phoneNumber]);

    useEffect(() => {
        placeCall(phoneNumber);
    }, [phoneNumber , placeCall]);

    return(
    <>
        <label>Enter the number to call:</label>
        <input type="phone" ref={phoneNumberRef} onChange={ () => {setCurrentNumber(phoneNumberRef.current.value)}  } />
        <button onClick={handleClick}>
            Place Call
        </button>
        <h1>{currentNumber}</h1>
    </>
    );
}

export default CallMe;