let x = 20;

function somefunc(){
 let x = 10;
  x = 30;
 console.log(`from somefunc with let  ${x}`);
}

somefunc();

const owner = ["Rajesh","Vemulakonda","Kids"];

// we can change value of existing 
owner[2] = "Ashritha & Ananya";

// we can push new value
owner.push("new kid");

console.log(`the value of existing kids is ${owner[2]} and value of new kid id is ${owner[3]}`);

console.log(`value of x is  ${x}`);