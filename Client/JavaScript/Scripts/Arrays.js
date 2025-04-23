const cars = ['Honda', 'BMW', 'AUDI'];

const mobiles = ['iphone','samsung','oppo'];

const electronics = ['tv','fridge','washing machine'];

const houseitems = [cars, mobiles, electronics];

console.log(`Deleted first element of cars ${delete cars[0]} and now household items are ${cars}`);

console.log(`the value of cars is ${cars} and type of cars is ${typeof(cars)} and cars at 2 is ${cars.at(2)}`);

console.log(`'the value of all house hold items is ${houseitems} and electronics items are ${houseitems[2]}`);

{
    let text = '<ul>';

    electronics.forEach(myFunction);

    text += '</ul>';

    function myFunction(value){
        text += `<li> ${value} </li>`;
    }

    console.log(text);
}