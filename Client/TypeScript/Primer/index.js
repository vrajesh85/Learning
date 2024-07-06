var hatPrice = 100;
console.log("hat price is ".concat(hatPrice));
var bootsPrice = 100;
console.log("boots price is ".concat(bootsPrice));
if (hatPrice === bootsPrice)
    console.log('both are same');
else
    console.log('both are NOT same');
var totalPrice = hatPrice + bootsPrice;
console.log("The total price is ".concat(totalPrice, " and type of totalPrice is ").concat(typeof (totalPrice)));
console.log("type of null is ".concat(typeof (null)));

let firstCity;
let secondCity = firstCity || "London";
console.log(`second city is ${secondCity}`);

function sumPrices(first, second, third){
    return first + second + third;
}

totalPrice = sumPrices(100,200);
console.log(`The sum is ${totalPrice}`);

let data = new Map();
data.set("hat", "Test 1");
data.set("boots", "test 2");

[...data.keys()].forEach(key => console.log(key.toString()));
[...data.keys()].forEach(key => console.log(data.get(key).toString()));

