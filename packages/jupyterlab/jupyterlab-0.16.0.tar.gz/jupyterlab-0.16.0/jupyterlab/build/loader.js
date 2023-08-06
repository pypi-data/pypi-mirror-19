// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var loader_1 = require('../../lib/application/loader');
/**
 * A module loader instance.
 */
var _loader = new loader_1.ModuleLoader();
/**
 * Define a module that can be synchronously required.
 *
 * @param path - The version-mangled fully qualified path of the module.
 *   For example, "foo@1.0.1/lib/bar/baz.js".
 *
 * @param callback - The callback function for invoking the module.
 */
function define(path, callback) {
    _loader.define.call(_loader, path, callback);
}
exports.define = define;
exports.loader = _loader;
