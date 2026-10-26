/* GLASS Unison Clock Oracle — typing/tapping only. No search, shell eval, credentials or geolocation.
 * Built-in browser clocks are independently labeled from server clocks. When the local
 * Python companion isn't connected, API-only features remain unknown, never forged.
 */
(()=>{'use strict';
const $=id=>document.getElementById(id);
const input=$('expression'),results=$('lessons'),rail=$('operators'),zoneList=$('zoneList');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const OP=[
 {glyph:'۞',name:'DEVICE',insert:'۞',tip:'Device wall clock from the browser; not proof of server time.'},
 {glyph:'⊕',name:'UTC',insert:'⊕',tip:'World UTC clock: one common instant.'},
 {glyph:'⌛',name:'SERVER',insert:'⌛',tip:'Read the separate GLASS Python host clock, if connected.'},
 {glyph:'◷',name:'MONOTONIC',insert:'◷',tip:'A process/performance clock has no civil calendar epoch.'},
 {glyph:'⟳',name:'ZONES',insert:'⟳[America/New_York,Asia/Dubai]',tip:'IANA zones with legal UTC offsets and daylight rules.'},
 {glyph:'⌖',name:'EARTH',insert:'⌖[0,45]',tip:'Latitude, longitude and a 15° geometric wedge.'},
 {glyph:'☼',name:'SOLAR',insert:'☼[0,45]',tip:'Mean solar time + approximate NOAA equation of time.'},
 {glyph:'∆',name:'OFFSET',insert:'∆[America/New_York,Asia/Dubai]',tip:'Subtract legal UTC offsets at one instant.'},
 {glyph:'ϕ',name:'PHASE',insert:'ϕ[60]',tip:'Turn a measured duration into a cyclic phase.'},
 {glyph:'λ',name:'SHELL',insert:'λ⟳[Asia/Dubai]',tip:'Generate copyable instructional shell text. Never execute it automatically.'},
 {glyph:'∅',name:'UNKNOWN',insert:'∅',tip:'A missing observation is a typed state, not the numeric value zero.'},
 {glyph:'⟦⟧',name:'FRAME',insert:'⟦ ⊕ ⟧',tip:'Group symbolic expressions into one source frame.'}
];
const SHOWCASE=[
 ['UTC','UTC'],['LOS ANGELES','America/Los_Angeles'],['NEW YORK','America/New_York'],
 ['LONDON','Europe/London'],['CAIRO','Africa/Cairo'],['DUBAI','Asia/Dubai'],
 ['KOLKATA','Asia/Kolkata'],['KATHMANDU','Asia/Kathmandu'],['TOKYO','Asia/Tokyo'],
 ['SYDNEY','Australia/Sydney'],['AUCKLAND','Pacific/Auckland'],['CHATHAM','Pacific/Chatham']
];
const meta={
 '۞':['DEVICE CLOCK','Observed by the browser; changing your phone clock changes this reading.'],
 '⊕':['UTC ORIGIN','UTC is the common instant before civil-zone conversion.'],
 '⌛':['SERVER CLOCK','Another wall-clock observation; not necessarily synchronized with your device.'],
 '◷':['MONOTONIC','Elapsed clock; an arbitrary origin rather than a calendar timestamp.'],
 '∅':['NON-TIME','No value was observed. UNKNOWN is not the same as zero.'],
 '⟳':['CIVIL ZONES','IANA rules govern legal offsets and daylight-saving transitions.'],
 '⌖':['EARTH COORDINATE','15° longitude forms one geometric wedge; legal time zones do not strictly follow these wedges.'],
 '☼':['SOLAR GEOMETRY','Mean solar minutes = UTC + 4×longitude; apparent adds the equation of time.'],
 '∆':['OFFSET DIFFERENCE','Compare UTC offsets of two civil zones at the same instant.'],
 'ϕ':['CYCLE PHASE','Angle = 2π × fractional part of elapsed / period.'],
 'λ':['SHELL RECIPE','Generate source text for a real script; this website never executes it.'],
 '⟦':['FRAME BEGIN','A typed source grouping marker.'], '⟧':['FRAME END','A typed source grouping marker.']
};
let connection=false,serverSample=null,evalRequest=0,lastRemoteResult=null,frame=0,selectedSymbol='۞',firstPerf=performance.now(),lastPoll=0; 
const localZone=(()=>{try{return Intl.DateTimeFormat().resolvedOptions().timeZone||'DEVICE LOCAL'}catch{return 'DEVICE LOCAL'}})();
const formatZone=(date,zone)=>{try{return new Intl.DateTimeFormat('en-GB',{timeZone:zone,hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false,hourCycle:'h23'}).format(date)}catch{return 'UNAVAILABLE'}};
const utcFormat=d=>d.toISOString().slice(11,19);
const shortDate=d=>d.toISOString().slice(0,10);
const eot=(date)=>{
 const year=date.getUTCFullYear(),leap=year%4===0&&(year%100!==0||year%400===0),start=Date.UTC(year,0,0);
 const n=Math.floor((Date.UTC(year,date.getUTCMonth(),date.getUTCDate())-start)/86400000);
 const hour=date.getUTCHours()+date.getUTCMinutes()/60+date.getUTCSeconds()/3600;
 const g=2*Math.PI/(leap?366:365)*(n-1+(hour-12)/24);
 return {eq:229.18*(.000075+.001868*Math.cos(g)-.032077*Math.sin(g)-.014615*Math.cos(2*g)-.040849*Math.sin(2*g)),
 decl:.006918-.399912*Math.cos(g)+.070257*Math.sin(g)-.006758*Math.cos(2*g)+.000907*Math.sin(2*g)-.002697*Math.cos(3*g)+.00148*Math.sin(3*g)};
};
function coord(a){if(a.length!==2)throw Error('Coordinates require [latitude,longitude]');const [lat,lon]=a.map(Number);if(!a.every(x=>/^[+-]?\d{1,3}(?:\.\d{1,6})?$/.test(x))||!Number.isFinite(lat)||!Number.isFinite(lon)||lat< -90||lat>90||lon< -180||lon>180)throw Error('Latitude -90..90; longitude -180..180');return [lat,lon]}
function solarValues(lat,lon,date){const {eq,decl}=eot(date),dayMinutes=date.getUTCHours()*60+date.getUTCMinutes()+date.getUTCSeconds()/60+date.getUTCMilliseconds()/60000;
 const mean=dayMinutes+4*lon,apparent=mean+eq,angle=((apparent%1440+1440)%1440)/4-180,angleRad=angle*Math.PI/180,phi=lat*Math.PI/180;
 const sinAltitude=Math.sin(phi)*Math.sin(decl)+Math.cos(phi)*Math.cos(decl)*Math.cos(angleRad);
 const fmt=offset=>new Date(date.getTime()+offset*60000).toISOString().slice(0,19).replace('T',' ');
 return {mean:fmt(4*lon),apparent:fmt(4*lon+eq),eqMinutes:eq,elevation:Math.asin(Math.max(-1,Math.min(1,sinAltitude)))*180/Math.PI,wedge:Math.min(23,Math.max(0,Math.floor((lon+180)/15)))}
}
function parseLocal(source){if(typeof source!=='string'||source.length>2048)throw Error('Source limit 2048 characters');let pos=0,ops=[];
 const isSep=c=>/\s|[;·]/u.test(c||'');
 function skip(){while(pos<source.length&&isSep(source[pos]))pos++}
 function one(depth){if(depth>3)throw Error('Generator nesting exceeds limit');skip();const start=pos;if(pos>=source.length)throw Error('Missing operator');const op=source[pos++];if(!meta[op])throw Error('Only Unison operator symbols are accepted. Tap a glyph to learn it.');if(op==='λ'){const child=one(depth+1);if(['λ','∅','⟦','⟧'].includes(child.op))throw Error('λ needs one clock operator');return {op,args:[],source:source.slice(start,pos),child}}
 let args=[];if(['⟳','☼','⌖','∆','ϕ'].includes(op)){
  if(source[pos]!=='[')throw Error(op+' requires [operands]');pos++;let begin=pos;
  while(pos<source.length&&source[pos]!==']'){if('[\r\n'.includes(source[pos]))throw Error('Nested or invalid operand');if(pos-begin>512)throw Error('Operand size limit');pos++}
  if(source[pos]!==']')throw Error('Missing ]');args=source.slice(begin,pos++).split(',').map(x=>x.trim());if(!args.length||args.some(x=>!x))throw Error('Empty operand');if(op==='⟳'&&args.length>8)throw Error('Maximum eight zones');if(op==='∆'&&args.length!==2)throw Error('∆ requires two zones');if(['⟳','∆'].includes(op))for(const zone of args){if(!/^[A-Za-z0-9_.+/-]{1,96}$/.test(zone)||zone.includes('..'))throw Error('Invalid IANA zone');try{new Intl.DateTimeFormat('en',{timeZone:zone})}catch{throw Error('Unknown IANA zone: '+zone)}}
  if(['⌖','☼'].includes(op))coord(args);if(op==='ϕ'&&(args.length!==1||!/^[+-]?\d{1,3}(?:\.\d{1,6})?$/.test(args[0])||Number(args[0])<.1||Number(args[0])>86400))throw Error('ϕ period 0.1..86400 seconds');
 }
 return{op,args,source:source.slice(start,pos),child:null};}
 let frames=0;while(true){skip();if(pos>=source.length)break;const n=one(0);if(n.op==='⟦')frames++;if(n.op==='⟧')frames--;if(frames<0||frames>8)throw Error('Unmatched frame');ops.push(n);if(ops.length>24)throw Error('Maximum 24 operators');}if(frames)throw Error('Unclosed ⟦ frame');return ops;
}
function formatOffset(s){const sign=s>=0?'+':'-',abs=Math.abs(s);return sign+String(Math.floor(abs/3600)).padStart(2,'0')+':'+String(Math.floor(abs%3600/60)).padStart(2,'0')}
function offsetFor(date,zone){const parts=new Intl.DateTimeFormat('en-CA',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false,hourCycle:'h23'}).formatToParts(date);const obj={};for(const p of parts)if(p.type!=='literal')obj[p.type]=Number(p.value);
 const nominal=Date.UTC(obj.year,obj.month-1,obj.day,obj.hour===24?0:obj.hour,obj.minute,obj.second);
 const epochRounded=Math.floor(date.getTime()/1000)*1000;
 return Math.round((nominal-epochRounded)/1000);
}
function shellFor(op){const child=op.child||op;let base=child.op;const arg=child.args||[];
 if(base==='۞')return "date '+%Y-%m-%d %H:%M:%S %z'";
 if(base==='⊕')return "date -u '+%Y-%m-%dT%H:%M:%SZ'";
 if(base==='⌛')return "python3 -c 'import time; print(time.time_ns())' # local host";
 if(base==='◷')return "python3 -c 'import time; print(time.monotonic_ns())'";
 if(['⟳','∆'].includes(base))return "python3 - <<'PY'\nfrom datetime import datetime, timezone\nfrom zoneinfo import ZoneInfo\nzones = "+JSON.stringify(arg)+"\nnow = datetime.now(timezone.utc)\nfor zone in zones:\n    print(zone, now.astimezone(ZoneInfo(zone)).isoformat())\nPY";
 if(['⌖','☼'].includes(base)){const [lat,lon]=coord(arg);return "python3 - <<'PY'\nfrom datetime import datetime, timezone, timedelta\nlat, lon = "+lat+", "+lon+"\nprint(datetime.now(timezone.utc) + timedelta(minutes=4*lon))\nPY"}
 if(base==='ϕ'){const period=Number(arg[0]);return "python3 - <<'PY'\nimport math,time\nP="+period+"\nt0=time.monotonic()\nprint(2*math.pi*((time.monotonic()-t0)%P)/P)\nPY"}
 return '# No executable shell operator registered';
}
function offlineEvaluate(ops){const now=new Date(),results=[];for(const op of ops){let values={},status='BROWSER_REFERENCE',lesson=meta[op.op][1];switch(op.op){
 case '۞':values={device_time:now.toLocaleString(),time:formatZone(now,localZone)};break;
 case '⊕':values={utc_iso:now.toISOString(),source:'device clock, NOT server UTC'};break;
 case '⌛':status='UNKNOWN';values={server_clock:'NOT CONNECTED'};break;
 case '◷':values={browser_elapsed_seconds:((performance.now()-firstPerf)/1000).toFixed(3),source:'performance clock (browser origin)'};break;
 case '∅':status='UNKNOWN_BY_DESIGN';values={clock:'UNOBSERVED',numeric_zero:false};break;
 case '⟳':values={zones:op.args.map(name=>({zone:name,time:formatZone(now,name),offset_seconds:offsetFor(now,name)}))};break;
 case '∆':{const [a,b]=op.args;values={from:a,to:b,to_minus_from:formatOffset(offsetFor(now,b)-offsetFor(now,a)),label:'UTC offset difference'};break}
 case '⌖':{const [lat,lon]=coord(op.args),s=solarValues(lat,lon,now);values={latitude:lat,longitude:lon,wedge:s.wedge,mean_offset_minutes:4*lon,orientation:'longitude east-positive'};break}
 case '☼':{const [lat,lon]=coord(op.args);values=solarValues(lat,lon,now);values.model='NOAA approximate solar geometry from browser clock';break}
 case 'ϕ':{const period=Number(op.args[0]);values={period_seconds:period,phase_radians:((performance.now()-firstPerf)/1000%period)/period*2*Math.PI};break}
 case 'λ':status='GENERATED_NOT_EXECUTED';values={shell:shellFor(op)};lesson='This is a shell teaching artifact only; nothing has executed.';break;
 default:values={source_group:op.op};}
 results.push({operator:op.op,title:meta[op.op][0],kind:'client',lesson,status,values});}return{schema:'glass.clock.browser-preview/0.1',results,operators:ops.map(x=>x.op)}}
function simplify(result){const o=result.operator,v=result.values||{};
 if(o==='۞')return v.device_time||v.device_reported_iso||'UNOBSERVED';
 if(o==='⊕')return v.utc_iso||'UTC unavailable';
 if(o==='⌛')return v.server_wall_utc||v.server_clock||'NOT CONNECTED';
 if(o==='◷')return (v.process_elapsed_seconds??v.browser_elapsed_seconds??'—')+' seconds';
 if(o==='∅')return '∅  UNOBSERVED';
 if(o==='⟳')return (v.zones||[]).map(z=>z.zone+' '+(z.time||'')+' ['+formatOffset(z.offset_seconds||0)+']').join('\n');
 if(o==='∆')return (v.to_minus_from||'UNKNOWN')+'  ·  '+(typeof v.from==='string'?v.from:v.from?.zone||'')+' → '+(typeof v.to==='string'?v.to:v.to?.zone||'');
 if(o==='⌖')return 'WEDGE '+(v.longitude_wedge_15deg??v.wedge)+' · LON '+(v.longitude_deg??v.longitude)+'° · SOLAR Δ '+(v.mean_solar_offset_minutes??v.mean_offset_minutes)+' min';
 if(o==='☼')return 'MEAN '+(v.mean_solar_label??v.mean)+'\nAPPARENT '+(v.apparent_solar_label??v.apparent)+'\nSUN '+Number(v.solar_elevation_deg??v.elevation??0).toFixed(2)+'°';
 if(o==='ϕ')return 'ϕ = '+Number(v.angle_radians??v.phase_radians??0).toFixed(5)+' radians';
 if(o==='λ')return 'λ  GENERATED SHELL SOURCE · NOT EXECUTED';
 return o+' / '+JSON.stringify(v);
}
function renderResults(payload,error){results.replaceChildren();const rs=payload?.results||[];if(error){const box=document.createElement('article');box.className='result error';const title=document.createElement('div');title.className='result-top';title.textContent='∅   GRAMMAR REFUSAL';const main=document.createElement('div');main.className='result-main';main.textContent=error;const lesson=document.createElement('div');lesson.className='result-info';lesson.textContent='An unfinished or unknown program has no side effects. Tap a glyph to insert its admitted form.';box.append(title,main,lesson);results.append(box);$('traceLabel').textContent='EVENTS 0000';return;}
 if(!rs.length){const item=document.createElement('div');item.className='lesson-placeholder';item.textContent='۞  ⊕  ☼';const span=document.createElement('span');span.textContent='Touch a symbol. GLASS will explain the computation.';item.append(span);results.append(item);$('traceLabel').textContent='EVENTS 0000';return;}
 for(const r of rs){const box=document.createElement('article');box.className='result';const heading=document.createElement('div');heading.className='result-top';const glyph=document.createElement('span');glyph.className='result-glyph';glyph.textContent=r.operator;const label=document.createElement('span');label.textContent=r.title;heading.append(glyph,label);
  const main=document.createElement('div');main.className='result-main';main.textContent=simplify(r);main.style.whiteSpace='pre-wrap';
  const desc=document.createElement('div');desc.className='result-info';desc.textContent=(r.status==='GENERATED_NOT_EXECUTED'?'GENERATED SOURCE · ':'')+r.lesson;box.append(heading,main,desc);
  if(r.operator==='λ'){const code=document.createElement('pre');code.className='result-code';code.textContent=r.values.shell||'';code.tabIndex=0;code.title='Tap to copy this generated shell text (does not execute it)';code.addEventListener('click',()=>{if(navigator.clipboard?.writeText){navigator.clipboard.writeText(code.textContent).then(()=>{desc.textContent='Source copied. It has not been executed.'}).catch(()=>{})}});box.append(code);}
  results.append(box);
 }
 $('traceLabel').textContent='EVENTS '+String(payload.event_trace?.length??rs.length).padStart(4,'0');
}
function insertSymbol(text){let a=input.selectionStart??input.value.length,b=input.selectionEnd??a;input.value=input.value.slice(0,a)+text+input.value.slice(b);input.focus({preventScroll:true});const pos=a+text.length;const bracket=text.indexOf('[');input.selectionStart=input.selectionEnd=bracket>=0?a+bracket+1:pos;onInput()}
for(const entry of OP){const item=document.createElement('span');item.className='operator';item.setAttribute('role','option');item.setAttribute('tabindex','0');item.setAttribute('aria-label',entry.tip);item.title=entry.tip;item.textContent=entry.glyph;const sm=document.createElement('small');sm.className='op-code';sm.textContent=entry.name;item.append(sm);item.addEventListener('click',()=>insertSymbol(entry.insert));item.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();insertSymbol(entry.insert)}});rail.append(item);}
function renderZones(now=new Date()){zoneList.replaceChildren();const frag=document.createDocumentFragment();SHOWCASE.forEach(([label,name])=>{const row=document.createElement('div');row.className='zone';const nm=document.createElement('span');nm.className='zone-name';nm.textContent=label;const t=document.createElement('span');t.className='zone-clock';t.textContent=formatZone(now,name);row.append(nm,t);frag.append(row)});zoneList.append(frag)}
function refreshClocks(){const now=new Date();$('localTime').textContent=formatZone(now,localZone);$('localZone').textContent=localZone.replace(/_/g,' ');$('utcTime').textContent=utcFormat(now);$('utcDate').textContent=shortDate(now)+' · UTC';$('monoTime').textContent=((performance.now()-firstPerf)/1000).toFixed(3)+'s';
 if(serverSample){const ms=serverSample.server_ms+(performance.now()-serverSample.receive_perf);$('serverTime').textContent=utcFormat(new Date(ms));$('serverAge').textContent='SERVER SAMPLE '+((performance.now()-serverSample.receive_perf)/1000).toFixed(1)+'s OLD';$('skewTime').textContent=(serverSample.offset_ms>=0?'+':'')+serverSample.offset_ms.toFixed(0)+' ms ~'+serverSample.error_bound_ms.toFixed(0)+' RTT/2';}
 else{$('serverTime').textContent='UNKNOWN';$('serverAge').textContent='LOCAL TERMINAL OFFLINE';$('skewTime').textContent='UNKNOWN';}
 $('frameEpoch').textContent='⟦ '+String(Math.floor((performance.now()-firstPerf)/1000)+1).padStart(6,'0')+' ⟧';
 renderZones(now);
}
async function pollServer(){const sent_perf=performance.now(),sent_wall=Date.now();try{const r=await fetch('/api/time',{cache:'no-store',signal:AbortSignal.timeout(3000)});if(!r.ok)throw Error('server '+r.status);const data=await r.json();if(data.schema!=='glass.clock-oracle/0.1'||!Number.isFinite(data.server_epoch_ms))throw Error('invalid server time');const recv_perf=performance.now(),recv_wall=Date.now();const rtt=recv_perf-sent_perf;const midpoint=(sent_wall+recv_wall)/2;serverSample={server_ms:data.server_epoch_ms,receive_perf:recv_perf,offset_ms:data.server_epoch_ms-midpoint,error_bound_ms:rtt/2};connection=true;$('statusText').textContent='SERVER CONNECTED';$('statusDot').classList.add('online');refreshClocks();triggerEval();}
 catch{connection=false;serverSample=null;$('statusText').textContent='LOCAL ONLY';$('statusDot').classList.remove('online');refreshClocks();}}
let evalTimer=null;
function onInput(){clearTimeout(evalTimer);const source=input.value;let ops;try{ops=parseLocal(source)}catch(err){renderResults(null,err.message);$('parserMode').textContent='PARSER / REFUSAL';return}
 $('parserMode').textContent='GRAMMAR / '+ops.length+' OPERATORS';renderResults(offlineEvaluate(ops));
 if(connection){evalTimer=setTimeout(triggerEval,120)}
 if(ops.length){selectedSymbol=ops.at(-1).op;if(ops.at(-1).op==='λ')selectedSymbol=ops.at(-1).child?.op||'λ';$('centerGlyph').textContent=selectedSymbol;}
}
async function triggerEval(){if(!connection)return;const source=input.value;let ops;try{ops=parseLocal(source)}catch{return}const seq=++evalRequest;try{const r=await fetch('/api/eval',{method:'POST',headers:{'Content-Type':'application/json'},cache:'no-store',body:JSON.stringify({source,client_epoch_ms:Date.now()}),signal:AbortSignal.timeout(5000)});const data=await r.json();if(seq!==evalRequest||source!==input.value)return;if(!r.ok){renderResults(null,data.error||'Grammar refused');return}lastRemoteResult=data;renderResults(data);}
 catch{if(seq!==evalRequest)return;connection=false;serverSample=null;$('statusText').textContent='LOCAL ONLY';$('statusDot').classList.remove('online');renderResults(offlineEvaluate(ops));}}
input.addEventListener('input',onInput);
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();const position=input.selectionStart||0;input.value=input.value.slice(0,position)+' · '+input.value.slice(input.selectionEnd||position);input.selectionStart=input.selectionEnd=position+3;onInput()}});
// Canvas globe: a geometric model of 24 longitudinal wedges; never a map of legal IANA time zones.
const globe=$('globe'),gc=globe.getContext('2d',{alpha:true}),stars=$('stars'),sc=stars.getContext('2d',{alpha:true});
const TWO=Math.PI*2;let starfield=[];let sampleRate=0;
function resizeCanvas(c,context){const r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);if(c.width!==Math.round(r.width*d)||c.height!==Math.round(r.height*d)){c.width=Math.max(1,Math.round(r.width*d));c.height=Math.max(1,Math.round(r.height*d))}context.setTransform(d,0,0,d,0,0);return{w:r.width,h:r.height}}
function initializeStars(){const {w,h}=resizeCanvas(stars,sc);let seed=74017;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};starfield=Array.from({length:Math.min(135,Math.max(35,Math.round(w*h/12000)))},()=>({x:rnd(),y:rnd(),r:.3+rnd()*.9,tw:rnd()*TWO}))}
function paintStars(t){const{w,h}=resizeCanvas(stars,sc);sc.clearRect(0,0,w,h);for(const pt of starfield){const alpha=.08+.2*(.5+.5*Math.sin(t*.00031+pt.tw));sc.fillStyle=`rgba(219,195,154,${alpha})`;sc.fillRect(pt.x*w,pt.y*h,pt.r,pt.r)}}
function paintGlobe(ms){const{w,h}=resizeCanvas(globe,gc);gc.clearRect(0,0,w,h);const cx=w/2,cy=h*.48,R=Math.min(w*.43,h*.43),incline=.28;const rot=ms*.000018;
 const halo=gc.createRadialGradient(cx,cy,R*.05,cx,cy,R*1.4);halo.addColorStop(0,'rgba(184,139,77,.14)');halo.addColorStop(.62,'rgba(99,126,145,.045)');halo.addColorStop(1,'rgba(0,0,0,0)');gc.fillStyle=halo;gc.beginPath();gc.arc(cx,cy,R*1.4,0,TWO);gc.fill();
 const map=(la,lo)=>{const lat=la*Math.PI/180,lng=lo*Math.PI/180+rot;const x=Math.cos(lat)*Math.sin(lng),z=Math.cos(lat)*Math.cos(lng);const y=Math.sin(lat)*Math.cos(incline)-z*Math.sin(incline);const depth=z*Math.cos(incline)+Math.sin(lat)*Math.sin(incline);return{x:cx+x*R,y:cy-y*R,depth}};
 gc.save();gc.strokeStyle='rgba(205,173,125,.21)';gc.lineWidth=.75;gc.beginPath();gc.ellipse(cx,cy,R,R*.98,0,0,TWO);gc.stroke();
 const arcs=[];for(let longitude=-180;longitude<180;longitude+=15){const pts=[];for(let lat=-90;lat<=90;lat+=3)pts.push(map(lat,longitude));arcs.push({kind:'longitude',pts,highlight:longitude===0})}
 for(let latitude=-75;latitude<=75;latitude+=15){const pts=[];for(let lon=-180;lon<=180;lon+=3)pts.push(map(latitude,lon));arcs.push({kind:'latitude',pts,highlight:latitude===0})}
 for(const line of arcs){const segments=[[],[]];for(let i=0;i<line.pts.length;i++){const p=line.pts[i];segments[p.depth>=0?0:1].push(p);if(i&&Math.sign(p.depth)!==Math.sign(line.pts[i-1].depth)){segments[0].push(p);segments[1].push(p)}}for(let half=1;half>=0;half--){const points=segments[half];if(points.length<2)continue;gc.strokeStyle=line.highlight?(half?'rgba(244,212,157,.09)':'rgba(250,211,153,.37)'):(half?'rgba(101,132,146,.06)':'rgba(173,185,170,.16)');gc.lineWidth=line.highlight?1.1:.55;gc.beginPath();for(let i=0;i<points.length;i++){const p=points[i];i?gc.lineTo(p.x,p.y):gc.moveTo(p.x,p.y)}gc.stroke()}}
 // Exact 24 x 15° wedge spokes are the meridian planes, not political zones.
 gc.strokeStyle='rgba(204,176,119,.23)';gc.beginPath();gc.ellipse(cx,cy,R*.98,R*.32,rot*.1,0,TWO);gc.stroke();
 const now=new Date();const utcHour=(now.getUTCHours()+now.getUTCMinutes()/60+now.getUTCSeconds()/3600);const sunLon=(12-utcHour)*15;const pt=map(0,sunLon);if(pt.depth>=-.2){const glow=gc.createRadialGradient(pt.x,pt.y,0,pt.x,pt.y,22);glow.addColorStop(0,'#ffe1acb8');glow.addColorStop(1,'#d4a66400');gc.fillStyle=glow;gc.beginPath();gc.arc(pt.x,pt.y,22,0,TWO);gc.fill();gc.fillStyle='#ffe9bd';gc.beginPath();gc.arc(pt.x,pt.y,3,0,TWO);gc.fill()}
 const rad=R*1.22;gc.font=`${Math.max(15,Math.min(27,R*.1))}px 'Amiri','Noto Naskh Arabic',serif`;gc.textAlign='center';gc.textBaseline='middle';const glyphs=['۞','⊕','⌛','◷','⟳','⌖','☼','∆','ϕ','λ','∅','⟦','⟧'];for(let k=0;k<glyphs.length;k++){const angle=k/glyphs.length*TWO+ms*.000035;gc.fillStyle=k%3?'rgba(194,161,110,.48)':'rgba(241,209,158,.78)';gc.fillText(glyphs[k],cx+Math.cos(angle)*rad,cy+Math.sin(angle)*rad*.88)}gc.restore();
}
function animate(t){if(!document.hidden){paintGlobe(reduce?0:t);if(!reduce&&Math.floor(t/90)!==sampleRate){paintStars(t);sampleRate=Math.floor(t/90)}}requestAnimationFrame(animate)}
window.addEventListener('resize',()=>{initializeStars();paintGlobe(0)});
// The terminal shows runnable examples only after explicit λ; original input stays local.
input.value='۞  ⊕  ⌛  ◷  ⟳[America/New_York,Asia/Dubai]';
initializeStars();refreshClocks();onInput();pollServer();
setInterval(refreshClocks,1000);setInterval(pollServer,5000);
if(!reduce)requestAnimationFrame(animate);else paintGlobe(0);
window.GLASS_CLOCK={parse:parseLocal,solar:solarValues,meta,offlineEvaluate,geometry:coord};
})();
