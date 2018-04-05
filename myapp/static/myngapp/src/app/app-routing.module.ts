import { AuthComponent } from './auth/auth.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { UserComponent } from './user/user.component';
import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { BouncerGuard } from '@guards/bouncer.guard';

export const APPROUTES: Routes = [
    {
        path: '', 
        component: UserComponent, 
        canActivate: [BouncerGuard], 
    },
    {
        path: '', 
        component: AuthComponent,
        children: [
            {
                path: '',
                component: AuthComponent
            },
            {
                path: 'login',
                component: AuthComponent
            },
        ] 
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
