import { Component } from '@angular/core';
import { TodoItem } from './TodoItem';
import { TodoList } from './TodoList';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
   private list = new TodoList("Rajesh",[
    new TodoItem("Study Angular",false),
    new TodoItem("Study React",false),
    new TodoItem("Study C#",true),
    new TodoItem("Study Dotnet",true)
   ]);

   get userName() : string {
    return this.list.user;
   }

   get itemCount() : number {
     return this.list.items.filter(item => item.isComplete).length;
   }
}
