'use strict';
// Uses the actual TypeScript compiler parser, not regex-matched quasi-ASTs.
const fs=require('fs');
let ts;try{ts=require('typescript')}catch{
  try{ts=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/typescript')}catch{process.stderr.write('Install typescript (npm) and set NODE_PATH to its directory.\n');process.exit(2)}
}
const lang=process.argv[2];if(!['javascript','typescript'].includes(lang))process.exit(2);
const source=fs.readFileSync(0,'utf8');if(Buffer.byteLength(source,'utf8')>32768)process.exit(2);
const sourceFile=ts.createSourceFile('input.'+(lang==='typescript'?'ts':'js'),source,ts.ScriptTarget.Latest,true,lang==='typescript'?ts.ScriptKind.TS:ts.ScriptKind.JS);
const nodes=[];
function walk(n,parent,depth){
 if(nodes.length>=640)throw Error('node budget');if(depth>80)throw Error('depth budget');
 const id='n'+String(nodes.length).padStart(4,'0');
 let label='';
 if(n.name?.text)label=String(n.name.text);
 else if(ts.isIdentifier(n))label=n.text;
 else if(ts.isStringLiteral(n))label=n.text;
 const start=sourceFile.getLineAndCharacterOfPosition(n.pos);
 nodes.push({kind:ts.SyntaxKind[n.kind],label:label.slice(0,100),parent,span:String(start.line+1)+':'+String(start.character+1)});
 ts.forEachChild(n,ch=>walk(ch,id,depth+1));
}
try{walk(sourceFile,null,0);process.stdout.write(JSON.stringify({parser:'TypeScript compiler '+ts.version+' syntax AST',nodes,diagnostics:(sourceFile.parseDiagnostics||[]).map(d=>ts.flattenDiagnosticMessageText(d.messageText,' ')).slice(0,5)}))}catch(e){process.stderr.write(String(e));process.exit(2)}
