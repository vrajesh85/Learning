import React, { Component, createRef } from 'react';
import RefExampleChild from './RefExampleChild';

class RefExampleParent extends Component {
    constructor(props) {
        super(props);

        this.childRef = createRef();
    }

    handleClick = () => {
        if (this.childRef.current) {
            this.childRef.current.someMethod();
        }
    };

    render() {
        return (
            <>
                <RefExampleChild ref={this.childRef}></RefExampleChild>
                <button onClick={this.handleClick}>Call Child Method</button>
            </>
        );
    }
}

export default RefExampleParent;