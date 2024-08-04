import { Component } from "react";

class NewsFeed extends Component {
    constructor(props){
        super(props);

        this.state = {
            headlines : [],
            date : new Date()
        }

        this.updateState = this.updateState.bind(this);        
    }
   
    render(){
        return(
            <>
            <h1> The date is {this.state.date} </h1>
            </>
        );
    }
}

