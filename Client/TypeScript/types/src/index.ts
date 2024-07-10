


let numericValue : unknown;
console.log(`Type of numericValue is ${typeof(numericValue)}`);
numericValue = "Rajesh";
console.log(`Type of numericValue is ${typeof(numericValue)}`);
numericValue = 20;
console.log(`Type of numericValue is ${typeof(numericValue)}`);

function check(expres : any) : asserts expres is boolean {
    if(!expres) 
        throw new Error("check failed !");
}

function multiply (amount : number) : number {
    check(amount)
   return amount * 2;
}

function writeAmount(amount : number, product : string) : void {
    console.log(`price of ${product} is ${amount}`);
}

let names : string[] = ["Hat","Gloves","Umbrella"];
let prices = [10,20,30];

prices.forEach((price, index) => {
    writeAmount(multiply(price),names[index]);
});

let price : any = multiply(10); 
let halfPrice = price / 2;

console.log(`${10} into 2 is = ${multiply(10)}`);
console.log(`price and half price are ${price} and ${halfPrice}`);

console.log('with tuples');

let hats : [string , number] = ['Hat', 100];
let Gloves : [string , number] = ["Gloves" , 200];
writeAmount(hats[1], hats[0]);

let [hatname , hatPrice] = hats;
writeAmount(hatPrice,hatname);

let products : [string , number][] = [["Hats", 100],["Gloves",200]]; 
let tupleUnions : ([string , number] | boolean)[] = [true, false, hats, ...products]; // means all products elements are added here

enum Product { "AP" = 1, "TG" = 2, "TN" = 3};
[Product.AP, Product.TG,Product.TN].forEach(( (val) => console.log(`states names are : ${val}`)));

class Person {
    constructor(public id : string, public name : string , public city :string){}
}
 
class Employee extends Person {
    constructor(public id:string,public name:string, public city:string,private dept:string){
        super(id,name,city);
        this.dept = dept;
    }
}

class Customer extends Person {
    constructor(public id:string,public name:string, public city:string, private credit : number){
        super(id,name,city);
        this.credit = credit;
    }
}

class Supplier extends Person {
    constructor(public id:string,public name:string, public city:string,public companyName : string){
        super(id,name,city);
        this.companyName = companyName;
    }
}

let data : Person[] = [ new Employee("1","Rajesh","VSKP","IT"), new Employee("2","Raj","Hyd","IT")];

data.push(new Supplier("3","Sup","Che","XYZ"));

data.forEach(item => {
    console.log(`details are ${item.city}  ,${item.id}`);
});

abstract class Animal {
    constructor(public name:string,public isNoNVeg : boolean){ }
    
    abstract getDetails() : string;

    getSpecificDetails() : string {
        return `animal name is ${this.name} and details are : ${this.getDetails()}`;
    }
}

class Tiger extends Animal {
    constructor(public name, public isNonVeg : boolean, public canClimbTree : boolean){
        super(name,isNonVeg)
        this.canClimbTree = canClimbTree;
    }

     public getDetails(): string {
        return ` can tiger climb a tree ? ${this.canClimbTree}`;
    }
}

class Leopard extends Animal {
    constructor(public name, public isNonVeg : boolean, public canClimbTree : boolean, public canRunFast : boolean){
        super(name,isNonVeg);
        this.canClimbTree = canClimbTree;
        this.canRunFast = canRunFast;
    }

    public getDetails() : string {
        return ` can Leopard climb a tree ? ${this.canClimbTree} and can leopard run faster ${this.canRunFast}`;
    }
}

let animalData : Animal[] = [ new Tiger("TIGER", true, false) , new Leopard("LEOPARD", true, true, true)];

animalData.forEach(item => {
   console.log(item.getSpecificDetails());
});

type ageType = { age : number };

class MiddleAge<T>{
    private items : Set<T>;
    constructor(initialItems : T[] = []){
        this.items = new Set<T>(initialItems);
    }

    addItems(...newItems : T[]){
        newItems.forEach(item => this.items.add(item));
    }

    getItems(name : T) : T{
        return[...this.items.values()].find(item => item);
    }

    getCount() : number {
        return[...this.items.values()].length;
    }
}

let shape : ageType = { age : 39};
let normalPerson : MiddleAge<Person> = new MiddleAge<Person>(data);
normalPerson.addItems(new Employee("3","Raj","VSKP","IT"));