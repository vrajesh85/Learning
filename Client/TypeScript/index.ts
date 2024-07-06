
import { TodoItem } from './TodoItem.js'
import { TodoCollection } from './TodoCollection.js';
 

let todoAP = new TodoItem(1 , "AP" , true);
let todoTG = new TodoItem(2 , "TG" , false);
let todoTN = new TodoItem(3 , "TN" , false);

let todoArrays : TodoItem[] = [todoAP,todoTG,todoTN];


let collection = new TodoCollection("Rajesh", todoArrays);

console.clear();
console.log(`${collection.userName}'s collection : `);

let newId = collection.addTodoItems("KL");
let todoItem  = collection.getToDo(newId) as TodoItem;

for(let index : number = 0; index < 3 ; index ++){
  collection.todos[index].printDetails();
}

console.log(`The value with true are :`);
collection.getTodoItems(true).forEach(item => item.printDetails());
