import React, { Component } from "react";

class RefExample extends Component {
    constructor(props) {
        super(props);

        this.textView = React.createRef();
    }

    componentDidMount() {
        this.textView.current.focus();
        this.textView.current.style = "color:red";
    }

    render() {
        return (
            <>
                <textarea ref={this.textView} />
            </>
        );
    }
}

export default RefExample;