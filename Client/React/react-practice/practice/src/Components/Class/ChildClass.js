import { Component } from "react";

class ChildClass extends Component {
    static defaultProps = {
        age: 40
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                The value sent from parent is {this.props.name} and this is coming from {this.props.age}
            </>
        );
    }
}

export default ChildClass;
