/* Offline canvas network. Every supplied node/edge is retained; no vendor runtime. */
class AuditNetwork {
  constructor(canvas, {onNode, onEdge, onStatus}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.callbacks = {onNode, onEdge, onStatus};
    this.nodes = []; this.edges = []; this.positions = []; this.edgePage = 0;
    this.camera = {x:0, y:0, k:1}; this.generation = 0; this.highlighted = null;
    this.selected = null; this.frame = null; this.paused = false;
    this.palette = ['#477591','#548b82','#7a729a','#aa8750','#788554','#8d7180','#567694','#6b8789'];
    new ResizeObserver(()=>{this.resize();this.requestDraw()}).observe(canvas.parentElement);
    this.layoutCache=new WeakMap();this.workers=[];this.bindPointer();
  }
  resize() {
    const r=this.canvas.parentElement.getBoundingClientRect();
    this.width=Math.max(1,r.width); this.height=Math.max(1,r.height);
    this.dpr=Math.min(window.devicePixelRatio||1,2);
    this.canvas.width=Math.round(this.width*this.dpr);
    this.canvas.height=Math.round(this.height*this.dpr);
  }
  setGraph(graph) {
    if(this.graph===graph)return;
    this.stopWorkers();this.graph=graph; this.generation++; this.paused=false; this.selected=null; this.highlighted=null;this.cameraTouched=false;
    this.nodes=graph.nodes; this.edges=graph.edges;
    this.index=new Map(this.nodes.map((n,i)=>[n.id,i]));
    this.edgeIndex=new Map(this.edges.map((e,i)=>[e.id,i]));
    this.degree=new Uint32Array(this.nodes.length); this.neighbors=this.nodes.map(()=>[]);
    this.ends=this.edges.map((e,i)=>{const a=this.index.get(e.source),b=this.index.get(e.target);
      this.degree[a]++;this.degree[b]++;this.neighbors[a].push(i);if(a!==b)this.neighbors[b].push(i);return [a,b]});
    const groups=new Map();
    this.groupOf=this.nodes.map(n=>{
      const key=String(n.group??n.path??n.kind??'Other')||'Other';
      if(!groups.has(key))groups.set(key,groups.size);return groups.get(key);
    });
    this.groupNames=[...groups.keys()];
    this.partition=partitionNetwork(this.groupOf,this.ends);
    const golden=Math.PI*(3-Math.sqrt(5)),count=this.partition.jobs.length;
    const pitch=Math.max(110,Math.sqrt(this.nodes.length/Math.max(1,count))*25);
    this.positions=this.nodes.map(()=>({x:0,y:0,vx:0,vy:0}));
    for(const job of this.partition.jobs){job.cx=Math.cos(job.id*golden)*Math.sqrt(job.id)*pitch;job.cy=Math.sin(job.id*golden)*Math.sqrt(job.id)*pitch;
      job.ids.forEach((i,j)=>{const r=14*Math.sqrt(j);Object.assign(this.positions[i],{x:job.cx+Math.cos(j*golden)*r,y:job.cy+Math.sin(j*golden)*r})});}
    this.internalEdges=this.partition.jobs.reduce((n,j)=>n+j.links.length,0);
    if(this.internalEdges+this.partition.crossEdges.length!==this.edges.length)throw Error('Partition edge reconciliation failed');
    this.completedJobs=0;this.failedJobs=0;this.queue=[...this.partition.jobs];this.workerMode='pending';this.layoutStarted=performance.now();
    const cached=this.layoutCache.get(graph);
    if(cached){this.positions=cached.map(p=>({...p}));this.completedJobs=count;this.queue=[];this.workerMode='cached';}
    // Keep parallel and reverse relations separately inspectable.
    const pairs=new Map();this.offsets=this.edges.map((e,i)=>{const [a,b]=this.ends[i],key=a<=b?a+':'+b:b+':'+a;
      const count=pairs.get(key)||0;pairs.set(key,count+1);return count===0?0:(count%2?1:-1)*Math.ceil(count/2)*9;});
    this.visibleNodes=this.nodes.map((_,i)=>i);this.visibleEdges=this.edges.map((_,i)=>i);
    this.riskNodes=new Set();this.edges.forEach((e,i)=>{if(e.state==='risk')this.ends[i].forEach(n=>this.riskNodes.add(n))});
    this.resize();this.fit();this.iteration=0;this.layoutDone=!this.queue.length;this.riskCount=this.edges.filter(e=>e.state==='risk').length;this.candidateCount=this.edges.filter(e=>e.candidates?.length).length;
    this.reportStatus();this.runLayout(this.generation);
  }
  stopWorkers() {
    for(const slot of this.workers||[]){clearTimeout(slot.timer);slot.worker.terminate()}
    this.workers=[];if(this.workerUrl){URL.revokeObjectURL(this.workerUrl);this.workerUrl=null}
  }
  runLayout(token) {
    if(this.paused||this.layoutDone||token!==this.generation)return;
    if(this.workers.length){for(const slot of this.workers)this.dispatch(slot,token);return}
    try {
      const code=layoutPartition.toString()+";onmessage=e=>{const results=e.data.map(layoutPartition);postMessage(results,results.map(r=>r.positions.buffer))}";
      this.workerUrl=URL.createObjectURL(new Blob([code],{type:'text/javascript'}));
      const size=Math.min(4,Math.max(1,(navigator.hardwareConcurrency||2)-1),this.queue.length);
      this.workerMode='workers';
      for(let i=0;i<size;i++){
        const slot={worker:new Worker(this.workerUrl),busy:false,jobs:[],timer:null};this.workers.push(slot);
        slot.worker.onmessage=e=>{if(token!==this.generation)return;clearTimeout(slot.timer);slot.busy=false;
          for(const result of e.data){const job=this.partition.jobs[result.id];
            if(result.ids.length!==job.ids.length||result.internalEdges!==job.links.length||result.ids.some((id,j)=>id!==job.ids[j])||!result.positions.every(Number.isFinite))throw Error('Partition merge identity mismatch');
            result.ids.forEach((id,j)=>{if(!this.positions[id].fixed){this.positions[id].x=job.cx+result.positions[2*j];this.positions[id].y=job.cy+result.positions[2*j+1]}});this.completedJobs++;}
          slot.jobs=[];this.partitionProgress();this.dispatch(slot,token);
        };
        slot.worker.onerror=()=>this.workerFailure(slot,token);
        this.dispatch(slot,token);
      }
    }catch(error){this.fallbackLayout(token)}
  }
  dispatch(slot,token) {
    if(slot.busy||this.paused||token!==this.generation||!this.queue.length)return;
    // Batch tiny modules to avoid hundreds of worker round trips.
    let nodes=0;slot.jobs=[];
    while(this.queue.length&&nodes<1000){const job=this.queue.shift();slot.jobs.push(job);nodes+=job.ids.length}
    slot.busy=true;slot.timer=setTimeout(()=>this.workerFailure(slot,token),5000);
    slot.worker.postMessage(slot.jobs.map(({id,ids,links})=>({id,ids,links})));
  }
  workerFailure(slot,token) {
    if(token!==this.generation||!this.workers.includes(slot))return;
    // Keep already-present nodes/edges and provisional coordinates for failed work.
    clearTimeout(slot.timer);slot.worker.terminate();this.failedJobs+=slot.jobs.length;this.completedJobs+=slot.jobs.length;
    slot.jobs=[];this.workers=this.workers.filter(s=>s!==slot);this.partitionProgress();
    if(!this.workers.length&&!this.layoutDone)this.fallbackLayout(token);
  }
  fallbackLayout(token) {
    this.workerMode='incremental fallback';
    const step=()=>{if(token!==this.generation||this.paused||this.layoutDone)return;
      const job=this.queue.shift();if(job){const result=layoutPartition(job);result.ids.forEach((id,j)=>Object.assign(this.positions[id],{x:job.cx+result.positions[j*2],y:job.cy+result.positions[j*2+1]}));this.completedJobs++;}
      this.partitionProgress();if(!this.layoutDone)setTimeout(step,0);
    };setTimeout(step,0);
  }
  partitionProgress() {
    this.layoutDone=this.completedJobs===this.partition.jobs.length;
    if(this.layoutDone){this.layoutMs=Math.round(performance.now()-this.layoutStarted);
      if(!this.failedJobs)this.layoutCache.set(this.graph,this.positions.map(p=>({...p})));this.stopWorkers();}
    // Counts update per batch; expensive full drawing is throttled during layout.
    if(!this.cameraTouched&&this.layoutDone)this.fit();
    if(this.layoutDone||performance.now()-(this.lastProgressDraw||0)>350){this.lastProgressDraw=performance.now();this.requestDraw()}
    this.reportStatus();
  }
  fit(indices=null) {
    const ids=indices?.length?indices:this.positions.map((_,i)=>i);
    let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
    for(const i of ids){const p=this.positions[i];minX=Math.min(minX,p.x);maxX=Math.max(maxX,p.x);minY=Math.min(minY,p.y);maxY=Math.max(maxY,p.y)}
    if(!ids.length){minX=minY=-50;maxX=maxY=50}
    this.camera={x:(minX+maxX)/2,y:(minY+maxY)/2,k:Math.min(4,Math.max(.005,Math.min((this.width-100)/Math.max(100,maxX-minX),(this.height-90)/Math.max(100,maxY-minY))))};
    this.requestDraw();
  }
  zoom(factor,x=this.width/2,y=this.height/2) {
    const before=this.world(x,y);this.camera.k=Math.max(.003,Math.min(50,this.camera.k*factor));
    const after=this.world(x,y);this.camera.x+=before.x-after.x;this.camera.y+=before.y-after.y;
    this.cameraTouched=true;this.requestDraw();
  }
  world(x,y){return {x:(x-this.width/2)/this.camera.k+this.camera.x,y:(y-this.height/2)/this.camera.k+this.camera.y}}
  screen(p){return {x:(p.x-this.camera.x)*this.camera.k+this.width/2,y:(p.y-this.camera.y)*this.camera.k+this.height/2}}
  filter(query='',mode='all') {
    const q=query.toLowerCase().trim();
    const matched=new Set();
    if(q)this.nodes.forEach((n,i)=>{if([n.id,n.label,n.path].join(' ').toLowerCase().includes(q))matched.add(i)});
    this.visibleEdges=[];const endpoints=new Set();
    this.edges.forEach((e,i)=>{const [a,b]=this.ends[i];if((mode==='all'||e.state===mode)&&(!q||matched.has(a)||matched.has(b)||[e.id,e.relation].join(' ').toLowerCase().includes(q))){this.visibleEdges.push(i);endpoints.add(a);endpoints.add(b)}});
    this.visibleNodes=this.nodes.map((_,i)=>i).filter(i=>!q&&mode==='all'||endpoints.has(i)||mode==='all'&&matched.has(i));
    this.edgePage=0;this.reportStatus();this.requestDraw();
  }
  reportStatus() {
    this.callbacks.onStatus?.({nodes:this.nodes.length,edges:this.edges.length,shownNodes:this.visibleNodes.length,shownEdges:this.visibleEdges.length,
      risks:this.riskCount,candidates:this.candidateCount,partitions:this.partition.jobs.length,completed:this.completedJobs,failed:this.failedJobs,workers:this.workers.length,workerMode:this.workerMode,internalEdges:this.internalEdges,crossEdges:this.partition.crossEdges.length,layoutMs:this.layoutMs,
      groups:this.groupNames.length,layout:this.layoutDone?'ready':this.paused?'paused':'arranging',iteration:this.iteration||0});
  }
  requestDraw(){if(this.frame!==null)return;this.frame=requestAnimationFrame(()=>{this.frame=null;this.draw()})}
  curve(i) {
    const [ai,bi]=this.ends[i],a=this.positions[ai],b=this.positions[bi],dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy)||1,o=this.offsets[i];
    return {a,b,c:{x:(a.x+b.x)/2-dy/len*o,y:(a.y+b.y)/2+dx/len*o},loop:ai===bi};
  }
  edgePath(ctx,i) {
    const {a,b,c,loop}=this.curve(i);
    ctx.moveTo(a.x,a.y);if(loop)ctx.bezierCurveTo(a.x+24,a.y-35,a.x-24,a.y-35,a.x,a.y);
    else if(this.offsets[i])ctx.quadraticCurveTo(c.x,c.y,b.x,b.y);else ctx.lineTo(b.x,b.y);
  }
  draw() {
    if(!this.ctx||!this.width)return;
    const c=this.ctx,k=this.camera.k;
    c.setTransform(this.dpr,0,0,this.dpr,0,0);c.clearRect(0,0,this.width,this.height);
    c.fillStyle='#fafbfc';c.fillRect(0,0,this.width,this.height);
    c.translate(this.width/2,this.height/2);c.scale(k,k);c.translate(-this.camera.x,-this.camera.y);
    const buckets={unknown:[],supported:[],review:[],risk:[],selected:[]};
    for(const i of this.visibleEdges){const e=this.edges[i];(buckets[e.state]||buckets.unknown).push(i)}
    const styles={unknown:['#8b9ba9',this.edges.length>10000?.12:.32,.65],supported:['#68867c',.45,.8],review:['#b78126',.65,1],risk:['#ce2435',.96,2.1]};
    // Every visible edge is submitted, with reviewed risks drawn last over context.
    let drawn=0;
    for(const state of ['unknown','supported','review','risk']){
      const [color,opacity,width]=styles[state];c.strokeStyle=color;c.lineWidth=width/k;c.globalAlpha=opacity;c.beginPath();
      for(const i of buckets[state]){this.edgePath(c,i);drawn++}c.stroke();
    }
    if(this.highlighted){c.strokeStyle='#206aba';c.globalAlpha=.8;c.lineWidth=1.5/k;c.beginPath();
      for(const i of this.visibleEdges){const [a,b]=this.ends[i];if(this.highlighted.has(a)&&this.highlighted.has(b)&&this.edges[i].state!=='risk')this.edgePath(c,i)}c.stroke();}
    // Direction arrows appear when readable; undirected links never gain arrows.
    if(k>.8){for(const i of this.visibleEdges){const e=this.edges[i];if(!e.directed)continue;const {a,b,c:cp,loop}=this.curve(i);if(loop)continue;
      const dx=b.x-cp.x,dy=b.y-cp.y,d=Math.hypot(dx,dy)||1,r=5/k,tip={x:b.x-dx/d*r,y:b.y-dy/d*r},s=3.5/k;
      c.globalAlpha=e.state==='risk'?1:.55;c.fillStyle=styles[e.state]?.[0]||styles.unknown[0];c.beginPath();c.moveTo(tip.x,tip.y);c.lineTo(tip.x-dx/d*s-dy/d*s*.6,tip.y-dy/d*s+dx/d*s*.6);c.lineTo(tip.x-dx/d*s+dy/d*s*.6,tip.y-dy/d*s-dx/d*s*.6);c.closePath();c.fill();}}
    c.globalAlpha=1;
    const nodeBuckets=this.palette.map(()=>[]);
    for(const i of this.visibleNodes)nodeBuckets[this.groupOf[i]%this.palette.length].push(i);
    for(let g=0;g<nodeBuckets.length;g++){c.fillStyle=this.palette[g];c.beginPath();for(const i of nodeBuckets[g]){const p=this.positions[i],r=this.radius(i)/k;c.moveTo(p.x+r,p.y);c.arc(p.x,p.y,r,0,Math.PI*2)}c.fill()}
    c.strokeStyle='#ce2435';c.lineWidth=1.4/k;c.beginPath();
    for(const i of this.visibleNodes){if(!this.riskNodes.has(i))continue;const p=this.positions[i],r=(this.radius(i)+2)/k;c.moveTo(p.x+r,p.y);c.arc(p.x,p.y,r,0,Math.PI*2)}c.stroke();
    if(this.selected?.type==='edge'){const i=this.selected.index;c.strokeStyle=this.edges[i].state==='risk'?'#a20f22':'#154f94';c.lineWidth=3.5/k;c.beginPath();this.edgePath(c,i);c.stroke()}
    const selectedNode=this.selected?.type==='node'?this.selected.index:null;
    if(selectedNode!==null){const p=this.positions[selectedNode];c.strokeStyle='#154f94';c.lineWidth=2/k;c.beginPath();c.arc(p.x,p.y,(this.radius(selectedNode)+4)/k,0,Math.PI*2);c.stroke()}
    c.setTransform(this.dpr,0,0,this.dpr,0,0);c.font='12px Segoe UI, Arial';c.textBaseline='middle';
    // Declutter labels only. No node/edge is dropped as the camera zooms.
    let labels=0;const labelIds=new Set(this.visibleNodes.filter(i=>k>=1.8||this.visibleNodes.length<=60||this.riskNodes.has(i)));
    if(selectedNode!==null)labelIds.add(selectedNode);
    for(const i of labelIds){const p=this.screen(this.positions[i]);if(p.x<0||p.x>this.width||p.y<0||p.y>this.height)continue;if(labels>=200&&i!==selectedNode)continue;
      const text=String(this.nodes[i].label).slice(0,65),x=p.x+this.radius(i)+5,w=c.measureText(text).width;
      c.fillStyle='rgba(250,251,252,.91)';c.fillRect(x-2,p.y-8,w+4,16);c.fillStyle=this.riskNodes.has(i)?'#9e1d2a':'#233443';c.fillText(text,x,p.y);labels++;
    }
    if(!this.visibleNodes.length){c.fillStyle='#59616b';c.fillText('No matching connections. Clear the filters to restore the complete network.',24,35)}
    this.canvas.dataset.drawnEdges=String(drawn);this.canvas.dataset.drawnNodes=String(this.visibleNodes.length);
    this.canvas.dataset.layout=this.layoutDone?'ready':'arranging';this.canvas.dataset.failedPartitions=String(this.failedJobs);
  }
  radius(i){return Math.min(5.5,Math.max(this.nodes.length>10000?1.4:2.6,1.6+Math.log2(1+this.degree[i])*.48))}
  pick(x,y) {
    let best=null,distance=10;
    for(const i of this.visibleNodes){const p=this.screen(this.positions[i]),d=Math.hypot(p.x-x,p.y-y);if(d<distance){best={type:'node',index:i};distance=d}}
    if(best)return best;
    distance=6;
    // Test the actual curves, including parallel relations and self loops.
    for(const i of this.visibleEdges){const curve=this.curve(i);let a=this.screen(curve.a);const steps=curve.loop?16:this.offsets[i]?8:1;
      for(let step=1;step<=steps;step++){const t=step/steps,u=1-t;let p;
        if(curve.loop){const q=curve.a;p={x:u*u*u*q.x+3*u*u*t*(q.x+24)+3*u*t*t*(q.x-24)+t*t*t*q.x,y:q.y-105*u*t};}
        else p={x:u*u*curve.a.x+2*u*t*curve.c.x+t*t*curve.b.x,y:u*u*curve.a.y+2*u*t*curve.c.y+t*t*curve.b.y};
        const b=this.screen(p),dx=b.x-a.x,dy=b.y-a.y,len=dx*dx+dy*dy;
        const f=len?Math.max(0,Math.min(1,((x-a.x)*dx+(y-a.y)*dy)/len)):0;
        const d=Math.hypot(x-a.x-f*dx,y-a.y-f*dy);if(d<distance){best={type:'edge',index:i};distance=d}a=b;
      }
    }
    return best;
  }
  select(hit) {this.selected=hit;this.requestDraw();if(!hit)return;
    if(hit.type==='node')this.callbacks.onNode(this.nodes[hit.index]);else this.callbacks.onEdge(this.edges[hit.index]);}
  focusEdge(id) {const i=this.edgeIndex.get(id);if(i===undefined)return;this.cameraTouched=true;this.fit(this.ends[i]);this.select({type:'edge',index:i})}
  bindPointer() {
    const pos=e=>{const r=this.canvas.getBoundingClientRect();return {x:e.clientX-r.left,y:e.clientY-r.top}};
    this.canvas.onpointerdown=e=>{const p=pos(e),hit=this.pick(p.x,p.y);this.drag={start:p,last:p,node:hit?.type==='node'?hit.index:null,hit,moved:false};this.canvas.setPointerCapture(e.pointerId)};
    this.canvas.onpointermove=e=>{if(!this.drag)return;const p=pos(e),d=this.drag;d.moved ||= Math.hypot(p.x-d.start.x,p.y-d.start.y)>4;
      if(d.moved){this.cameraTouched=true;if(d.node!==null){const q=this.world(p.x,p.y);Object.assign(this.positions[d.node],q,{vx:0,vy:0,fixed:true})}else{this.camera.x-=(p.x-d.last.x)/this.camera.k;this.camera.y-=(p.y-d.last.y)/this.camera.k}this.requestDraw()}d.last=p;};
    this.canvas.onpointerup=e=>{if(!this.drag)return;const d=this.drag;this.drag=null;if(!d.moved)this.select(d.hit);this.canvas.releasePointerCapture(e.pointerId)};
    this.canvas.onpointercancel=()=>{this.drag=null};
    this.canvas.onwheel=e=>{e.preventDefault();const p=pos(e);this.zoom(Math.exp(-e.deltaY*.0015),p.x,p.y)};
    this.canvas.onkeydown=e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','0'].includes(e.key))e.preventDefault();
      if(e.key==='+')this.zoom(1.3);else if(e.key==='-')this.zoom(1/1.3);else if(e.key==='0'){this.cameraTouched=true;this.fit()}
      else if(e.key.startsWith('Arrow')){this.cameraTouched=true;this.camera.x+=(e.key==='ArrowLeft'?-60:e.key==='ArrowRight'?60:0)/this.camera.k;this.camera.y+=(e.key==='ArrowUp'?-60:e.key==='ArrowDown'?60:0)/this.camera.k;this.requestDraw();}};
  }
}

let network=null, networkGraph=null;
const sourceGraph={nodes:D.source_nodes,edges:D.source_edges};
const processGraph={nodes:D.process_nodes,edges:D.handoffs};
function drawNetwork() {
  if(!network)return;
  const graph=$('map-kind').value==='source'?sourceGraph:processGraph;
  if(networkGraph!==graph){networkGraph=graph;network.setGraph(graph);}
  network.filter($('search').value,$('filter').value);
  $('map-title').textContent=$('map-kind').value==='source'?'Complete source network':'All declared handoffs';
  $('graph-note').textContent='Every supplied node and connection is loaded. Colors identify source groups; red lines mark reviewed risk or assessed gaps. Scroll to zoom, drag the background to pan, or drag a node. Extraction coverage remains separate.';
  renderConnectionList();
}
function renderConnectionList() {
  const list=$('edge-list');list.replaceChildren();if(!network)return;
  const size=80,start=network.edgePage*size,indices=network.visibleEdges.slice(start,start+size);
  for(const i of indices){const e=network.edges[i],a=network.nodes[network.ends[i][0]],b=network.nodes[network.ends[i][1]];
    const button=el('button',`${a.label} ${e.directed?'→':'↔'} ${b.label} · ${e.relation}`);
    button.title=e.id;button.onclick=()=>network.focusEdge(e.id);list.append(button);}
  $('edge-page').textContent=network.visibleEdges.length?`${start+1}–${Math.min(start+size,network.visibleEdges.length)} of ${network.visibleEdges.length.toLocaleString()} connections`:'No matching connections';
  $('edge-prev').disabled=network.edgePage===0;$('edge-next').disabled=start+size>=network.visibleEdges.length;
}
function highlight(seed) {
  const index=network.index.get(seed);if(index===undefined)return;
  const seen=new Set([index]);let front=[index];
  for(let depth=0;depth<2;depth++){const next=[];for(const i of front)for(const ei of network.neighbors[i]){
    const [a,b]=network.ends[ei],e=network.edges[ei];const other=i===a?b:!e.directed?a:null;
    if(other!==null&&!seen.has(other)){seen.add(other);next.push(other)}}front=next;}
  network.highlighted=seen;network.requestDraw();
  $('path-status').textContent=`${seen.size.toLocaleString()} related nodes within 2 hops highlighted. The complete network stays visible; these are investigation paths, not proven failure propagation.`;
}
function initializeNetwork() {
  network=new AuditNetwork($('network'),{onNode:inspectNode,onEdge:inspectEdge,onStatus:s=>{
    $('map-count').textContent=`${s.shownNodes.toLocaleString()} / ${s.nodes.toLocaleString()} nodes · ${s.shownEdges.toLocaleString()} / ${s.edges.toLocaleString()} connections · ${s.risks.toLocaleString()} risk links · ${s.candidates.toLocaleString()} candidate links`;
    $('layout-state').textContent=s.layout==='ready'?`Merged ${s.completed}/${s.partitions} partitions · ${s.crossEdges.toLocaleString()} cross-partition links${s.failed?' · '+s.failed+' provisional partitions':''}`:s.layout==='paused'?`Paused · ${s.completed}/${s.partitions} partitions`:`${s.workers} workers · ${s.completed}/${s.partitions} partitions ready`;
    $('next-risk').disabled=s.risks===0;
    $('pause-layout').disabled=s.layout==='ready';
    $('pause-layout').textContent=s.layout==='ready'?'Layout complete':s.layout==='paused'?'Resume layout':'Pause layout';
  }});
  $('map-kind').value=D.source_nodes.length?'source':'process';
  $('map-kind').onchange=()=>{networkGraph=null;$('path-status').textContent='';drawNetwork();};
  $('reset').onclick=()=>{$('search').value='';$('filter').value='all';network.highlighted=null;network.selected=null;network.cameraTouched=true;drawNetwork();network.fit();$('path-status').textContent='Complete network restored.'};
  $('zoom-in').onclick=()=>network.zoom(1.35);$('zoom-out').onclick=()=>network.zoom(1/1.35);
  $('pause-layout').onclick=()=>{network.paused=!network.paused;$('pause-layout').textContent=network.paused?'Resume layout':'Pause layout';network.reportStatus();if(!network.paused)network.runLayout(network.generation)};
  let riskCursor=-1;
  $('next-risk').onclick=()=>{const risks=network.edges.filter(e=>e.state==='risk');if(!risks.length)return;riskCursor=(riskCursor+1)%risks.length;$('search').value='';$('filter').value='all';drawNetwork();network.focusEdge(risks[riskCursor].id)};
  $('edge-prev').onclick=()=>{network.edgePage--;renderConnectionList()};$('edge-next').onclick=()=>{network.edgePage++;renderConnectionList()};
  $('expand-network').onclick=()=>{document.body.classList.toggle('expanded-network');$('expand-network').textContent=document.body.classList.contains('expanded-network')?'Exit expanded view':'Expand network';};
  show('connections');
}
