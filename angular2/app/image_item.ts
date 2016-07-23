import { 
    Component, 
    Input, 
    Output, 
    EventEmitter 
} from '@angular/core';

@Component({
    selector: 'image-item',
    templateUrl: 'app/image_item.html',
})

export class ImageItemComponent 
{
    @Input() imageItem : ImageItem; 
    @Output() selectedItemChanged : any = new EventEmitter();
    
    public get selected() {
        return this.imageItem.selected;
    }
    
    public set selected(value) {
        this.imageItem.selected = value; 
        this.selectedItemChanged.emit();   
    }
}
    
export class ImageItem 
{
    public index: any;
    public fileName : string;
    public selected : boolean;
    constructor(itemIndex : any, fileName :string)
    {
        this.index = itemIndex;
        this.fileName = fileName;
    }
    
    
    
  
}