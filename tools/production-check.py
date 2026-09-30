#!/usr/bin/env python3
"""Compare live production bytes and security headers with an explicit source commit."""
import argparse, datetime, hashlib, json, subprocess, urllib.request
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--url', required=True)
p.add_argument('--commit', required=True)
p.add_argument('--deploy-id', required=True)
p.add_argument('--output', default='release-results/production.json')
a = p.parse_args()
if not a.url.startswith('https://'):
    p.error('Production URL must use HTTPS')
source = subprocess.check_output(['git', 'show', a.commit + ':index.html'])
config = subprocess.check_output(['git', 'show', a.commit + ':netlify.toml']).decode()
import tomllib
expected_headers = tomllib.loads(config)['headers'][0]['values']
report = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              requested_url=a.url, commit=a.commit, deploy_id=a.deploy_id,
              deploy_id_evidence='operator-supplied; independently confirm in host',
              expected_sha256=hashlib.sha256(source).hexdigest())
try:
    request = urllib.request.Request(a.url, headers={'Cache-Control': 'no-cache', 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        report.update(final_url=response.url, status=response.status,
                      actual_sha256=hashlib.sha256(body).hexdigest(),
                      exact_source_match=body == source,
                      headers={name: dict(expected=value, actual=response.headers.get(name),
                                          match=response.headers.get(name) == value)
                               for name, value in expected_headers.items()})
    report['pass'] = report['exact_source_match'] and all(h['match'] for h in report['headers'].values())
except Exception as error:
    report.update(error=str(error), **{'pass': False})
target = Path(a.output)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['pass'] else 1)
