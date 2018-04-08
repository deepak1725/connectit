import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule, MatCheckboxModule } from '@angular/material';
import { MatCardModule } from '@angular/material/card';
import {MatGridListModule} from '@angular/material/grid-list';

const MODULES = [
  MatCardModule, 
  MatButtonModule,
  MatCheckboxModule,
  MatGridListModule,
];

@NgModule({
  imports: MODULES,
  exports: MODULES,
})

export class MaterialcompsModule { }
