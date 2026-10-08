// Independent subset-weight formula (contract enumerates join-order permutations).
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=name=>JSON.parse(fs.readFileSync(path.join(root,'proofs',name+'.json')));
const canonical=v=>JSON.stringify(v,(_,x)=>x&&!Array.isArray(x)&&typeof x==='object'?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b))):x);
const same=(a,b)=>assert.equal(canonical(a),canonical(b));
const expected={additive:[0,6,12,18,18,24,30,36],shared:[0,10,10,14,10,14,14,18],unstable:[0,10,10,10,10,10,10,24],missing:[0,10,10,14,10,14,14,null],nonmonotone:[0,10,10,14,10,14,14,9]};
const m=read('deployment');
assert.equal(m.chain_id,61999);assert.equal(m.network,'studionet');assert.equal(m.exact_source_match,true);
assert.equal(m.source_sha256,hash(fs.readFileSync(path.join(root,'contracts/coalition_meter.py'))));
assert.equal(m.transactions.length,6);
let previous=[];
for(const [index,tx] of m.transactions.entries()){
 const r=read(tx.label+'-receipt');assert.equal(r.hash,tx.hash);
 assert.equal(r.status_name||r.statusName,'FINALIZED');assert.equal(r.result_name,'MAJORITY_AGREE');
 assert.ok(['SUCCESS','FINISHED_WITH_RETURN'].includes(r.txExecutionResultName||r.consensus_data?.leader_receipt?.[0]?.execution_result));
 assert.ok(Object.values(r.consensus_data.votes).filter(v=>v==='agree').length>=3);
 if(tx.action==='deploy')continue;
 assert.equal(tx.action,'allocate');assert.equal(r.to_address.toLowerCase(),m.contract_address.toLowerCase());
 const proof=read(tx.label),state=proof.state,batch=state.batches.at(-1),result=batch.result;
 assert.equal(proof.transaction.hash,tx.hash);assert.equal(proof.contract_address,m.contract_address);assert.equal(proof.source_sha256,m.source_sha256);
 assert.equal(state.source_repository,'gabrieladash123-bit/coalition-meter');same(state.members,['amber','cobalt','jade']);
 assert.equal(state.batches.length,index);same(state.batches.slice(0,-1),previous);previous=state.batches;
 const body=fs.readFileSync(path.join(root,'records',tx.label+'.json')),record=JSON.parse(body);
 same(batch.record,record);assert.equal(batch.sha256,hash(body));assert.equal(batch.sha256,m.sources[tx.label].sha256);
 assert.equal(batch.url,`https://raw.githubusercontent.com/gabrieladash123-bit/coalition-meter/${m.fixture_revision}/records/${tx.label}.json`);
 assert.ok(r.data.calldata.readable.includes(batch.url));assert.ok(r.data.calldata.readable.includes(batch.sha256));
 assert.equal(batch.report.coalitions.length,7);
 const costs=[0];
 for(const [i,c] of batch.report.coalitions.entries()){
  assert.equal(c.mask,i+1);assert.ok(record.tariff.includes(c.quote));assert.ok(c.quote.length>=12);
  assert.equal(c.decision,c.cost===null?'UNKNOWN':'KNOWN');costs.push(c.cost);
 }
 same(costs,expected[tx.label]);same(result.costs,costs);assert.equal(result.denominator,6);
 const unknown=costs.slice(1).flatMap((c,i)=>c===null?[i+1]:[]);same(result.unknown,unknown);
 if(unknown.length){assert.equal(result.status,'REVIEW');same(result.shares_numerator,[]);same(result.rounded_preview,[]);continue;}
 const bad=[];
 for(let a=0;a<8;a++)for(let b=0;b<8;b++)if(a!==b&&(a&b)===a&&costs[a]>costs[b])bad.push({subset:a,superset:b,decrease:costs[a]-costs[b]});
 same(result.monotonicity_violations,bad);
 if(bad.length){assert.equal(result.status,'INCONSISTENT');same(result.shares_numerator,[]);same(result.rounded_preview,[]);continue;}
 const shares=[0,1,2].map(i=>{
  const bit=1<<i,others=[0,1,2].filter(j=>j!==i).map(j=>1<<j),[x,y]=others;
  return 2*costs[bit]+(costs[bit|x]-costs[x])+(costs[bit|y]-costs[y])+2*(costs[7]-costs[x|y]);
 });
 same(result.shares_numerator,shares);assert.equal(shares.reduce((a,b)=>a+b,0),6*costs[7]);assert.ok(shares.every(n=>n>=0));
 const core=[];
 for(let mask=1;mask<7;mask++){
  const charge=shares.reduce((sum,n,i)=>sum+((mask&(1<<i))?n:0),0);
  if(charge>6*costs[mask])core.push({mask,charge_numerator:charge,standalone_numerator:6*costs[mask],excess_numerator:charge-6*costs[mask]});
 }
 same(result.core_violations,core);assert.equal(result.status,core.length?'UNSTABLE':'STABLE');
 const rounded=shares.map(n=>Math.floor(n/6)),residual=costs[7]-rounded.reduce((a,b)=>a+b,0);
 [0,1,2].sort((a,b)=>(shares[b]%6-shares[a]%6)||a-b).slice(0,residual).forEach(i=>rounded[i]++);
 same(result.rounded_preview,rounded);assert.equal(rounded.reduce((a,b)=>a+b,0),costs[7]);
 const roundedCore=[];
 for(let mask=1;mask<7;mask++){
  const charge=rounded.reduce((sum,n,i)=>sum+((mask&(1<<i))?n:0),0);
  if(charge>costs[mask])roundedCore.push({mask,charge,standalone:costs[mask]});
 }
 same(result.rounded_core_violations,roundedCore);
}
console.log('Verified 6 finalized receipts, source commitments, 35 coalition decisions, exact shares and all instability/domain witnesses.');
