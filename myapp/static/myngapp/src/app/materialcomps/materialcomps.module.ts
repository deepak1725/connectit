import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule, MatCheckboxModule } from '@angular/material';
import { MatCardModule } from '@angular/material/card';

const MODULES = [
  MatCardModule, 
  MatButtonModule,
  MatCheckboxModule
];

@NgModule({
  imports: MODULES,
  exports: MODULES,
})

export class MaterialcompsModule { }
