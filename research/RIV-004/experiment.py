"""RIV-004 matched SQLite comparison; synthetic trusted callbacks only."""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory

OAP = 'b535850af64a460f96edfbcf56fa40df0d5ff974'
VER = 'bfb6af94984ddda87133bd76bbcce2b28d10f485'
OAP_BLOB = '78259b22c9b804da5c803290bd1e4b6eec855da5'
VER_BLOB = 'b477e4aed0bfe81878e83cb732ef62cc26fbc188'
INITIAL = [('neighbor',0,'clean'),('target',0,'old')]
EXPECTED = [('neighbor',0,'clean'),('target',1,'new')]
QUERY = 'SELECT resource,revision,value FROM resource_state ORDER BY resource'
CASES = [
    ('clean',[('target','new')]), ('lost_ack',[('target','new')]),
    ('no_effect',[]), ('wrong_value',[('target','wrong')]),
    ('collateral_persistent',[('target','new'),('neighbor','dirty')]),
    ('collateral_restored',[('target','new'),('neighbor','dirty'),('neighbor','clean')]),
    ('duplicate',[('target','new'),('target','new')]),
    ('transient_wrong',[('target','wrong'),('target','new')]),
    ('collateral_reset',[('target','new'),('neighbor','dirty'),('neighbor','clean'),('reset','neighbor')]),
    ('duplicate_reset',[('target','new'),('target','new'),('reset','target')]),
    ('precondition_mismatch',[('target','new')]),
    ('outside_scope',[('target','new'),('other','changed')]),
]


def pinned(root, commit, path, blob):
    head = subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    data = (root/path).read_bytes()
    digest = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if head != commit or digest != blob:
        raise ValueError('pinned implementation mismatch')
    if subprocess.check_output(['git','-C',str(root),'status','--porcelain','--untracked-files=all']):
        raise ValueError('checkout is not clean')


def fixture(root, name, events):
    db = root/'fixture.db'
    with closing(sqlite3.connect(db)) as con:
        con.execute('CREATE TABLE resource_state(resource TEXT PRIMARY KEY, revision INTEGER, value TEXT)')
        con.executemany('INSERT INTO resource_state VALUES (?,?,?)', INITIAL)
        con.execute('CREATE TABLE outside_scope(value TEXT)')
        con.execute("INSERT INTO outside_scope VALUES ('clean')")
        if name == 'precondition_mismatch':
            con.execute("UPDATE resource_state SET value='dirty' WHERE resource='neighbor'")
        con.commit()
    journal=[]
    def actor():
        with closing(sqlite3.connect(db)) as con:
            for target,value in events:
                if target == 'reset':
                    con.execute('UPDATE resource_state SET revision=? WHERE resource=?',(int(value=='target'),value))
                elif target == 'other':
                    con.execute('UPDATE outside_scope SET value=?',(value,))
                else:
                    con.execute('UPDATE resource_state SET revision=revision+1,value=? WHERE resource=?',(value,target))
                con.commit()
                journal.append((target,value))
        if name == 'lost_ack':
            raise RuntimeError('synthetic acknowledgement loss')
    return db,journal,actor


def inspect(db):
    with closing(sqlite3.connect(db)) as con:
        return con.execute(QUERY).fetchall(), con.execute('SELECT value FROM outside_scope').fetchone()[0]


def invoke(actor):
    try:
        actor()
        return 'RETURNED'
    except RuntimeError:
        return 'RAISED'


def classify(verdict, mapping):
    if verdict not in mapping:
        raise ValueError(f'unrecognized verdict: {verdict}')
    return mapping[verdict]


def run(oap=None, probe=None):
    methods=['fixture_reference'] if oap is None else ['oap_scope','verieffect_exact','verieffect_target']
    rows=[]
    for name,events in CASES:
        truth=name in ('clean','lost_ack')
        for method in methods:
            with TemporaryDirectory() as tmp:
                root=Path(tmp);db,journal,actor=fixture(root,name,events)
                initial,_=inspect(db)
                if method=='oap_scope':
                    verify,guard=oap
                    result=verify(database=db,guard=guard(root/'replay.db',initialize=True),key=b'\x01'*32,task_id='riv004',observer_id='fixture',initial={r:(v,x) for r,v,x in INITIAL},target='target',desired='new',actor=actor,window_seconds=0.5)
                    verdict,status=result.verdict,result.actor_status
                    decision=classify(verdict,{'STATE_MATCHED_UNATTRIBUTED':True,'STATE_MISMATCH':False,'PRECONDITION_MISMATCH':False,'STATE_PREEXISTING':False,'INDETERMINATE':None})
                elif method=='verieffect_exact':
                    _,before=probe(str(db),{'query':QUERY,'rows':[list(x) for x in INITIAL]})
                    if before!='PASS':
                        status='NOT_INVOKED';verdict=before
                    else:
                        status=invoke(actor)
                        _,verdict=probe(str(db),{'query':QUERY,'rows':[list(x) for x in EXPECTED]})
                    decision=classify(verdict,{'PASS':True,'FAIL':False,'UNVERIFIABLE':None})
                elif method=='verieffect_target':
                    status=invoke(actor)
                    _,verdict=probe(str(db),{'query':"SELECT value FROM resource_state WHERE resource='target'",'rows':[['new']]})
                    decision=classify(verdict,{'PASS':True,'FAIL':False,'UNVERIFIABLE':None})
                else:
                    status='NOT_INVOKED' if initial!=INITIAL else invoke(actor)
                    decision=initial==INITIAL and inspect(db)[0]==EXPECTED
                    verdict='REFERENCE_ONLY'
                final,outside=inspect(db)
                assert journal==(events if status!='NOT_INVOKED' else [])
                assert truth==(initial==INITIAL and journal==[('target','new')])
                rows.append(dict(case=name,method=method,truth=truth,decision=decision,verdict=verdict,actor_status=status,journal=journal,initial=initial,final=final,outside=outside))
    metrics={}
    for method in methods:
        c=dict(tp=0,fp=0,tn=0,fn=0,ap=0,an=0)
        for row in (r for r in rows if r['method']==method):
            t,d=row['truth'],row['decision'];c[('ap' if t else 'an') if d is None else ('tp' if t else 'fp') if d else ('fn' if t else 'tn')]+=1
        assert sum(c.values())==len(CASES)
        metrics[method]={**c,'false_acceptance':c['fp']/10,'valid_acceptance':c['tp']/2,'coverage':(c['tp']+c['fp']+c['tn']+c['fn'])/12}
    return {'mode':'fixtures_only' if oap is None else 'actual_implementations','oap_commit':OAP,'verieffect_commit':VER,'metrics':metrics,'rows':rows}


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixtures-only',action='store_true');p.add_argument('--oap',type=Path);p.add_argument('--verieffect',type=Path);args=p.parse_args()
    if args.fixtures_only:
        result=run()
    else:
        if not args.oap or not args.verieffect:
            p.error('supply --oap and --verieffect clean pinned checkouts')
        pinned(args.oap,OAP,'src/openactionproof/scope.py',OAP_BLOB)
        pinned(args.verieffect,VER,'verieffect/probes.py',VER_BLOB)
        sys.dont_write_bytecode=True
        sys.path[:0]=[str(args.oap.resolve()/'src'),str(args.verieffect.resolve())]
        from openactionproof.scope import verify_scoped_write
        from openactionproof.durable_replay import DurableReplayGuard
        from verieffect.probes import probe_db_row_matches
        result=run((verify_scoped_write,DurableReplayGuard),probe_db_row_matches)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
