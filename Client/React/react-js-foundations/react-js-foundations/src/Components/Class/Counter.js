import { Component} from "react";

class Counter extends Component {
    constructor(props){
        super(props);

        this.state = {
            count : 0            
        }; 
    
    this.incrementCount = this.incrementCount.bind(this);
    }

    incrementCount(){
        this.setState({
            count : this.state.count + 1
        });
        console.log(`the count is ${this.state.count}`);
    }

    render(){
        return(
            <>
                <p>
                    The current state count is {this.state.count}
                </p>
                <button type="button" onClick={ () => this.incrementCount() }>Add 1</button>
            </>
        );
    }
}

export default Counter;