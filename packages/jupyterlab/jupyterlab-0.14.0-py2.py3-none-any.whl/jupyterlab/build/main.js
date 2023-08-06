// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var es6_promise_1 = require('es6-promise');
var application_1 = require('../../lib/application');
require('font-awesome/css/font-awesome.min.css');
require('../../lib/default-theme/index.css');
es6_promise_1.polyfill();
/* tslint:disable */
var mods = [
    require('../../lib/about/plugin'),
    require('../../lib/application/plugin'),
    require('../../lib/clipboard/plugin'),
    require('../../lib/codemirror/plugin'),
    require('../../lib/commandlinker/plugin'),
    require('../../lib/commandpalette/plugin'),
    require('../../lib/console/plugin'),
    require('../../lib/csvwidget/plugin'),
    require('../../lib/docmanager/plugin'),
    require('../../lib/docregistry/plugin'),
    require('../../lib/editorwidget/plugin'),
    require('../../lib/faq/plugin'),
    require('../../lib/filebrowser/plugin'),
    require('../../lib/help/plugin'),
    require('../../lib/imagewidget/plugin'),
    require('../../lib/inspector/plugin'),
    require('../../lib/landing/plugin'),
    require('../../lib/launcher/plugin'),
    require('../../lib/instancerestorer/plugin'),
    require('../../lib/mainmenu/plugin'),
    require('../../lib/markdownwidget/plugin'),
    require('../../lib/notebook/plugin'),
    require('../../lib/rendermime/plugin'),
    require('../../lib/running/plugin'),
    require('../../lib/services/plugin'),
    require('../../lib/shortcuts/plugin'),
    require('../../lib/statedb/plugin'),
    require('../../lib/terminal/plugin'),
    require('../../lib/tooltip/plugin')
];
/* tslint:enable */
/**
 * Create an application object.
 *
 * @param loader - The module loader for the application.
 *
 * @returns A new application object.
 */
function createLab(loader) {
    var lab = new application_1.JupyterLab({
        loader: loader,
        gitDescription: process.env.GIT_DESCRIPTION,
        namespace: 'jupyterlab',
        version: require('../../package.json').version
    });
    lab.registerPluginModules(mods);
    return lab;
}
exports.createLab = createLab;
