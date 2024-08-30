import { Component } from 'react';

class CounterClass extends Component {
    constructor(props) {
        super(props);
        this.state = {
            count: 0
        };
        console.log('from counter class');
        this.incrementCount = this.incrementCount.bind(this);
    }

    incrementCount() {        
        this.setState({
            count: this.state.count + 1
        })
    }

    render() {
        return (
            <>
                <p> The count is {this.state.count}</p>
                <button type="button" onClick={() => this.incrementCount()}>Add Count</button>
            </>
        )
    }
}

export default CounterClass;
