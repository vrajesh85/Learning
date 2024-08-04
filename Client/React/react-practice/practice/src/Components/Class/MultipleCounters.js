import { Component } from 'react';

class MultipleCounters extends Component {
    constructor(props){
        super(props);

        this.state = {
            count1 : 0,
            count2 : 0
        }

        this.testCount = 0;

        this.incrementButton1 = this.incrementButton1.bind(this);
        this.incrementButton2 = this.incrementButton2.bind(this);
    }

    incrementButton1 = () => {
        // this.setState({
        //     count1 : this.state.count1 + 1
        // })
        
        this.setState((current) => {
           return { count1 : current.count1 + 1 };
        });

        this.testCount++;

        console.log(`the value of test count is ${this.testCount}`);
        console.log(`the value of count1 is ${this.state.count1}`);
    }   

    updater(){
       return () => {  return this.state.count1 + 1; }
    }

    incrementButton2 = () => {
        this.setState({
            count2 : this.state.count2 + 1
        })
    }

    render(){
        return(
            <>
            <button onClick={this.incrementButton1}>Button 1 {this.state.count1}</button>
            <br />
            <button onClick={this.incrementButton2}>Button 2 {this.state.count2}</button>
            </>
        );
    }
}

export default MultipleCounters;