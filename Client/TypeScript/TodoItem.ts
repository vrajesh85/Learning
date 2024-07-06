export class TodoItem {
    // No need for these variables
    // private id:number;
    // private task:string;
    // private isChecked:boolean;

    constructor(public id:number , public task:string, public isChecked:boolean=false){ }

    printDetails():void {
        console.log(`${this.id} --> ${this.task} ${this.isChecked ? "checked" : ""}`);
    }
}