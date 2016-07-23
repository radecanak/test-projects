import { Component, Injectable, bind } from '@angular/core';
import { ImageItem, ImageItemComponent } from './image_item';
import {Observable} from 'rxjs/Rx';
import 'rxjs/Rx';

import { 
  Http,
  Response,
  RequestOptions,
  Headers
} from '@angular/http';

@Injectable()
export class ImageService {
    public images: Observable<any>;
    
    constructor(public http: Http ) {
    }
    
    refreshImages(): any
    {
        this.images = this.http.get('http://localhost:8020/get_all_images')
        .map((res:Response) => { return res;})     
        .publishReplay(1).refCount();   
        return this.images;
    }
}

export var imageServiceInjectables: Array<any> = [
  bind(ImageService).toClass(ImageService)
];