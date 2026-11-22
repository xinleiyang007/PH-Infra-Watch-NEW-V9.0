import json, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collect_news_v9 import collect, categorize, canonical_url, extract_items

class CollectorTests(unittest.TestCase):
    def test_topic_and_url_normalization(self):
        self.assertIn('storage',categorize('Philippines battery energy storage project'))
        self.assertEqual('https://example.org/story',canonical_url('https://www.example.org/story?utm_source=abc'))
    def test_rss_parse(self):
        rss=b'<rss><channel><item><title>Philippines solar farm project approved</title><link>https://example.org/solar</link><description><![CDATA[New 50 MW plant announced]]></description><pubDate>Sat, 21 Nov 2026 03:00:00 GMT</pubDate></item></channel></rss>'
        entries=list(extract_items(rss))
        self.assertEqual(1,len(entries));self.assertTrue(entries[0]['published_at'].startswith('2026-11-21'))
    def test_two_feeds_deduplicated_and_company_data_untouched(self):
        with tempfile.TemporaryDirectory() as path:
            root=Path(path);(root/'config').mkdir();(root/'data').mkdir();(root/'fixtures').mkdir()
            sources=[{'id':'a','label':'Publisher A','publisher':'A','group':'media','method':'rss','feed_url':'https://example.org/a','home':'https://example.org'},
                     {'id':'b','label':'Publisher B','publisher':'B','group':'media','method':'google_news_search','query':'Philippines BESS','home':'https://example.org'}]
            cfg={'sources':sources,'retention_days':120,'max_records':100,'max_items_per_source':20}
            (root/'config/news_sources.json').write_text(json.dumps(cfg))
            story='New 50 MW solar farm project approved in Philippines'
            for source in sources:
                rss=f'<rss><channel><item><title>{story}</title><link>https://{source["id"]}.example.org/solar</link><description>Construction of renewable energy power plant</description><pubDate>Sat, 21 Nov 2026 03:00:00 GMT</pubDate></item></channel></rss>'
                (root/'fixtures'/(source['id']+'.xml')).write_text(rss)
            original='{"projects":[{"id":"approved"}]}'
            (root/'data/projects.json').write_text(original)
            rc=collect(root,root/'fixtures',now=datetime(2026,11,22,tzinfo=timezone.utc))
            self.assertEqual(0,rc)
            leads=json.loads((root/'data/media_leads.json').read_text())['leads']
            status=json.loads((root/'data/media_status.json').read_text())
            self.assertEqual(1,len(leads));self.assertEqual(2,len(leads[0]['coverage']))
            self.assertEqual('unverified_discovery',leads[0]['review_status'])
            self.assertEqual(2,status['successful_sources'])
            self.assertEqual(original,(root/'data/projects.json').read_text())

if __name__=='__main__':unittest.main()
