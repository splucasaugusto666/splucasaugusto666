'use strict';
// Recompute published metrics from recorded rows; not independent experiment replication.
function audit(studies){
  let checks=0;const assert=(ok,msg)=>{checks++;if(!ok)throw Error(msg)};
  const counts=(rows,truth,decision)=>{const c={tp:0,tn:0,fp:0,fn:0,ap:0,an:0};for(const r of rows){const t=truth(r),d=decision(r);assert(typeof t==="boolean"&&(typeof d==="boolean"||d===null),"invalid truth or decision");c[d===null?(t?"ap":"an"):d?(t?"tp":"fp"):(t?"fn":"tn")]++}return c};
  const eq=(a,b,msg)=>assert(a===null||b===null?a===b:typeof a==="number"&&typeof b==="number"&&Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<1e-12,msg);
  const compare=(rows,truth,decision,stored,kind,ctx)=>{const c=counts(rows,truth,decision), n=rows.length,dec=c.tp+c.tn+c.fp+c.fn,neg=c.fp+c.tn+c.an;for(const k of Object.keys(c))if(kind!==2||!["ap","an"].includes(k))eq(c[k],stored[k],ctx+":"+k);if(kind===1){eq(n,stored.n,ctx+":n");eq(dec/n,stored.coverage,ctx+":coverage");eq(neg?c.fp/neg:null,stored.false_accept_fraction,ctx+":false_accept_fraction");eq(dec?(c.fp+c.fn)/dec:null,stored.selective_error,ctx+":selective_error")}if(kind===2){eq((c.tp+c.fp)/n,stored.acceptance,ctx+":acceptance");eq(c.fp/neg,stored.false_acceptance,ctx+":false_acceptance")}if(kind===3){eq(c.fp/neg,stored.false_accept,ctx+":false_accept");eq(c.tp/(c.tp+c.fn+c.ap),stored.true_accept,ctx+":true_accept");eq(dec/n,stored.coverage,ctx+":coverage");eq(50*c.tn/neg+30*c.tp/(c.tp+c.fn+c.ap)+20*dec/n,stored.score,ctx+":score")}return c};
  const result={}; const a=studies["RIV-001"],b=studies["RIV-002"],c=studies["RIV-003"];
  assert(a.rows.length===16,"RIV-001 row count");assert(new Set(a.rows.map(r=>JSON.stringify([r.truth,r.faultA,r.faultB,r.availableB]))).size===16,"RIV-001 unique states");
  for(const r of a.rows)for(const k of ["truth","faultA","faultB","availableB"])assert(r[k]===0||r[k]===1,"RIV-001 binary state");
  const strata={primary:r=>r.faultA+r.faultB<=1,complete_primary:r=>r.faultA+r.faultB<=1&&r.availableB===1,missing_primary:r=>r.faultA+r.faultB<=1&&r.availableB===0,two_fault:r=>r.faultA+r.faultB===2};
  for(const [s,f] of Object.entries(strata))for(const m of ["first","majority","unanimity","domains","abstain"])compare(a.rows.filter(f),r=>!!r.truth,r=>{const d=r.decisions[m];assert(d===0||d===1||d===null,"RIV-001 invalid decision");return d===null?null:!!d},a.metrics[s][m],1,`RIV-001/${s}/${m}`);
  result["RIV-001"]={rows:a.rows.length,metric_groups:20};
  assert(b.cases===12&&b.rows.length===12&&new Set(b.rows.map(r=>r.case)).size===12,"RIV-002 cases");
  for(const r of b.rows){assert(r.truth===(r.initial==="old"&&JSON.stringify(r.journal)==='[["target","new"]]'),"RIV-002 truth mismatch");assert(r.oap===(r.verdict==="CONFIRMED"),"RIV-002 verdict mismatch")}
  for(const m of ["claim_only","target_only","oap","whole_snapshot"])compare(b.rows,r=>r.truth,r=>r[m],b.metrics[m],2,`RIV-002/${m}`);
  result["RIV-002"]={rows:b.rows.length,metric_groups:4};
  const regimes=["honest","reset_counters","missing_journal","both_fabricated"];assert(c.histories===341&&c.rows.length===1364&&JSON.stringify(c.regimes)===JSON.stringify(regimes),"RIV-003 count");
  for(const s of regimes){const rows=c.rows.filter(r=>r.regime===s);assert(rows.length===341&&new Set(rows.map(r=>JSON.stringify(r.events))).size===341,"RIV-003 unique histories");for(const r of rows){assert(Array.isArray(r.events)&&r.events.length<=4&&r.events.every(e=>["T0","T1","N0","N1"].includes(e)),"RIV-003 alphabet");assert(r.truth===(r.events.length===1&&r.events[0]==="T1"),"RIV-003 truth mismatch")}for(const m of ["target","snapshot","revision","journal"])compare(rows,r=>r.truth,r=>r.decision[m],c.metrics[s][m],3,`RIV-003/${s}/${m}`)}
  result["RIV-003"]={rows:c.rows.length,metric_groups:16};return {status:"PASS",studies:result,rows:1392,metric_groups:40,checks};
}
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const studies={};for(const id of ['RIV-001','RIV-002','RIV-003'])studies[id]=JSON.parse(fs.readFileSync(path.join(__dirname,id,'results.json'),'utf8'));const result=audit(studies);let rejected=0;for(const id of Object.keys(studies)){const bad=JSON.parse(JSON.stringify(studies));if(id==='RIV-001')bad[id].metrics.primary.first.fp++;if(id==='RIV-002')bad[id].metrics.oap.tp++;if(id==='RIV-003')bad[id].metrics.honest.revision.fp++;try{audit(bad)}catch{rejected++}}if(rejected!==3)throw Error('negative controls failed');console.log(JSON.stringify({...result,negative_controls_rejected:rejected},null,2))}
module.exports={audit};
