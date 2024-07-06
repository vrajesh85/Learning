"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TodoCollection = void 0;
var TodoItem_1 = require("./TodoItem");
var TodoCollection = /** @class */ (function () {
    function TodoCollection(userName, todos) {
        if (todos === void 0) { todos = []; }
        var _this = this;
        this.userName = userName;
        this.todos = todos;
        this.nextId = 1;
        this.itemMap = new Map();
        this.todos.forEach(function (item) { return _this.itemMap.set(item.id, item); });
    }
    TodoCollection.prototype.getToDo = function (id) {
        return this.todos.find(function (item) { return item.id === id; });
    };
    TodoCollection.prototype.getTodoItems = function (includeBoolean) {
        return this.todos.filter(function (item) { return item.isChecked == includeBoolean; });
    };
    TodoCollection.prototype.addTodoItems = function (task) {
        while (this.getToDo(this.nextId)) {
            this.nextId++;
        }
        this.itemMap.set(this.nextId, new TodoItem_1.TodoItem(this.nextId, task));
        return this.nextId;
    };
    return TodoCollection;
}());
exports.TodoCollection = TodoCollection;
