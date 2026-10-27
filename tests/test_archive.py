import unittest
from archive import Archive, load_records, REQUIRED, ENDING

class RetrievalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.a=Archive()
 def test_exact_source_preserved(self):
  originals={r['id']:r for r in load_records()}
  for hit in self.a.search('Why was the amber lantern kept burning?')['hits']:
   self.assertEqual(hit['text'], originals[hit['id']]['text'])
 def test_reject_invalid_questions(self):
  for q in ['', ' '*20, 17, 'x'*513, '\x00hello']:
   with self.assertRaises(ValueError):self.a.search(q)
 def test_order_stable(self):
  self.assertEqual(self.a.search('What rang at midnight?'),self.a.search('What rang at midnight?'))
 def test_ending_requires_sources(self):
  self.assertFalse(self.a.ending(['pipe','battery','portrait'])['unlocked'])
  self.assertFalse(self.a.ending(['light','bell'])['unlocked'])
  self.assertEqual(self.a.ending(list(REQUIRED))['text'],ENDING)
 def test_invalid_evidence(self):
  for ids in [['unknown'],[False],{},['bell']*20]:
   with self.assertRaises(ValueError):self.a.ending(ids)
 def test_ending_citations(self):
  r=self.a.ending(list(REQUIRED));self.assertEqual({x['id'] for x in r['sources']},REQUIRED)
 def test_read_only_archive(self):
  from archive import ROOT
  before=(ROOT/'archive.json').read_bytes();self.a.search('Who kept the light?');self.a.ending(list(REQUIRED))
  self.assertEqual(before,(ROOT/'archive.json').read_bytes())
if __name__=='__main__':unittest.main()
