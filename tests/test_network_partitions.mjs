import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const context=vm.createContext({});
vm.runInContext(readFileSync('skills/software-process-audit/scripts/assets/layout-worker.js','utf8'),context);
const groups=Array.from({length:1400},(_,i)=>i<1300?0:1);
const edges=Array.from({length:1399},(_,i)=>[i,i+1]);
edges.push([0,0],[0,1],[1,0],[1399,0]);
const {jobs,crossEdges,owner}=context.partitionNetwork(groups,edges);
assert.equal(jobs.length,4);assert.ok(jobs.every(j=>j.ids.length<=600));
const nodes=jobs.flatMap(j=>j.ids),assigned=jobs.flatMap(j=>j.edgeIds).concat(crossEdges);
assert.equal(new Set(nodes).size,groups.length);assert.equal(nodes.length,groups.length);
assert.equal(new Set(assigned).size,edges.length);assert.equal(assigned.length,edges.length);
for(const i of crossEdges)assert.notEqual(owner[edges[i][0]],owner[edges[i][1]]);
const merged=new Map();
// Deliberately reverse completion order; stable IDs must reconcile unchanged.
for(const job of [...jobs].reverse()){const result=context.layoutPartition(job);
  assert.equal(result.internalEdges,job.links.length);assert.equal(result.positions.length,job.ids.length*2);
  assert.ok(Array.from(result.positions).every(Number.isFinite));
  result.ids.forEach((id,i)=>merged.set(id,[result.positions[i*2],result.positions[i*2+1]]));}
assert.equal(merged.size,groups.length);
const empty=context.partitionNetwork([],[]);assert.equal(empty.jobs.length,0);
const isolated=context.partitionNetwork([0,1,2],[]);assert.equal(isolated.jobs.flatMap(j=>j.ids).length,3);
console.log('Partition checks passed: bounded jobs, unique node ownership, internal/cross-edge conservation, parallel/self edges, reversed merge, empty/isolated nodes.');
