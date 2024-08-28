import { Product } from './Product'

export class SimpleDataSource {

    private SimpleProducts:Product[];
    private productOne : Product = new Product(1, "Laptop", "Electronic", 30000);
    private productTwo : Product = new Product(2, "TV", "Electronic", 65000);
    private productThree : Product = new Product(3, "Fridge", "Electronic", 20000);
    private productFour : Product = new Product(4, "Mobile", "Gadget", 65000);

    constructor(){
        this.SimpleProducts  = new Array<Product>(this.productOne , this.productTwo, this.productThree , this.productFour);    
    }

    get products() : Product[]{
        return this.SimpleProducts; 
    }
       
}