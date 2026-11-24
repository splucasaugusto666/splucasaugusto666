"""RIV-005: trusted complete-plan broker, not an arbitrary actor sandbox."""
import json
import sqlite3
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import closing

INITIAL = ([('neighbor', 0, 'clean'), ('target', 0, 'old')], 'clean')
EXPECTED = ([('neighbor', 0, 'clean'), ('target', 1, 'new')], 'clean')
CASES = [
    ('clean', [('target','new')]), ('lost_ack', [('target','new')]),
    ('no_effect', []), ('wrong_value', [('target','wrong')]),
    ('collateral_persistent', [('target','new'),('neighbor','dirty')]),
    ('collateral_restored', [('target','new'),('neighbor','dirty'),('neighbor','clean')]),
    ('duplicate', [('target','new'),('target','new')]),
    ('transient_wrong', [('target','wrong'),('target','new')]),
    ('collateral_reset', [('target','new'),('neighbor','dirty'),('neighbor','clean'),('reset','neighbor')]),
    ('duplicate_reset', [('target','new'),('target','new'),('reset','target')]),
    ('precondition_mismatch', [('target','new')]),
    ('outside_scope', [('target','new'),('other','changed')]),
]


def state(con):
    return (con.execute('SELECT resource,revision,value FROM resource_state ORDER BY resource').fetchall(),
            con.execute('SELECT value FROM outside_scope').fetchone()[0])


def setup(con, name):
    con.execute('CREATE TABLE resource_state(resource TEXT PRIMARY KEY, revision INTEGER, value TEXT)')
    con.executemany('INSERT INTO resource_state VALUES (?,?,?)', INITIAL[0])
    con.execute('CREATE TABLE outside_scope(value TEXT)')
    con.execute("INSERT INTO outside_scope VALUES ('clean')")
    if name == 'precondition_mismatch':
        con.execute("UPDATE resource_state SET value='dirty' WHERE resource='neighbor'")
    con.commit()


def apply(con, operation):
    target, value = operation
    if target == 'reset':
        con.execute('UPDATE resource_state SET revision=? WHERE resource=?', (int(value=='target'), value))
    elif target == 'other':
        con.execute('UPDATE outside_scope SET value=?', (value,))
    else:
        con.execute('UPDATE resource_state SET revision=revision+1,value=? WHERE resource=?', (value,target))


def allowed(plan):
    return (type(plan) is list and len(plan)==1 and type(plan[0]) is tuple and len(plan[0])==2
            and all(type(v) is str for v in plan[0]) and plan[0]==('target','new'))


def broker(con, plan, *, fail=False, lost_ack=False):
    if not allowed(plan):
        return 'REJECT', 0
    try:
        con.execute('BEGIN IMMEDIATE')
        if state(con)!=INITIAL:
            con.rollback()
            return 'REJECT', 0
        apply(con, ('target','new'))
        if fail:
            raise RuntimeError('injected before commit')
        if state(con)!=EXPECTED:
            con.rollback()
            return 'REJECT', 0
        con.commit()
    except (sqlite3.Error, RuntimeError):
        con.rollback()
        return 'ABSTAIN', 0
    if lost_ack and state(con)!=EXPECTED:
        return 'ABSTAIN', 1
    return 'ACCEPT', 1


def baseline(con, plan, *, lost_ack=False):
    if state(con)[0]!=INITIAL[0]:
        return 'REJECT', 0
    for op in plan:
        apply(con, op)
        con.commit()
    return ('ACCEPT' if state(con)[0]==EXPECTED[0] else 'REJECT'), len(plan)


def run():
    rows=[]
    with TemporaryDirectory() as tmp:
        counter=0
        def fresh(name):
            nonlocal counter
            counter+=1
            con=sqlite3.connect(Path(tmp)/f'{counter}.db')
            setup(con,name)
            return con
        for name,plan in CASES:
            for method,fn in [('baseline',baseline),('broker',broker)]:
                with closing(fresh(name)) as con:
                    initial=state(con)
                    verdict,committed=fn(con,plan,lost_ack=name=='lost_ack')
                    final=state(con)
                    truth=name in ('clean','lost_ack')
                    if method=='broker' and verdict=='REJECT':
                        assert committed==0 and final==initial
                    if truth:
                        assert final==EXPECTED
                    rows.append(dict(case=name,method=method,truth=truth,verdict=verdict,committed=committed,initial=initial,final=final))
        controls=[]
        for name,plan in [('empty_string',''),('wrong_arity',[('target',)]),('unknown_resource',[('other','new')]),('bool_value',[('target',True)])]:
            with closing(fresh(name)) as con:
                verdict,n=broker(con,plan)
                controls.append(dict(case=name,verdict=verdict,committed=n,unchanged=state(con)==INITIAL))
        with closing(fresh('rollback')) as con:
            verdict,n=broker(con,[('target','new')],fail=True)
            controls.append(dict(case='rollback',verdict=verdict,committed=n,unchanged=state(con)==INITIAL))
        for name,ops in [('bypass_outside',[('other','changed')]),('bypass_reset',[('neighbor','dirty'),('neighbor','clean'),('reset','neighbor')])]:
            with closing(fresh(name)) as con:
                verdict,n=broker(con,[('target','new')])
                for op in ops:
                    apply(con,op)
                    con.commit()
                controls.append(dict(case=name,broker_verdict=verdict,unmediated_commits=len(ops),scope_matches=state(con)[0]==EXPECTED[0],full_state_matches=state(con)==EXPECTED))
    metrics={}
    for method in ['baseline','broker']:
        a=[r for r in rows if r['method']==method]
        metrics[method]=dict(valid_accepted=sum(r['truth'] and r['verdict']=='ACCEPT' for r in a),invalid_accepted=sum(not r['truth'] and r['verdict']=='ACCEPT' for r in a),invalid_with_commits=sum(not r['truth'] and r['committed']>0 for r in a),abstentions=sum(r['verdict']=='ABSTAIN' for r in a))
    hypotheses=dict(H1=metrics['broker']==dict(valid_accepted=2,invalid_accepted=0,invalid_with_commits=0,abstentions=0),H2=metrics['baseline']['invalid_accepted']==3,H3=all(c['verdict']=='REJECT' and c['unchanged'] and c['committed']==0 for c in controls[:4]),H4=all(c['broker_verdict']=='ACCEPT' and c['unmediated_commits']>0 and c['scope_matches'] for c in controls[5:]),H5=controls[4]['verdict']=='ABSTAIN' and controls[4]['unchanged'] and controls[4]['committed']==0)
    return dict(rows=rows,controls=controls,metrics=metrics,hypotheses=hypotheses,python=sys.version.split()[0])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
