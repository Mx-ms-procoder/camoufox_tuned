const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'../..');
const primitive=fs.readFileSync(path.join(root,'additions/juggler/protocol/PrimitiveTypes.js'),'utf8').replace(/export \{ t, checkScheme \};/,'');
const protocol=fs.readFileSync(path.join(root,'additions/juggler/protocol/Protocol.js'),'utf8').replace(/^const \{t, checkScheme\}.*$/m,'').replace('export const protocol','const protocol').replace(/export \{ checkScheme \};/,'');
const data=vm.runInNewContext(primitive+'\n'+protocol+'\n'+`JSON.stringify((()=>{const base={viewport:{viewportSize:{width:800,height:600},deviceScaleFactor:1}};const modern={viewport:{...base.viewport,isMobile:false}};const details={};return {baselineAccepted:checkScheme(protocol.domains.Browser.methods.setDefaultViewport.params,base,{}),modernAccepted:checkScheme(protocol.domains.Browser.methods.setDefaultViewport.params,modern,details),details};})())`);
fs.writeFileSync(path.join(__dirname,'evidence/protocol-probe.json'),data);console.log(data);
