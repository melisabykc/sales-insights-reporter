import tempfile,unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_revenue(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3';app.add('Book',2,10,'2026-10-27','Online',p);self.assertEqual(app.report(p)['total_revenue'],20)
if __name__=='__main__':unittest.main()
