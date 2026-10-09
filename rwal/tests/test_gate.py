import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gate import evaluate, REQUIREMENTS
HEAD='a'*40
class GateTests(unittest.TestCase):
 def test_missing_evidence_blocks(self):
  self.assertEqual(evaluate({'head_sha':HEAD})['decision'],'BLOCKED')
 def test_unknown_preserved(self):
  self.assertEqual(evaluate({'head_sha':HEAD})['checks']['deploy_mapping'],'UNKNOWN')
 def test_valid_pass(self):
  e={'head_sha':HEAD,'evidence':{k:{'status':'PASS','head_sha':HEAD,'reference':'test:'+k} for k in REQUIREMENTS}}
  self.assertEqual(evaluate(e)['decision'],'PASS')
 def test_wrong_sha_fails(self):
  e={'head_sha':HEAD,'evidence':{'ci_head':{'status':'PASS','head_sha':'b'*40,'reference':'test'}}}
  self.assertEqual(evaluate(e)['checks']['ci_head'],'FAIL')
 def test_unsupported_claim(self):
  e={'head_sha':HEAD,'claims':[{'type':'deployed','asserted':True}]}
  self.assertTrue(any('UNSUPPORTED' in x['id'] for x in evaluate(e)['defects']))
 def test_deterministic(self):
  e={'head_sha':HEAD}
  self.assertEqual(evaluate(e)['ledger_sha256'],evaluate(e)['ledger_sha256'])
if __name__=='__main__':unittest.main()
