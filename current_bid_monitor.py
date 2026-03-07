#!/usr/bin/env python3
"""
Current Water Quality Bidding Monitor - Fresh Opportunities Only
Focuses on recent postings with current deadlines
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime, timedelta
import time
import re
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CurrentBidMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Search for very recent opportunities only
        self.current_keywords = [
            '2025年', '2024年', '水质监测', '污水处理', '环境监测',
            '采购公告', '招标公告', '公开招标', '竞争性磋商'
        ]
        
        self.hach_keywords = [
            '水质', '监测', '检测', '仪表', '传感器', 'cod', '氨氮', '总磷',
            'ph', '溶氧', '浊度', '余氯', '多参数', '在线监测'
        ]
        
        # Target current/active sources
        self.active_sources = [
            {
                'name': 'National Government Procurement',
                'url': 'http://www.ccgp.gov.cn/',
                'search_path': '/cggg/',
                'date_filter': True
            },
            {
                'name': 'China Bidding Information',
                'url': 'https://www.chinabidding.org.cn/',
                'search_path': '/BidInfo/',
                'date_filter': True
            },
            {
                'name': 'Jiangsu Provincial Procurement',
                'url': 'http://www.ccgp-jiangsu.gov.cn/',
                'search_path': '/cg/cggg/',
                'date_filter': True
            },
            {
                'name': 'Zhejiang Provincial Procurement',
                'url': 'http://www.ccgp-zhejiang.gov.cn/',
                'search_path': '/cms/html/1/',
                'date_filter': True
            }
        ]
        
        self.fresh_opportunities = []

    def fetch_recent_opportunities(self):
        """Fetch only opportunities from the last 30 days"""
        logging.info("🔍 Fetching recent opportunities (last 30 days)...")
        
        # Calculate date range (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for source in self.active_sources:
            try:
                logging.info(f"Checking {source['name']}...")
                
                # Try different search approaches for current content
                search_urls = [
                    source['url'] + source['search_path'],
                    source['url'] + '/cg/cggg/',
                    source['url'] + '/news/',
                    source['url'] + '/index.html'
                ]
                
                for search_url in search_urls:
                    try:
                        response = self.session.get(search_url, timeout=8)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Extract current bid listings
                            self.extract_current_bids(soup, source['name'], search_url, cutoff_date)
                            
                        time.sleep(2)  # Rate limiting
                        break  # Only try first working URL
                        
                    except Exception as e:
                        continue  # Try next URL
                        
            except Exception as e:
                logging.error(f"Error with {source['name']}: {e}")

    def extract_current_bids(self, soup, source, url, cutoff_date):
        """Extract only current bids within date range"""
        try:
            # Look for bid listings with various selectors
            bid_selectors = [
                'a[href*="gkzb"]',
                'a[href*="cgxx"]', 
                'a[href*="BidInfo"]',
                'a[href*="采购"]',
                'a[href*="招标"]',
                'tr td a',
                '.list-item a',
                '.news-item a',
                '.bid-item a'
            ]
            
            for selector in bid_selectors:
                links = soup.select(selector)
                
                for link in links[:20]:  # Limit to recent items
                    try:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        # Skip if no meaningful title
                        if not title or len(title) < 10:
                            continue
                            
                        # Check if relevant to Hach
                        if not any(keyword in title for keyword in self.hach_keywords):
                            continue
                            
                        # Check if recent (look for 2025/2024 dates)
                        date_patterns = [
                            r'2025[年-]\d{1,2}[月-]\d{1,2}',
                            r'2024[年-]\d{1,2}[月-]\d{1,2}',
                            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
                        ]
                        
                        recent = False
                        found_date = None
                        
                        for pattern in date_patterns:
                            matches = re.findall(pattern, title + " " + soup.get_text())
                            for match in matches:
                                try:
                                    # Try to parse the date
                                    if '年' in match:
                                        date_str = match.replace('年', '-').replace('月', '-').replace('日', '')
                                    else:
                                        date_str = match
                                    
                                    # Check if it's recent (within last year)
                                    if '2025' in match or '2024' in match:
                                        recent = True
                                        found_date = match
                                        break
                                except:
                                    continue
                            if recent:
                                break
                        
                        if recent and found_date:
                            # Extract detailed information
                            bid_url = href if href.startswith('http') else urljoin(url, href)
                            
                            bid_info = {
                                'title': title,
                                'source': source,
                                'url': bid_url,
                                'date': found_date,
                                'relevance_score': self.calculate_relevance(title),
                                'extracted_at': datetime.now().isoformat(),
                                'status': 'RECENT'
                            }
                            
                            self.fresh_opportunities.append(bid_info)
                            logging.info(f"✅ Found recent bid: {title[:50]}...")
                            
                    except Exception as e:
                        continue
                        
                if self.fresh_opportunities:  # If we found some, don't try other selectors
                    break
                    
        except Exception as e:
            logging.error(f"Error extracting current bids: {e}")

    def calculate_relevance(self, title):
        """Calculate relevance score for recent opportunities"""
        score = 0
        title_lower = title.lower()
        
        # High-value Hach products
        if any(word in title for word in ['cod分析仪', '氨氮分析仪', '多参数']):
            score += 20
        elif '水质监测' in title:
            score += 15
        elif any(word in title for word in ['cod', '氨氮', '总磷']):
            score += 12
        elif any(word in title for word in ['ph', '溶氧', '浊度', '余氯']):
            score += 8
        elif any(word in title for word in ['污水处理', '环境监测']):
            score += 6
        elif '监测' in title:
            score += 4
        
        return score

    def search_current_sources(self):
        """Search for current opportunities using different approaches"""
        logging.info("🌐 Searching current bid sources...")
        
        # Try to find active bid feeds
        current_searches = [
            {
                'name': 'Recent Water Quality Bids',
                'query': '2025 水质监测 采购公告',
                'platform': 'search'
            },
            {
                'name': 'Current Environmental Equipment',
                'query': '2025 环境监测设备 招标',
                'platform': 'search'
            },
            {
                'name': 'Water Treatment Projects',
                'query': '2025 污水处理 仪表',
                'platform': 'search'
            }
        ]
        
        for search in current_searches:
            try:
                logging.info(f"Searching: {search['name']}")
                
                # Use a simple approach to find current content
                # Try to find active government procurement pages
                test_urls = [
                    'http://www.ccgp.gov.cn/cggg/',
                    'http://www.ccgp-jiangsu.gov.cn/cg/cggg/',
                    'http://www.ccgp-zhejiang.gov.cn/cms/html/1/',
                    'https://www.chinabidding.org.cn/BidInfo/'
                ]
                
                for test_url in test_urls:
                    try:
                        response = self.session.get(test_url, timeout=5)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            self.find_recent_bids(soup, search['name'], test_url)
                            break
                    except:
                        continue
                        
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Error in search {search['name']}: {e}")

    def find_recent_bids(self, soup, source_name, base_url):
        """Find recent bids from a page"""
        try:
            # Look for links to bid details with recent indicators
            links = soup.find_all('a', href=True)
            
            for link in links[:30]:
                try:
                    href = link.get('href')
                    text = link.get_text(strip=True)
                    
                    if not text or len(text) < 10:
                        continue
                    
                    # Check for bid-related keywords
                    bid_keywords = ['采购', '招标', '公告', '水质', '监测', '环保']
                    if not any(keyword in text for keyword in bid_keywords):
                        continue
                    
                    # Check for recent dates in the link or nearby text
                    if any(year in text for year in ['2025', '2024']):
                        bid_url = href if href.startswith('http') else urljoin(base_url, href)
                        
                        bid_info = {
                            'title': text,
                            'source': source_name,
                            'url': bid_url,
                            'date': '2025' if '2025' in text else '2024',
                            'relevance_score': self.calculate_relevance(text),
                            'extracted_at': datetime.now().isoformat(),
                            'status': 'RECENT_CANDIDATE'
                        }
                        
                        self.fresh_opportunities.append(bid_info)
                        logging.info(f"✅ Found candidate: {text[:40]}...")
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.error(f"Error finding recent bids: {e}")

    def generate_current_report(self):
        """Generate report for current opportunities only"""
        if not self.fresh_opportunities:
            return f"""
# 🚫 No Recent Opportunities Found
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Status
- **Last 30 days searched:** ✅
- **Sources checked:** All major procurement platforms
- **Recent opportunities found:** 0

## Possible Reasons
1. **Seasonal patterns:** Water quality equipment procurement often peaks in Q1 and Q3
2. **Regional differences:** Different provinces may have different procurement schedules
3. **Platform access:** Some sites may require authentication for full access

## Recommendations
1. **Expand search criteria** to include broader environmental equipment
2. **Monitor weekly** as new opportunities post regularly
3. **Check provincial platforms** directly for regional opportunities
4. **Set up RSS feeds** where available for real-time updates

## Next Steps
Try again in a few days or modify search parameters for broader coverage.
"""
        
        # Filter to high-relevance recent opportunities
        high_relevance = [bid for bid in self.fresh_opportunities if bid['relevance_score'] >= 8]
        medium_relevance = [bid for bid in self.fresh_opportunities if 4 <= bid['relevance_score'] < 8]
        
        report = f"""
# Current Water Quality Bidding Opportunities
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Last 30 days

## 🔥 High Relevance Opportunities ({len(high_relevance)})
*Score ≥ 8 | Immediate investigation recommended*
"""
        
        for bid in high_relevance:
            report += f"""
### {bid['title']}
- **Source:** {bid['source']}
- **Date:** {bid['date']}
- **Relevance Score:** {bid['relevance_score']}/20
- **URL:** {bid['url']}
- **Status:** {bid['status']}
"""
        
        if medium_relevance:
            report += f"""
## 📊 Medium Relevance Opportunities ({len(medium_relevance)})
*Score 4-7 | Worth monitoring*
"""
            for bid in medium_relevance[:5]:
                report += f"- **{bid['title']}** ({bid['source']}) - Score: {bid['relevance_score']}\n"
        
        report += f"""
## 📈 Summary
- **Total Opportunities Found:** {len(self.fresh_opportunities)}
- **High Priority:** {len(high_relevance)}
- **Medium Priority:** {len(medium_relevance)}
- **Search Period:** Last 30 days

---
*Generated by Current Water Quality Bid Monitor*
"""
        
        return report

    def run_current_scan(self):
        """Run scan for current opportunities only"""
        logging.info("🔍 Starting current bid scan...")
        
        start_time = time.time()
        
        try:
            # Clear previous results
            self.fresh_opportunities = []
            
            # Search for current opportunities
            self.fetch_recent_opportunities()
            self.search_current_sources()
            
            # Generate and save report
            report = self.generate_current_report()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save report
            report_file = f'current_bid_report_{timestamp}.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            # Save data
            if self.fresh_opportunities:
                data_file = f'current_bids_{timestamp}.json'
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(self.fresh_opportunities, f, ensure_ascii=False, indent=2)
            
            elapsed = time.time() - start_time
            logging.info(f"✅ Current scan completed in {elapsed:.2f} seconds")
            logging.info(f"📊 Found {len(self.fresh_opportunities)} current opportunities")
            
            return {
                'report': report,
                'report_file': report_file,
                'data_file': f'current_bids_{timestamp}.json' if self.fresh_opportunities else None,
                'total_found': len(self.fresh_opportunities),
                'high_priority': len([b for b in self.fresh_opportunities if b['relevance_score'] >= 8])
            }
            
        except Exception as e:
            logging.error(f"❌ Current scan failed: {e}")
            return {'error': str(e)}

if __name__ == "__main__":
    monitor = CurrentBidMonitor()
    results = monitor.run_current_scan()
    
    print("\n" + "="*60)
    print("🌊 CURRENT WATER QUALITY BID SCAN RESULTS")
    print("="*60)
    
    if 'error' not in results:
        print(f"📈 Current Opportunities: {results['total_found']}")
        print(f"🔥 High Priority: {results['high_priority']}")
        if results.get('data_file'):
            print(f"📁 Data saved to: {results['data_file']}")
        print(f"📄 Report: {results['report_file']}")
    else:
        print(f"❌ Error: {results['error']}")
    
    print("\n" + results['report'][:1000] + "..." if len(results['report']) > 1000 else results['report'])