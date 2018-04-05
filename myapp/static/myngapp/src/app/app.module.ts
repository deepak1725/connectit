import { BouncerGuard } from '@guards/bouncer.guard';
import { MaterialcompsModule } from './materialcomps/materialcomps.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule} from './app-routing.module'
import { AppComponent } from './app.component';
import { AuthComponent } from './auth/auth.component';
import { UserComponent } from './user/user.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';


@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    UserComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialcompsModule,
    AppRoutingModule,

  ],
  providers: [BouncerGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
