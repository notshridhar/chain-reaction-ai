import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { PageRouterModule } from './route';
import { AppComponent } from './component/app';
import { GridComponent } from './component/grid';
import { CellComponent } from './component/cell';

@NgModule({
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        CommonModule,
        HttpClientModule,
        PageRouterModule
    ],
    declarations: [
        AppComponent,
        GridComponent,
        CellComponent,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class PageModule {}
