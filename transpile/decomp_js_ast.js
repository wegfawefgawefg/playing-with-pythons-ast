const escodegen = require("escodegen");
const fs = require("fs");
// take in a file of js ast
file = process.argv[2];
// json parse the file
let js_ast = JSON.parse(fs.readFileSync(file, "utf8"));
let p = escodegen.generate(js_ast);
console.log(p);
