/* Pure per-partition layout. The worker sees coordinates and topology, not source text. */
function layoutPartition(job) {
  const n=job.ids.length,p=new Float64Array(n*2),v=new Float64Array(n*2),degree=new Uint32Array(n);
  const golden=Math.PI*(3-Math.sqrt(5));
  for(let i=0;i<n;i++){const r=14*Math.sqrt(i);p[i*2]=Math.cos(i*golden)*r;p[i*2+1]=Math.sin(i*golden)*r;}
  for(const [a,b]of job.links){degree[a]++;degree[b]++;}
  // Bounded local work; inter-partition edges are merged by the coordinator.
  for(let iteration=0;iteration<20;iteration++){
    const grid=new Map(),cell=30,alpha=1-iteration/28;
    for(let i=0;i<n;i++){const key=Math.floor(p[2*i]/cell)+','+Math.floor(p[2*i+1]/cell);if(!grid.has(key))grid.set(key,[]);grid.get(key).push(i)}
    for(let i=0;i<n;i++){
      const x=p[2*i],y=p[2*i+1],cx=Math.floor(x/cell),cy=Math.floor(y/cell);
      for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++){
        const bucket=grid.get((cx+dx)+','+(cy+dy))||[];
        const stride=Math.max(1,Math.ceil(bucket.length/24));
        for(let j=0;j<bucket.length;j+=stride){const other=bucket[j];if(i===other)continue;
          const px=x-p[2*other]||.01,py=y-p[2*other+1]||.01,d=px*px+py*py,f=Math.min(2,65/d)*alpha*.035;
          v[2*i]+=px*f;v[2*i+1]+=py*f;}
      }
    }
    for(const [a,b]of job.links){if(a===b)continue;const dx=p[2*b]-p[2*a],dy=p[2*b+1]-p[2*a+1],d=Math.hypot(dx,dy)||1;
      const f=(d-25)/d*.045*alpha/Math.sqrt(Math.max(degree[a],degree[b],1));v[2*a]+=dx*f;v[2*a+1]+=dy*f;v[2*b]-=dx*f;v[2*b+1]-=dy*f;}
    for(let i=0;i<p.length;i++){v[i]*=.6;p[i]+=Math.max(-7,Math.min(7,v[i]));}
  }
  return {id:job.id,ids:job.ids,positions:p,internalEdges:job.links.length};
}

function partitionNetwork(groupOf,ends,maxNodes=600) {
  const groups=new Map(),jobs=[],owner=new Int32Array(groupOf.length),local=new Int32Array(groupOf.length);
  for(let i=0;i<groupOf.length;i++){const g=groupOf[i];if(!groups.has(g))groups.set(g,[]);groups.get(g).push(i)}
  for(const [group,ids]of groups)for(let start=0;start<ids.length;start+=maxNodes){
    const part=ids.slice(start,start+maxNodes),id=jobs.length;
    part.forEach((i,j)=>{owner[i]=id;local[i]=j});jobs.push({id,group,ids:part,links:[],edgeIds:[]});
  }
  const crossEdges=[];
  ends.forEach(([a,b],i)=>{if(owner[a]===owner[b]){const job=jobs[owner[a]];job.links.push([local[a],local[b]]);job.edgeIds.push(i)}else crossEdges.push(i)});
  return {jobs,crossEdges,owner};
}
