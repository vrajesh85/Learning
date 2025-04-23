function myFunction() {
    return () => { console.log('this is return value') };
}

let value = myFunction;
(value())();