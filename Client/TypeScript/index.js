"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var TodoItem_js_1 = require("./TodoItem.js");
var TodoCollection_js_1 = require("./TodoCollection.js");
var todoAP = new TodoItem_js_1.TodoItem(1, "AP", true);
var todoTG = new TodoItem_js_1.TodoItem(2, "TG", false);
var todoTN = new TodoItem_js_1.TodoItem(3, "TN", false);
var todoArrays = [todoAP, todoTG, todoTN];
var collection = new TodoCollection_js_1.TodoCollection("Rajesh", todoArrays);
console.clear();
console.log("".concat(collection.userName, "'s collection : "));
var newId = collection.addTodoItems("KL");
var todoItem = collection.getToDo(newId);
for (var index = 0; index < 3; index++) {
    collection.todos[index].printDetails();
}
console.log("The value with true are :");
collection.getTodoItems(true).forEach(function (item) { return item.printDetails(); });
