"use strict";
function run(){
 const rows=[]; const methods=["first","majority","unanimity","domains","abstain"];
 const assert=(condition,msg)=>{if(!condition)throw Error(msg)};
 for(const truth of [0,1])for(const faultA of [0,1])for(const faultB of [0,1])for(const availableB of [0,1]){
  const a=truth^faultA,b=truth^faultB,reports=availableB?[a,a,b]:[a,a];
  const decisions={first:a,majority:Number(reports.reduce((s,v)=>s+v,0)>reports.length/2),unanimity:reports.every(v=>v===a)?a:null,domains:availableB&&a===b?a:null,abstain:null};
  rows.push({truth,faultA,faultB,availableB,reports,decisions});
 }
 const strata={primary:rows.filter(r=>r.faultA+r.faultB<=1),complete_primary:rows.filter(r=>r.faultA+r.faultB<=1&&r.availableB),missing_primary:rows.filter(r=>r.faultA+r.faultB<=1&&!r.availableB),two_fault:rows.filter(r=>r.faultA+r.faultB===2)};
 const summarize=(rs,m)=>{let tp=0,tn=0,fp=0,fn=0,ap=0,an=0;for(const r of rs){const d=r.decisions[m];if(d===null){if(r.truth)ap++;else an++}else if(d===1){if(r.truth)tp++;else fp++}else if(r.truth)fn++;else tn++}const n=tp+tn+fp+fn+ap+an,decisions=tp+tn+fp+fn;return {n,tp,tn,fp,fn,ap,an,coverage:decisions/n,false_accept_fraction:fp/(fp+tn+an),selective_error:decisions?(fp+fn)/decisions:null}};
 const metrics=Object.fromEntries(Object.entries(strata).map(([k,rs])=>[k,Object.fromEntries(methods.map(m=>[m,summarize(rs,m)]))]));
 assert(rows.length===16&&strata.primary.length===12&&strata.two_fault.length===4,"state counts");
 assert(metrics.primary.domains.fp===0&&metrics.primary.majority.fp>0,"H1");
 assert(metrics.primary.domains.coverage<metrics.primary.majority.coverage,"H2");
 assert(strata.two_fault.some(r=>r.availableB&&r.truth===0&&r.decisions.domains===1),"H3");
 assert(strata.complete_primary.every(r=>r.decisions.domains===r.decisions.unanimity),"H4");
 assert(metrics.primary.abstain.coverage===0&&metrics.primary.abstain.selective_error===null,"negative control");
 assert(strata.primary.filter(r=>!r.faultA&&!r.faultB&&r.availableB).every(r=>r.decisions.domains===r.truth),"clean control");
 return {experiment:"RIV-001",version:1,metrics,rows,assertions:"7 passed"};
}
console.log(JSON.stringify(run(), null, 2));
