#!/usr/bin/env python3
"""
Water Quality Instrument Bidding Information Collector
Designed for Hach sales to monitor government procurement opportunities
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import os
from datetime import datetime, timedelta
import time
import re
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bid_scraper.log'),
        logging.StreamHandler()
    ]
)

class WaterBidScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
        # Keywords relevant to Hach water quality equipment
        self.hach_keywords = [
            '水质', '监测', '检测', '仪表', '仪器', '传感器', '分析',
            'ph', '溶氧', '浊度', '余氯', 'cod', '氨氮', '总磷', '总氮',
            '多参数', '在线', '实时', '自动', '监测站', '污水处理',
            'water quality', 'monitoring', 'sensor', 'analyzer'
        ]
        
        # Target websites
        self.target_sites = {
            'ccgp_gov': 'http://www.ccgp.gov.cn/',
            'ggzy_gov': 'http://www.ggzy.gov.cn/',
            'chinabidding': 'http://www.chinabidding.org.cn/',
            'taizhou_gov': 'https://czj.taizhou.gov.cn/tzzfcgw/',
            'yongwu_gov': 'https://www.yw.gov.cn/',
            'sz_water': 'https://cg.sz-water.com.cn/',
            'zhumadian_gov': 'https://zhumadian.zfcg.henan.gov.cn/'
        }

    def search_ggzy_gov(self):
        """Search National Public Resource Trading Platform"""
        logging.info("Searching National Public Resource Trading Platform...")
        
        # Search URLs for water quality related terms
        search_terms = ['水质监测', '水质检测', '污水处理', '环境监测']
        
        for term in search_terms:
            try:
                # Construct search URL (simplified - would need actual API)
                search_url = f"http://www.ggzy.gov.cn/Front/Search/Index"
                
                # This is a simplified approach - real implementation would need proper API
                logging.info(f"Searching for: {term}")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logging.error(f"Error searching GGZY for {term}: {e}")

    def search_chinabidding_org(self):
        """Search China Bidding Organization"""
        logging.info("Searching China Bidding Organization...")
        
        try:
            # Search page for water quality monitoring
            search_url = "http://www.chinabidding.org.cn/"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract bid listings (simplified - would need actual selectors)
                bid_items = soup.find_all('div', class_='bid-item')
                
                for item in bid_items:
                    title = item.get_text(strip=True)
                    if any(keyword in title for keyword in self.hach_keywords):
                        self.extract_bid_info(item, 'chinabidding.org')
                        
        except Exception as e:
            logging.error(f"Error searching chinabidding.org: {e}")

    def search_sz_water_group(self):
        """Search Shenzhen Water Group procurement platform"""
        logging.info("Searching Shenzhen Water Group...")
        
        try:
            # Base URL for water group procurement
            base_url = "https://cg.sz-water.com.cn/"
            
            response = self.session.get(base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for procurement announcements
                announcements = soup.find_all('a', href=re.compile(r'.*\.(jhtml|html)$'))
                
                for ann in announcements[:20]:  # Limit to recent items
                    title = ann.get_text(strip=True)
                    if any(keyword in title for keyword in self.hach_keywords):
                        link = urljoin(base_url, ann.get('href'))
                        self.extract_bid_from_page(link, 'sz-water-group')
                        
        except Exception as e:
            logging.error(f"Error searching sz-water.com: {e}")

    def extract_bid_from_page(self, url, source):
        """Extract detailed bid information from a specific page"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_elem = soup.find('h1') or soup.find('h2') or soup.find('title')
                title = title_elem.get_text(strip=True) if title_elem else "No title"
                
                # Extract content
                content_elem = soup.find('div', class_='content') or soup.find('div', id='content')
                content = content_elem.get_text(strip=True) if content_elem else ""
                
                # Extract dates
                date_patterns = [
                    r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
                    r'(\d{4}年\d{1,2}月\d{1,2}日)',
                    r'发布时间[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
                ]
                
                publication_date = None
                deadline = None
                
                full_text = title + " " + content
                
                for pattern in date_patterns:
                    matches = re.findall(pattern, full_text)
                    if matches and not publication_date:
                        publication_date = matches[0]
                    if matches and len(matches) > 1 and not deadline:
                        deadline = matches[1]
                
                # Extract contact info
                contact_patterns = [
                    r'联系[人方式][：:]\s*([^\n\r]+)',
                    r'电话[：:]\s*(\d{3,4}[-\s]?\d{7,8})',
                    r'邮箱[：:]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'联系人[：:]\s*([^\n\r]+)'
                ]
                
                contact_info = {}
                for pattern in contact_patterns:
                    matches = re.findall(pattern, full_text)
                    if matches:
                        contact_info['raw'] = matches[0]
                
                # Create bid record
                bid_record = {
                    'title': title,
                    'source': source,
                    'url': url,
                    'publication_date': publication_date,
                    'deadline': deadline,
                    'content_preview': content[:500] + "..." if len(content) > 500 else content,
                    'contact_info': contact_info,
                    'extracted_at': datetime.now().isoformat(),
                    'relevance_score': self.calculate_relevance(title + " " + content)
                }
                
                self.results.append(bid_record)
                logging.info(f"Extracted bid: {title}")
                
        except Exception as e:
            logging.error(f"Error extracting bid from {url}: {e}")

    def extract_bid_info(self, element, source):
        """Extract bid information from search results element"""
        try:
            title_elem = element.find('a') or element.find('h3') or element.find('h4')
            title = title_elem.get_text(strip=True) if title_elem else "No title"
            
            # Check relevance to Hach products
            if any(keyword in title for keyword in self.hach_keywords):
                url_elem = element.find('a')
                if url_elem and url_elem.get('href'):
                    bid_url = url_elem.get('href')
                    if not bid_url.startswith('http'):
                        bid_url = urljoin(f"https://{source}", bid_url)
                    
                    self.extract_bid_from_page(bid_url, source)
                    
        except Exception as e:
            logging.error(f"Error extracting bid info: {e}")

    def calculate_relevance(self, text):
        """Calculate relevance score for Hach products"""
        score = 0
        text_lower = text.lower()
        
        # High-value keywords (specific Hach products/markets)
        high_value = ['多参数', 'cod', '氨氮', '总磷', '总氮', '在线监测', '自动监测']
        medium_value = ['水质', '监测', '检测', 'ph', '溶氧', '浊度']
        low_value = ['仪表', '仪器', '传感器']
        
        for keyword in high_value:
            if keyword in text:
                score += 10
                
        for keyword in medium_value:
            if keyword in text:
                score += 5
                
        for keyword in low_value:
            if keyword in text:
                score += 2
        
        return score

    def save_results(self):
        """Save results to files"""
        if not self.results:
            logging.info("No new results to save")
            return
            
        # Save to JSON
        with open('water_bids.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        with open('water_bids.csv', 'w', newline='', encoding='utf-8') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
        
        # Sort by relevance
        self.results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        logging.info(f"Saved {len(self.results)} bid results")

    def generate_report(self):
        """Generate a summary report"""
        if not self.results:
            return "No new bidding opportunities found."
        
        report = f"""
# Water Quality Equipment Bidding Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## High Priority Opportunities (Score ≥ 10)
"""
        
        high_priority = [r for r in self.results if r['relevance_score'] >= 10]
        if high_priority:
            for bid in high_priority:
                report += f"""
### {bid['title']}
- **Source:** {bid['source']}
- **Publication Date:** {bid['publication_date'] or 'Unknown'}
- **Deadline:** {bid['deadline'] or 'Unknown'}
- **URL:** {bid['url']}
- **Relevance Score:** {bid['relevance_score']}
"""
        
        report += f"""
## Other Opportunities ({len(self.results) - len(high_priority)} total)
"""
        
        medium_priority = [r for r in self.results if 5 <= r['relevance_score'] < 10]
        low_priority = [r for r in self.results if r['relevance_score'] < 5]
        
        for bid in medium_priority[:5]:  # Show top 5 medium priority
            report += f"- {bid['title']} ({bid['source']}) - Score: {bid['relevance_score']}\n"
        
        return report

    def run(self):
        """Main execution method"""
        logging.info("Starting water bid collection...")
        start_time = time.time()
        
        try:
            # Search various sources
            self.search_chinabidding_org()
            self.search_sz_water_group()
            self.search_ggzy_gov()
            
            # Save results
            self.save_results()
            
            # Generate report
            report = self.generate_report()
            with open('bid_report.md', 'w', encoding='utf-8') as f:
                f.write(report)
            
            elapsed = time.time() - start_time
            logging.info(f"Collection completed in {elapsed:.2f} seconds")
            logging.info(f"Found {len(self.results)} relevant opportunities")
            
            return report
            
        except Exception as e:
            logging.error(f"Error during collection: {e}")
            return f"Error: {e}"

if __name__ == "__main__":
    scraper = WaterBidScraper()
    report = scraper.run()
    print(report)