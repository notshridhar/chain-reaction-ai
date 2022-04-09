import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { config } from '@app/util/config';
import { PageModule } from '@app/page/module';

if (config.name === 'prod')
    enableProdMode();

platformBrowserDynamic()
    .bootstrapModule(PageModule)
    .catch((err) => console.error(err));
