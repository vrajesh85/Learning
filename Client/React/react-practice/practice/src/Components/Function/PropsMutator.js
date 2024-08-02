const PropsMutator = props => {
    let myNumber = props.theNumber;

    const myPropsChange = () => {
        myNumber = myNumber + 1;
        console.log(`the value of my number is :` + myNumber);
    }

    return (
        <>
            <div>
                <p>
                    The number is my number : {myNumber}
                </p>
                <p>
                    The value of props the number is : {props.theNumber}
                </p>
                <button onClick={myPropsChange}>change my Number</button>
                <button onClick={() => { props.setTheNumber(props.theNumber + 1) }}>change the number</button>
            </div>
        </>
    );
}

export default PropsMutator;