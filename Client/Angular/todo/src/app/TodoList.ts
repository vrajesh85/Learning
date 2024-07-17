import { TodoItem } from "./TodoItem";

export class TodoList {
    constructor(public user : string , public todoItems : TodoItem[]){ }

    get items() : readonly TodoItem[] {
        return this.todoItems;
    }

    addItem(task : string){
        this.todoItems.push(new TodoItem(task));
    }
}