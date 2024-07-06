import { Component } from "react";

class TodoComponent extends Component {
    constructor(props){
        super(props);

        this.state = {
            item : '',
            todoList : []
        };

    this.handleOnSubmit = this.handleOnSubmit.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
    }

    handleOnSubmit(e){
        e.preventDefault();
        const list = [this.state.todoList , this.state.item];

        this.setState({
            todoList : list
        });
    }

    handleOnChange(e){
        this.setState({
            item : e.target.value
        });
    }

    render(){
        const currentTodos =  this.state.todoList.map(
            (todo,index) => <p key={index}>{todo}</p>
        );

        return(
            <form onSubmit={this.handleOnSubmit}>
                <input type="text" id="todoItem" value={this.state.item} onChange = {this.handleOnChange} />
                <button type="submit">Add</button>

                {currentTodos}
            </form>
        );
    }
}

export default TodoComponent;