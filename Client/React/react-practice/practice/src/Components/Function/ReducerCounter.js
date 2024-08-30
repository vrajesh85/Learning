import { useReducer } from "react";

const initialState = { counter : 0 };

const reducer = (state, action) => {
    switch(action.type){
        case 'increment':
            return { counter : state.counter + 1 };
        case 'decrement':
            return { counter : state.counter - 1 };
        default :
            throw new Error("Not Available");
    }
};


const ReducerCounter = () => {  
    const[state , dispatch] = useReducer(reducer , initialState);

    return (
        <>    
            Count is {state.counter} <br />
            <button onClick={ () => dispatch({type : 'increment'})}>Add +</button> <br />
            <button onClick={ () => dispatch({type : 'decrement'})}>Substract -</button>
        </>
    );
};

export default ReducerCounter;