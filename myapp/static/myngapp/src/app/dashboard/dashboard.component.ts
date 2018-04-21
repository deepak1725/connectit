import { UserService } from './../__services/user.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  providers: [UserService]
})
export class DashboardComponent implements OnInit {

  userData:any;
  followNotification = 2
  streamNotification = 1

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.getUserDetails()
  }

  getUserDetails = () => {
    this.userService.getAllUsers().subscribe(
      (response) => {
        console.log(response);
        this.userData = response.data;
      }
    )
  }
}
