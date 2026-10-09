#!/usr/bin/env python3
"""Fail-closed RWAL evidence gate; standard library only."""
import argparse, hashlib, json, pathlib, sys
REQUIREMENTS = {
 'ci_head': ('P0','GitHub Actions completed successfully on exact PR head'),
 'local_acceptance': ('P1','Local 24-traversal acceptance evidence tied to source SHA'),
 'deploy_mapping': ('P0','Netlify deploy ID maps to exact candidate commit'),
 'staging_identity': ('P0','Staging HTML checksum equals candidate checksum'),
 'staging_workflows': ('P0','Staging workflow acceptance passed'),
 'production_identity': ('P0','Production HTML checksum equals candidate checksum'),
 'production_headers': ('P0','Production security headers match approved policy'),
 'production_workflows': ('P0','Production workflow acceptance passed'),
 'manual_focus': ('P1','Manual keyboard focus review passed'),
 'manual_swipe': ('P1','Manual swipe review passed'),
 'manual_clipping': ('P1','Circular viewport clipping review passed'),
 'physical_device': ('P1','Physical device review passed'),
}
VALID={'PASS','FAIL','UNKNOWN','BLOCKED'}
def evaluate(e):
    head=e.get('head_sha'); entries=e.get('evidence',{}); defects=[]; checks={}
    for key,(severity,description) in REQUIREMENTS.items():
        item=entries.get(key) or {}; status=item.get('status','UNKNOWN')
        if status not in VALID: status='FAIL'
        reference=item.get('reference'); sha=item.get('head_sha')
        if status=='PASS' and (not isinstance(reference,str) or not reference.strip() or not head or sha!=head):
            status='FAIL'; reason='PASS evidence lacks reference or exact head SHA'
        else: reason=description
        checks[key]=status
        if status!='PASS':
            defects.append({'id':'RWAL-'+key.upper().replace('_','-'),'severity':severity,'status':status,'reason':reason,'required_evidence':description,'reference':reference or None})
    for i,claim in enumerate(e.get('claims',[])):
        if claim.get('type') in ('release_ready','deployed','merged') and claim.get('asserted') is True and any(v!='PASS' for v in checks.values()):
            defects.append({'id':f'RWAL-UNSUPPORTED-CLAIM-{i+1}','severity':'P0','status':'FAIL','reason':'Release/deployment/merge claim unsupported by complete gate evidence','required_evidence':'Independent current evidence for all mandatory release requirements','reference':None})
    defects.sort(key=lambda x:(x['severity'],x['id']))
    canonical=json.dumps({'head_sha':head,'checks':checks,'defects':defects},sort_keys=True,separators=(',',':')).encode()
    return {'schema':'rwal-gate/v1','head_sha':head,'decision':'PASS' if not defects else 'BLOCKED','checks':checks,'defects':defects,'ledger_sha256':hashlib.sha256(canonical).hexdigest()}
def main():
    p=argparse.ArgumentParser();p.add_argument('evidence');p.add_argument('--out',default='ledger.json');a=p.parse_args()
    data=json.loads(pathlib.Path(a.evidence).read_text()); result=evaluate(data)
    pathlib.Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(f"RWAL gate: {result['decision']} | {len(result['defects'])} findings | {result['ledger_sha256']}")
    return 0 if result['decision']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
