import { Component, OnInit } from '@angular/core';
import { ImageItem, ImageItemComponent } from './image_item';
import 'rxjs/Rx';

import { 
  Http,
  Response,
  RequestOptions,
  Headers
} from '@angular/http';

import {
  ImageService
} from './image_service';

@Component({
  selector: 'my-app',
  templateUrl: 'app/content.html', 
  directives: [ImageItemComponent],
})

export class AppComponent implements OnInit {
    imageItems: ImageItem[] = [];
    
    constructor(public http: Http, public imageService: ImageService)
    {
    }
    
    ngOnInit(): void {
        this.refreshImages();
    }
    
    private refreshImages(): void 
    {
        this.imageService.refreshImages()
          .subscribe(
            (imageItems: any) => {
                var parsedResult = imageItems.json();
                var imgs = [];
                for (let item in  parsedResult)
                {
                    imgs.push(new ImageItem(parseInt(item), parsedResult[item]));
                }
                
                this.imageItems = imgs;
            });    
    }
    
    onAddImage(image_file: HTMLInputElement): void
    {
        var f = image_file.files[0];
        var r = new FileReader();
        
        var fd = new FormData();
        fd.append('name', f.name);
        fd.append('file', f);       
        var headers = new Headers();       

        this.http.post('http://localhost:8020', fd, {
                headers: headers
            }).subscribe(
                        data => { 
                            this.refreshImages();
                      },
                      err => {}, 
                      () => console.log('Authentication Complete')
            );
    }
    
    onRemoveSelectedImages(): void
    {
        var itemsForRemove = [];
        this.imageItems.map((item: ImageItem) => 
            {
                if(item.selected)
                {
                    itemsForRemove.push(item.fileName);
                } 
            }
        );
       
        if(itemsForRemove.length > 0)
        {
            var headers = new Headers();
            this.http.post('http://localhost:8020/remove_images', JSON.stringify(itemsForRemove), {
                    headers: headers
                }).subscribe(
                            data => { 
                                this.refreshImages();
                          },
                          err => { console.log(err); },
                          () => console.log('Images removed.')
                );
         }
    } 
    
    onChooseFile(add_button: HTMLInputElement): void
    {
        add_button.disabled = false;
    }
    
    onSelectedItemChanged(remove_button: HTMLInputElement) : void
    {
        console.log( this.imageItems);
        
        for(let index in this.imageItems)
        {           
            if(this.imageItems[index].selected)
            {
                remove_button.disabled = false;
                return;
            } 
        }
        
        remove_button.disabled = true;
    }
}