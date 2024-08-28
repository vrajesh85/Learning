import { ApplicationRef , Component } from '@angular/core';
import { Model } from '../app/shared/models/ProductRepository.model';
import { Product } from './shared/models/Product';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.builtindir.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'example';
  model : Model = new Model();  
  selectedProduct : string | undefined;

  constructor(ref : ApplicationRef){
    (<any>window).appRef = ref;
    (<any>window).model = this.model;
  }

  getClasses(key : number) : string {
    let product = this.model.getProductById(key);
    return "p-2 " + ((product?.price ?? 0) < 40000 ? "bg-info" : "bg-warning");
  }

  getProductByPosition(index : number) : Product{
    return this.model.getProducts()[index];
  }

  getProducts() : Product[]{
    console.log("getProducts invoked");
    return this.model.getProducts();
  }

  getProductCount() : number {
    return this.getProducts().length;
  }

  getClassMap(key : number) : Object {
    let product = this.model.getProductById(key);
    return {
      "bg-info" : product?.name == "Laptop",
      "text-center bg-danger"  : (product?.price ?? 0) > 40000
    }
  }

  isProductSelected(product : Product) : boolean{
    return product.name == this.selectedProduct;
  }

  getKey(index : number , product : Product){
    return product.id;
  }
}
