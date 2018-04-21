import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response, HttpModule } from '@angular/http';
import { Observable } from "rxjs/Rx"



@Injectable()
export class UserService {
  headers: Headers;
  options: RequestOptions;
  currentUser: any;

  constructor(private http: Http, private httpModule: HttpModule) { 
    this.options = new RequestOptions();
    if (this.options.headers == null) {
      this.options.headers = new Headers();
    }

    this.options.headers.append('Content-Type', 'application/json');
  }

  getAllUsers() {
    return this.http.get(
      'api/user',
      this.options
    ).map((response) => response.json() )
    .catch(this.handleError);
  }

  public handleError = (error: Response) => {

    return Observable.throw(error)
  }


}
