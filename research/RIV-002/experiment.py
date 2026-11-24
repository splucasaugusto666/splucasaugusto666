"""RIV-002: execute against pinned OpenActionProof core.py, stdlib only."""
import hashlib
import json
import platform
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

BLOB = 'f259b111ff5a2fd5a6102451c3adefd6058a8b54'
COMMIT = 'df7b22bbb81c8b1a102bc6fef1506c3d4f9704cc'
CASES = [
    ('clean', 'old', True, [('target','new')], False),
    ('false_claim', 'old', True, [], False),
    ('wrong_target', 'old', True, [('target','wrong')], False),
    ('preexisting', 'new', True, [], False),
    ('lost_ack_after_write', 'old', True, [('target','new')], True),
    ('no_effect_exception', 'old', True, [], True),
    ('collateral_persistent', 'old', True, [('target','new'),('neighbor','dirty')], False),
    ('collateral_restored', 'old', True, [('target','new'),('neighbor','dirty'),('neighbor','clean')], False),
    ('target_repeated', 'old', True, [('target','new'),('target','new')], False),
    ('target_transient_wrong', 'old', True, [('target','wrong'),('target','new')], False),
    ('clean_false_claim', 'old', False, [('target','new')], False),
    ('collateral_false_claim', 'old', False, [('target','new'),('neighbor','dirty')], False),
]


def run(source):
    data = source.read_bytes()
    if hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest() != BLOB:
        raise ValueError('Pinned source mismatch')
    # Execute only the reviewed, exact pinned source; no network access.
    import importlib.util
    spec = importlib.util.spec_from_file_location('riv002_oap_core', source)
    core = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = core
    spec.loader.exec_module(core)
    rows = []
    for name, initial, claim, events, timeout in CASES:
        with TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root/'target').write_bytes(initial.encode())
            (root/'neighbor').write_bytes(b'clean')
            journal = []
            def actor(_target):
                for path, value in events:
                    (root/path).write_bytes(value.encode())
                    journal.append((path,value))
                if timeout:
                    raise TimeoutError('synthetic acknowledgement loss')
            receipt = core.verify_action(root, core.ActionSpec(name,'target',b'new',claim), actor, operation_name=name)
            assert core.check_receipt(receipt)
            final = {p.name:p.read_bytes().decode() for p in root.iterdir()}
            expected_final = {'target':initial, 'neighbor':'clean'}
            expected_final.update(events)
            assert journal == events and final == expected_final
            truth = initial == 'old' and journal == [('target','new')]
            verdict = receipt['verification']['verdict']
            rows.append(dict(case=name,truth=truth,initial=initial,claim=claim,journal=journal,timeout=timeout,final=final,verdict=verdict,claim_only=claim,target_only=final['target']=='new',oap=verdict=='CONFIRMED',whole_snapshot=initial=='old' and final=={'target':'new','neighbor':'clean'}))
    metrics = {}
    for method in ('claim_only','target_only','oap','whole_snapshot'):
        tp,fp,tn,fn = (sum(r['truth']==t and r[method]==p for r in rows) for t,p in [(True,True),(False,True),(False,False),(True,False)])
        assert tp+fp+tn+fn == len(rows)
        metrics[method] = dict(tp=tp,fp=fp,tn=tn,fn=fn,acceptance=(tp+fp)/len(rows),false_acceptance=fp/(fp+tn))
    by = {r['case']:r for r in rows}
    hypotheses = dict(H1=not by['preexisting']['oap'] and by['preexisting']['target_only'] and not by['false_claim']['oap'] and not by['false_claim']['target_only'],H2=by['collateral_persistent']['oap'],H3=not by['collateral_persistent']['whole_snapshot'] and by['collateral_restored']['whole_snapshot'] and by['target_repeated']['whole_snapshot'],H4=by['lost_ack_after_write']['verdict']=='INDETERMINATE')
    return dict(commit=COMMIT,blob=BLOB,python=platform.python_version(),cases=len(rows),metrics=metrics,hypotheses=hypotheses,rows=rows)


if __name__ == '__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python experiment.py /path/to/pinned/core.py')
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
