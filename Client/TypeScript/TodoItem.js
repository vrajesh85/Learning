"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TodoItem = void 0;
var TodoItem = /** @class */ (function () {
    // No need for these variables
    // private id:number;
    // private task:string;
    // private isChecked:boolean;
    function TodoItem(id, task, isChecked) {
        if (isChecked === void 0) { isChecked = false; }
        this.id = id;
        this.task = task;
        this.isChecked = isChecked;
    }
    TodoItem.prototype.printDetails = function () {
        console.log("".concat(this.id, " --> ").concat(this.task, " ").concat(this.isChecked ? "checked" : ""));
    };
    return TodoItem;
}());
exports.TodoItem = TodoItem;
