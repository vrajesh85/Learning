import { TodoItem }  from './TodoItem';

export class TodoCollection {
    private nextId : number = 1;
    private itemMap = new Map<number , TodoItem>();

    constructor(public userName : string, 
                public todos : TodoItem[] = []) { 
                   this.todos.forEach(item => this.itemMap.set(item.id , item));
                }

    getToDo(id : number) : TodoItem  | undefined {
        return this.todos.find(item => item.id === id);
    }

    getTodoItems(includeBoolean : boolean) : TodoItem[] {
        return this.todos.filter(item => item.isChecked == includeBoolean);
    }

    addTodoItems(task : string) : number{
        while(this.getToDo(this.nextId)) {
            this.nextId++;
        }        
        this.itemMap.set(this.nextId , new TodoItem(this.nextId , task));
        return this.nextId;
    }
}

