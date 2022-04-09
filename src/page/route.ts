import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GridComponent } from './component/grid';

const routes: Routes = [
    { path: 'game', component: GridComponent },
    { path: '**', redirectTo: 'game' }
];

@NgModule({
    declarations: [],
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class PageRouterModule {}
