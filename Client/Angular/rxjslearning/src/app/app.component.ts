import { Component, ElementRef, ViewChild } from '@angular/core';
import { Observable, of, from, fromEvent, interval, take } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'rxjslearning';
  agentName: string = "";
  ofOperatorValue: string = " ";
  order: string = "";
  familyDetails: string[] = ["V R Pantulu", "V Kasturi", "V Rajesh", "D Srividya", "Ashritha", "Ananya"];
  address: string = "";
  houseObject = {
    "area": "Prahladapuram",
    "city": "Vizag"
  }
  familyNames$: Observable<string[]>;
  houseAddress$: Observable<any>;
  agents$: Observable<string>;
  orders$: Observable<string> = from(['Kitchen', 'Electronics', 'HouseHold']);
  newOrders$ = this.orders$;
  @ViewChild('validate')
  validate: ElementRef | undefined;

  constructor() {
    this.agents$ = new Observable<string>(
      function (observer) {
        observer.next("Rajesh");
        setInterval(() => observer.next("Srividya"), 3000);
      });

    this.agents$.subscribe(data => this.agentName = data);

    this.familyNames$ = of(this.familyDetails);
    this.houseAddress$ = of(this.houseObject);

    this.familyNames$.subscribe(data => {
      this.ofOperatorValue += data;
    });

    this.houseAddress$.subscribe(data => {
      this.address = `family area is ${data.area} and city is ${data.city}`;
    });

    this.orders$.subscribe(data => {
      //this.order = data;
      setInterval(() => {
        this.order = data;
      }, 3000);
    });

    // interval operator
    this.newOrders$.subscribe((data => {
      const interval$ = interval(1000);
      // pipe operator
      const seqNum$ = interval$.pipe(take(7));
      seqNum$.subscribe((num => {
        console.log(`order is ${data} with sequence ${num}`);
      }))

    }));

  }

  // from event
  clickObservableEvent() {
    const btnObservable$ = fromEvent(this.validate?.nativeElement, 'click');
    let count: number = 1;
    btnObservable$.subscribe(data => {
      console.log(data);
      console.log(`you clicked the button ${count} times`);
      ++count;
    });
  }



}
