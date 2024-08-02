import { Component } from "react";
import ChildClass from "./ChildClass";

class ParentClass extends Component {
    constructor(props) {
        super(props);

        this.state = {
            somevalue: "Rajesh"
        };

        this.changeValue = this.changeValue.bind(this);
    }

    changeValue(valueSent) {
        this.setState({
            somevalue: valueSent == "" ? "Rajesh" : valueSent
        })
    }

    render() {
        return (
            <>
                <div>
                    Enter some value :  <input type="text" placeholder="somevalue" onChange={(e) => this.changeValue(e.target.value)} ></input>
                    <ChildClass name={this.state.somevalue}></ChildClass>
                </div>
            </>
        );
    }
}

export default ParentClass;