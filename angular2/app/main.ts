import { bootstrap }    from '@angular/platform-browser-dynamic';
import { Component, provide } from '@angular/core';
import {APP_BASE_HREF} from '@angular/common';

import { 
  HTTP_PROVIDERS
} from '@angular/http';
import { AppComponent } from './app.component';
import { NotFoundComponent } from './not_found';
import { imageServiceInjectables } from './image_service';

import {
  ROUTER_DIRECTIVES,
  ROUTER_PROVIDERS,
  RouteConfig,
} from '@angular/router-deprecated';

@Component({
  selector: 'router-app',
  directives: [ROUTER_DIRECTIVES],
  templateUrl: 'app/main.html',
})


@RouteConfig([
  { path: '/', name: 'root', redirectTo: ['/Home'] },
  { path: '/home', name: 'Home', component: AppComponent },
  { path: '/index', name: 'Index', redirectTo: ['/Home'] },
  {path: '/404', name: 'NotFound', component: NotFoundComponent},
  {path: '/*path', redirectTo: ['NotFound']}
])

class RoutesApp {
}


bootstrap(RoutesApp, [ROUTER_PROVIDERS, HTTP_PROVIDERS, imageServiceInjectables, provide(APP_BASE_HREF, {useValue : '/' })]);