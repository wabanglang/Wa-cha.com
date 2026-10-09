#!/usr/bin/env python3
"""Read-only Netlify API collector. Does not mark release evidence PASS."""
import argparse, json, os, pathlib, sys, urllib.request, urllib.error
def collect(site_id, token, expected_sha):
    req=urllib.request.Request('https://api.netlify.com/api/v1/sites/'+site_id+'/deploys?per_page=20',headers={'Authorization':'Bearer '+token,'Accept':'application/json','User-Agent':'rwal-evidence-gate/0.1'})
    with urllib.request.urlopen(req,timeout=20) as response:
        deployments=json.load(response)
    records=[]
    for d in deployments:
        sha=d.get('commit_ref') or d.get('commit_sha')
        records.append({'id':d.get('id'),'state':d.get('state'),'commit_sha':sha,'context':d.get('context'),'created_at':d.get('created_at'),'published_at':d.get('published_at'),'matches_expected':sha==expected_sha if sha else None})
    return {'schema':'rwal-netlify-observation/v1','expected_sha':expected_sha,'site_id':site_id,'deployments':records,'release_authorized':False,'note':'Metadata only. No HTML, header or live workflow checks performed.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--site-id',default=os.getenv('NETLIFY_SITE_ID'));p.add_argument('--expected-sha',required=True);p.add_argument('--out',default='rwal/netlify-observation.json');a=p.parse_args()
    token=os.getenv('NETLIFY_AUTH_TOKEN')
    if not a.site_id or not token:
        print('BLOCKED: NETLIFY_SITE_ID and NETLIFY_AUTH_TOKEN are required',file=sys.stderr);return 2
    try: result=collect(a.site_id,token,a.expected_sha)
    except (urllib.error.URLError,ValueError,TimeoutError) as exc:
        print('BLOCKED: Netlify metadata unavailable: '+str(exc),file=sys.stderr);return 2
    path=pathlib.Path(a.out);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('Observed '+str(len(result['deployments']))+' deployments; release remains BLOCKED')
    return 0
if __name__=='__main__':sys.exit(main())
