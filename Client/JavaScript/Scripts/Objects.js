const person = {
    name: "Rajesh",
    age: 40
}

// this prints [object object]
console.log(`the value of person is ${person}`);

let text = '';
for(let value in person)
{
    text += person[value] + '  ';
}

// this prints the values of objects
console.log(`the value of person with for loop is ${text}`);

// this prints with object.values()
const myArray = Object.values(person);
console.log(`the value of person with object values is ${myArray}`);


// this prints with Object.entries()
text = '';
for (let [key, value] of Object.entries(person)){
    text += key + ' : ' + value + ' ';
}

console.log(`the value of person with object entries is ${text}`);

// this is JSON stringify

console.log(`the value of person with JSON StringIfy is ${JSON.stringify(person)}`);

function Employee(name,age,qualification){
    this.name = name;
    this.age = age;
    this.qualification = qualification;
}

var myself = new Employee("Rajesh", 39, "SE");

Employee.prototype.nationality = "Indian";

console.log(`the nationality of employee is ${myself.nationality}`);

function Parent(name){
    this.name = name;
}

function Child(name , age){
    Parent.call(this, name);
    this.age = age;
}

// one way of doing...
Child.prototype.Nationality = "Indian";

// another way..

Child.prototype = Object.create(Parent.prototype);

Child.prototype.constructor = Child;

Child.prototype.shout = function () {
    console.log(`mummy`);
}

var childObject = new Child("Ananya", 2);

console.log(`the name and age of child is ${childObject.name} and ${childObject.age} with nationality as ${childObject.Nationality}`);

childObject.shout();

// the above code can be written in much cleaner way

class Animal {
    constructor(name){
        this.name = name;
    }

    speak(){
        console.log(`the name of the animal is ${this.name}`);
    }
}

class Dog extends Animal {
    constructor(name, breed){
        super(name);
        this.breed = breed;
    }

    bark(){
        console.log(`the dog barks bow bow`);
    }
}

var dog = new Dog("tommy","pit bull");

dog.speak();

dog.bark();