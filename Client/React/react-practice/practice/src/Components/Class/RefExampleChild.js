import { Component, forwardRef, ref } from "react";

class RefExampleChild extends Component {
    constructor(props) {
        super(props);
    }

    someMethod() {
        alert('Method in child class component called');
    }

    render() {
        return (
            <>
                Enter into child component -- <input type="text" />
            </>
        );
    }
}

export default RefExampleChild;