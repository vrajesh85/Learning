import { Product } from './Product';
import { SimpleDataSource } from "./DataSource.model";

export class Model {
    private dataSource : SimpleDataSource;
    private products: Product[];
    private locator = (product : Product , id : number | undefined) => product.id == id;

    constructor(){
        this.dataSource = new SimpleDataSource();
        this.products = new Array<Product>();
        this.dataSource.products.forEach(prod => this.products.push(prod));
    }

    getProducts() : Product[] {
       return this.products;
    }

    getProductById(id : number) : Product | undefined{
        return this.products.find(prod => this.locator(prod, id));
    }

    saveProduct(product : Product){
        if(product.id == 0 || product.id == null){
            product.id = this.generateId();
            this.products.push(product);
        } else {
            let index = this.products.findIndex(prod => this.locator(prod , prod.id));
            this.products.splice(index, 1, product);
        }       
    }

    deleteProduct(id : number){
        let index = this.products.findIndex(prod => this.locator(prod , id));
        if(index > -1)
            this.products.splice(index , 1);
    }


    private generateId() : number {
        let candidate = 100;

        while(this.getProductById(candidate) != null){
            candidate++;
        }
        return candidate;
    }
}