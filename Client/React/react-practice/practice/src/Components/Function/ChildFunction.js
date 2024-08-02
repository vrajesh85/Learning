const ChildFunction = props => {
    return (
        <>
            The value returned from Parent is {props.name} and this value is coming from default props {props.age}
        </>
    )
};

ChildFunction.defaultProps = {
    age: 39
}

export default ChildFunction;