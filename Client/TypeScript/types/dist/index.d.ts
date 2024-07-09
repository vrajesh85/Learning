declare let numericValue: unknown;
declare function check(expres: any): asserts expres is boolean;
declare function multiply(amount: number): number;
declare function writeAmount(amount: number, product: string): void;
declare let names: string[];
declare let prices: number[];
declare let price: any;
declare let halfPrice: number;
declare let hats: [string, number];
declare let Gloves: [string, number];
declare let hatname: string, hatPrice: number;
declare let products: [string, number][];
declare let tupleUnions: ([string, number] | boolean)[];
declare enum Product {
    "AP" = 1,
    "TG" = 2,
    "TN" = 3
}
declare class Person {
    id: string;
    name: string;
    city: string;
    constructor(id: string, name: string, city: string);
}
declare class Employee extends Person {
    id: string;
    name: string;
    city: string;
    private dept;
    constructor(id: string, name: string, city: string, dept: string);
}
declare class Customer extends Person {
    id: string;
    name: string;
    city: string;
    private credit;
    constructor(id: string, name: string, city: string, credit: number);
}
declare class Supplier extends Person {
    id: string;
    name: string;
    city: string;
    companyName: string;
    constructor(id: string, name: string, city: string, companyName: string);
}
declare let data: Person[];
declare abstract class Animal {
    name: string;
    isNoNVeg: boolean;
    constructor(name: string, isNoNVeg: boolean);
    abstract getDetails(): string;
    getSpecificDetails(): string;
}
declare class Tiger extends Animal {
    name: any;
    isNonVeg: boolean;
    canClimbTree: boolean;
    constructor(name: any, isNonVeg: boolean, canClimbTree: boolean);
    getDetails(): string;
}
declare class Leopard extends Animal {
    name: any;
    isNonVeg: boolean;
    canClimbTree: boolean;
    canRunFast: boolean;
    constructor(name: any, isNonVeg: boolean, canClimbTree: boolean, canRunFast: boolean);
    getDetails(): string;
}
declare let animalData: Animal[];
