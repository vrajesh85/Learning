let numericValue;
console.log(`Type of numericValue is ${typeof (numericValue)}`);
numericValue = "Rajesh";
console.log(`Type of numericValue is ${typeof (numericValue)}`);
numericValue = 20;
console.log(`Type of numericValue is ${typeof (numericValue)}`);
function check(expres) {
    if (!expres)
        throw new Error("check failed !");
}
function multiply(amount) {
    check(amount);
    return amount * 2;
}
function writeAmount(amount, product) {
    console.log(`price of ${product} is ${amount}`);
}
let names = ["Hat", "Gloves", "Umbrella"];
let prices = [10, 20, 30];
prices.forEach((price, index) => {
    writeAmount(multiply(price), names[index]);
});
let price = multiply(10);
let halfPrice = price / 2;
console.log(`${10} into 2 is = ${multiply(10)}`);
console.log(`price and half price are ${price} and ${halfPrice}`);
console.log('with tuples');
let hats = ['Hat', 100];
let Gloves = ["Gloves", 200];
writeAmount(hats[1], hats[0]);
let [hatname, hatPrice] = hats;
writeAmount(hatPrice, hatname);
let products = [["Hats", 100], ["Gloves", 200]];
let tupleUnions = [true, false, hats, ...products]; // means all products elements are added here
var Product;
(function (Product) {
    Product[Product["AP"] = 1] = "AP";
    Product[Product["TG"] = 2] = "TG";
    Product[Product["TN"] = 3] = "TN";
})(Product || (Product = {}));
;
[Product.AP, Product.TG, Product.TN].forEach(((val) => console.log(`states names are : ${val}`)));
class Person {
    id;
    name;
    city;
    constructor(id, name, city) {
        this.id = id;
        this.name = name;
        this.city = city;
    }
}
class Employee extends Person {
    id;
    name;
    city;
    dept;
    constructor(id, name, city, dept) {
        super(id, name, city);
        this.id = id;
        this.name = name;
        this.city = city;
        this.dept = dept;
        this.dept = dept;
    }
}
class Customer extends Person {
    id;
    name;
    city;
    credit;
    constructor(id, name, city, credit) {
        super(id, name, city);
        this.id = id;
        this.name = name;
        this.city = city;
        this.credit = credit;
        this.credit = credit;
    }
}
class Supplier extends Person {
    id;
    name;
    city;
    companyName;
    constructor(id, name, city, companyName) {
        super(id, name, city);
        this.id = id;
        this.name = name;
        this.city = city;
        this.companyName = companyName;
        this.companyName = companyName;
    }
}
let data = [new Employee("1", "Rajesh", "VSKP", "IT"), new Employee("2", "Raj", "Hyd", "IT")];
data.push(new Supplier("3", "Sup", "Che", "XYZ"));
data.forEach(item => {
    console.log(`details are ${item.city}  ,${item.id}`);
});
class Animal {
    name;
    isNoNVeg;
    constructor(name, isNoNVeg) {
        this.name = name;
        this.isNoNVeg = isNoNVeg;
    }
    getSpecificDetails() {
        return `animal name is ${this.name} and details are : ${this.getDetails()}`;
    }
}
class Tiger extends Animal {
    name;
    isNonVeg;
    canClimbTree;
    constructor(name, isNonVeg, canClimbTree) {
        super(name, isNonVeg);
        this.name = name;
        this.isNonVeg = isNonVeg;
        this.canClimbTree = canClimbTree;
        this.canClimbTree = canClimbTree;
    }
    getDetails() {
        return ` can tiger climb a tree ? ${this.canClimbTree}`;
    }
}
class Leopard extends Animal {
    name;
    isNonVeg;
    canClimbTree;
    canRunFast;
    constructor(name, isNonVeg, canClimbTree, canRunFast) {
        super(name, isNonVeg);
        this.name = name;
        this.isNonVeg = isNonVeg;
        this.canClimbTree = canClimbTree;
        this.canRunFast = canRunFast;
        this.canClimbTree = canClimbTree;
        this.canRunFast = canRunFast;
    }
    getDetails() {
        return ` can Leopard climb a tree ? ${this.canClimbTree} and can leopard run faster ${this.canRunFast}`;
    }
}
let animalData = [new Tiger("TIGER", true, false), new Leopard("LEOPARD", true, true, true)];
animalData.forEach(item => {
    console.log(item.getSpecificDetails());
});
class MiddleAge {
    items;
    constructor(initialItems = []) {
        this.items = new Set(initialItems);
    }
    addItems(...newItems) {
        newItems.forEach(item => this.items.add(item));
    }
    getItems(name) {
        return [...this.items.values()].find(item => item);
    }
    getCount() {
        return [...this.items.values()].length;
    }
}
let shape = { age: 39 };
let normalPerson = new MiddleAge(data);
normalPerson.addItems(new Employee("3", "Raj", "VSKP", "IT"));
