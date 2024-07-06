import { Component } from "react";

class UnmountExample extends Component{
    constructor(props){
        super(props);
        
        this.state = {
            seconds : 0
        }       
    }

    componentDidMount(){
        this.interval = setInterval(() => this.tick(), 1000);
    }

    tick(){
        this.setState({
            seconds : this.state.seconds + 1
        })
    }
    
    componentWillUnmount(){
        clearInterval(this.interval);        
    }

    render(){
        return(
            <div>
                The interval with class component is {this.state.seconds}
            </div>
        );
    }
}

export default UnmountExample;