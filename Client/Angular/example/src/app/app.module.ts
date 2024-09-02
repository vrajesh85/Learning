import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { PaAttributeDirective }   from '../Directives/Attribute/PaAttributeDirective';
import { PaAttributeInputDirective } from '../Directives/Attribute/PaAttributeInputDirective';

@NgModule({
  declarations: [
    AppComponent,
    PaAttributeDirective,
    PaAttributeInputDirective
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
