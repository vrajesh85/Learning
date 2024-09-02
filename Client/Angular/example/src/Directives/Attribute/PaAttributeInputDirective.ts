import { Directive , Input , ElementRef } from '@angular/core';

@Directive({
    selector : "[pa-attr-input]"
})
export class PaAttributeInputDirective {
    constructor(private element : ElementRef) {}

    @Input("pa-attr-input")
    bgClass : string | null = "";

    ngOnInit(){
        this.element.nativeElement.classList.add(this.bgClass || "text-primary", "fw-bold");
    }
}