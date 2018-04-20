import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { BouncerGuard } from '@guards/bouncer.guard';

export const APPROUTES: Routes = [
    {
        path: '', 
        component: DashboardComponent,
    },
    {
        path: 'dashboard', 
        component: DashboardComponent, 
    },
    { 
        path: '**', 
        component: PageNotFoundComponent, 
    }
]


@NgModule({
    imports: [
        RouterModule.forRoot(APPROUTES,
            { enableTracing: true }
        )
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule { }
// export const routingMethods = [AuthComponent, UserComponent, PageNotFoundComponent];
