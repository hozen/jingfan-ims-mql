#!/usr/bin/env python3
"""
Enhanced Water Quality Bidding Monitor
Real-time monitoring of Hach-relevant procurement opportunities
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
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnhancedBidMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Hach product categories and keywords
        self.hach_products = {
            'analyzers': ['cod分析仪', '氨氮分析仪', '总磷分析仪', '总氮分析仪', 'cod analyzer', 'ammonia analyzer'],
            'sensors': ['ph传感器', '溶氧传感器', '浊度传感器', '余氯传感器', 'ph sensor', 'do sensor'],
            'monitors': ['水质监测', '在线监测', '实时监测', '自动监测', 'water quality monitoring'],
            'equipment': ['多参数分析仪', '水质仪表', '水质仪器', 'environmental monitoring'],
            'software': ['水质软件', '监测系统', 'data logger', 'scada']
        }
        
        # Target procurement platforms with actual access methods
        self.platforms = {
            'taizhou_czj': {
                'name': '泰州市财政局',
                'base_url': 'https://czj.taizhou.gov.cn',
                'search_url': 'https://czj.taizhou.gov.cn/tzzfcgw/cgxx/sjcgxx/zbcg/gkzb/',
                'keywords': ['水质', '监测', '污水处理', '环境']
            },
            'chinabidding_org': {
                'name': '中国政府采购招标网',
                'base_url': 'http://www.chinabidding.org.cn',
                'search_path': '/BidInfoDetails_bid_',
                'keywords': ['水质监测', '检测仪器', '环保设备']
            },
            'sz_water': {
                'name': '深圳环水集团',
                'base_url': 'https://cg.sz-water.com.cn',
                'search_path': '/hyzbgg/',
                'keywords': ['水质', '监测设备', '仪器']
            }
        }
        
        self.bid_results = []
        self.new_opportunities = []

    def fetch_taizhou_opportunities(self):
        """Fetch opportunities from Taizhou Finance Bureau"""
        logging.info("Fetching Taizhou Finance Bureau opportunities...")
        
        try:
            # Try to access the specific water quality monitoring project we found
            url = "https://czj.taizhou.gov.cn/tzzfcgw/cgxx/sjcgxx/zbcg/gkzb/art/2025/art_dee6510586db43f991b44538536df16c.html"
            
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                bid_info = self.extract_project_details(soup, url, '泰州市财政局')
                if bid_info:
                    self.bid_results.append(bid_info)
                    logging.info(f"Found bid: {bid_info['title']}")
                    
        except Exception as e:
            logging.error(f"Error fetching Taizhou opportunities: {e}")

    def fetch_shibidding_opportunities(self):
        """Fetch opportunities from China Bidding Organization"""
        logging.info("Fetching China Bidding Organization opportunities...")
        
        try:
            # Search for water quality related projects
            search_terms = ['水质监测', '污水处理', '环境监测', '水质检测']
            
            for term in search_terms:
                # Use search functionality
                search_url = f"http://www.chinabidding.org.cn/search.php?keyword={term}"
                
                try:
                    response = self.session.get(search_url, timeout=8)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract bid listings
                        bid_links = soup.find_all('a', href=re.compile(r'/BidInfoDetails_bid_.*\.html'))
                        
                        for link in bid_links[:10]:  # Limit to recent results
                            bid_url = urljoin('http://www.chinabidding.org.cn', link.get('href'))
                            self.extract_detailed_bid(bid_url, '中国政府采购招标网')
                            
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logging.error(f"Error searching term '{term}': {e}")
                    
        except Exception as e:
            logging.error(f"Error fetching China Bidding Organization opportunities: {e}")

    def extract_project_details(self, soup, url, source):
        """Extract detailed project information"""
        try:
            # Extract title
            title_elem = soup.find('h1') or soup.find('h2') or soup.find('title') or soup.find(class_=re.compile(r'.*title.*'))
            title = title_elem.get_text(strip=True) if title_elem else "项目标题未找到"
            
            # Extract project number
            project_num_patterns = [
                r'项目编号[：:\s]*([A-Z0-9\-]+)',
                r'采购项目编号[：:\s]*([A-Z0-9\-]+)',
                r'招标编号[：:\s]*([A-Z0-9\-]+)'
            ]
            project_number = None
            content_text = soup.get_text()
            for pattern in project_num_patterns:
                match = re.search(pattern, content_text)
                if match:
                    project_number = match.group(1)
                    break
            
            # Extract dates
            date_patterns = [
                r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
                r'(\d{4}年\d{1,2}月\d{1,2}日)',
                r'发布时间[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
                r'截止时间[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
            ]
            
            dates = {'publication': None, 'deadline': None}
            for pattern in date_patterns:
                matches = re.findall(pattern, content_text)
                for match in matches:
                    if not dates['publication']:
                        dates['publication'] = match
                    elif not dates['deadline']:
                        dates['deadline'] = match
                        break
            
            # Extract contact information
            contact_info = {}
            contact_patterns = {
                'person': r'联系[人方式][：:]\s*([^\n\r,，]+)',
                'phone': r'电话[：:]\s*(\d{3,4}[-\s]?\d{7,8})',
                'email': r'邮箱[：:]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                'address': r'地址[：:]\s*([^\n\r,，]+)'
            }
            
            for key, pattern in contact_patterns.items():
                match = re.search(pattern, content_text)
                if match:
                    contact_info[key] = match.group(1).strip()
            
            # Extract budget information
            budget_patterns = [
                r'预算[金金额][：:]\s*(\d+\.?\d*)\s*[万元亿元]',
                r'最高限价[：:]\s*(\d+\.?\d*)\s*[万元亿元]',
                r'采购金额[：:]\s*(\d+\.?\d*)\s*[万元亿元]'
            ]
            budget = None
            for pattern in budget_patterns:
                match = re.search(pattern, content_text)
                if match:
                    budget = match.group(0)
                    break
            
            # Extract equipment requirements
            equipment_requirements = []
            for category, keywords in self.hach_products.items():
                for keyword in keywords:
                    if keyword in content_text:
                        equipment_requirements.append(f"{category}: {keyword}")
            
            # Calculate Hach relevance score
            relevance_score = self.calculate_relevance_score(title, content_text)
            
            return {
                'title': title,
                'project_number': project_number,
                'source': source,
                'url': url,
                'publication_date': dates['publication'],
                'deadline': dates['deadline'],
                'budget': budget,
                'contact_info': contact_info,
                'equipment_requirements': equipment_requirements,
                'relevance_score': relevance_score,
                'content_preview': content_text[:800] + "..." if len(content_text) > 800 else content_text,
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error extracting project details: {e}")
            return None

    def extract_detailed_bid(self, bid_url, source):
        """Extract detailed information from individual bid page"""
        try:
            response = self.session.get(bid_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                bid_info = self.extract_project_details(soup, bid_url, source)
                if bid_info and bid_info['relevance_score'] > 0:
                    self.bid_results.append(bid_info)
                    logging.info(f"Found relevant bid: {bid_info['title']} (Score: {bid_info['relevance_score']})")
                    
        except Exception as e:
            logging.error(f"Error extracting bid from {bid_url}: {e}")

    def calculate_relevance_score(self, title, content):
        """Calculate relevance score for Hach products"""
        text = (title + " " + content).lower()
        score = 0
        
        # High-value keywords (specific Hach products)
        high_value_products = ['cod分析仪', '氨氮分析仪', '总磷分析仪', '多参数分析仪', 
                              'cod analyzer', 'water quality monitoring system']
        
        # Medium value keywords (general water quality)
        medium_value = ['水质监测', '污水处理', '环境监测', '在线监测', '自动监测']
        
        # Basic keywords
        basic_value = ['水质', '检测', '仪表', '仪器', '传感器']
        
        for keyword in high_value_products:
            if keyword in text:
                score += 15
                
        for keyword in medium_value:
            if keyword in text:
                score += 8
                
        for keyword in basic_value:
            if keyword in text:
                score += 3
        
        # Bonus for specific equipment mentions
        equipment_mentions = re.findall(r'(ph|溶氧|浊度|余氯|cod|氨氮|总磷|总氮)', text)
        score += len(set(equipment_mentions)) * 2
        
        return score

    def generate_priority_report(self):
        """Generate prioritized report for Hach sales team"""
        if not self.bid_results:
            return "# No new bidding opportunities found.\n\nTry running the collector again or check network connectivity."
        
        # Sort by relevance score
        sorted_results = sorted(self.bid_results, key=lambda x: x['relevance_score'], reverse=True)
        
        # Categorize by priority
        high_priority = [r for r in sorted_results if r['relevance_score'] >= 15]
        medium_priority = [r for r in sorted_results if 8 <= r['relevance_score'] < 15]
        low_priority = [r for r in sorted_results if r['relevance_score'] < 8]
        
        report = f"""# Hach Water Quality Bidding Monitor Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT+8

## 🔥 URGENT - High Priority Opportunities ({len(high_priority)})
*Relevance Score ≥ 15 | Immediate action recommended*

"""
        
        for bid in high_priority:
            urgency = "🚨 URGENT" if bid['relevance_score'] >= 20 else "⚡ HIGH"
            report += f"""
### {urgency} {bid['title']}

- **Source:** {bid['source']}
- **Project Number:** {bid.get('project_number', 'N/A')}
- **Publication Date:** {bid.get('publication_date', 'Unknown')}
- **Deadline:** {bid.get('deadline', 'Unknown')}
- **Budget:** {bid.get('budget', 'Not specified')}
- **Relevance Score:** {bid['relevance_score']}/25
- **URL:** {bid['url']}

**Equipment Requirements:** {', '.join(bid.get('equipment_requirements', ['Not specified']))}

**Contact Information:**
"""
            for key, value in bid.get('contact_info', {}).items():
                report += f"- {key.title()}: {value}\n"
            
            report += f"\n**Content Preview:** {bid.get('content_preview', 'N/A')[:300]}...\n\n---\n"

        report += f"""
## 📊 Medium Priority Opportunities ({len(medium_priority)})
*Relevance Score 8-14 | Worth monitoring*

"""
        
        for bid in medium_priority[:5]:  # Show top 5
            report += f"- **{bid['title']}** ({bid['source']}) - Score: {bid['relevance_score']}\n"
            if bid.get('deadline'):
                report += f"  Deadline: {bid['deadline']}\n"
            report += f"  URL: {bid['url']}\n\n"

        if low_priority:
            report += f"""
## 📋 Additional Opportunities ({len(low_priority)})
*Relevance Score < 8 | Lower priority but worth noting*

"""
            for bid in low_priority[:3]:  # Show top 3
                report += f"- {bid['title']} ({bid['source']}) - Score: {bid['relevance_score']}\n"

        report += f"""
## 📈 Summary Statistics
- **Total Opportunities Found:** {len(self.bid_results)}
- **High Priority:** {len(high_priority)}
- **Medium Priority:** {len(medium_priority)}
- **Low Priority:** {len(low_priority)}
- **Average Relevance Score:** {sum(r['relevance_score'] for r in self.bid_results) / len(self.bid_results):.1f}

## 🎯 Recommended Actions
1. **Immediate:** Contact high-priority opportunities before deadlines
2. **This Week:** Review medium-priority opportunities for potential fit
3. **Monitor:** Set up alerts for ongoing monitoring of these platforms
4. **Follow-up:** Track response rates and conversion for strategy optimization

---
*Generated by Hach Water Quality Bidding Monitor*
"""
        
        return report

    def save_data(self):
        """Save all collected data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON data
        json_file = f'bid_data_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.bid_results, f, ensure_ascii=False, indent=2)
        
        # Save CSV for spreadsheet analysis
        csv_file = f'bid_data_{timestamp}.csv'
        if self.bid_results:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['title', 'source', 'project_number', 'publication_date', 'deadline', 
                             'budget', 'relevance_score', 'url', 'equipment_requirements']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for bid in self.bid_results:
                    row = {field: bid.get(field, '') for field in fieldnames}
                    row['equipment_requirements'] = '; '.join(bid.get('equipment_requirements', []))
                    writer.writerow(row)
        
        logging.info(f"Data saved to {json_file} and {csv_file}")
        return json_file, csv_file

    def run_collection(self):
        """Run the complete collection process"""
        logging.info("🚀 Starting enhanced water bid collection for Hach...")
        
        start_time = time.time()
        
        try:
            # Collect from all platforms
            self.fetch_taizhou_opportunities()
            self.fetch_shibidding_opportunities()
            
            # Save data and generate report
            json_file, csv_file = self.save_data()
            report = self.generate_priority_report()
            
            # Save report
            report_file = f"hach_bid_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            elapsed = time.time() - start_time
            logging.info(f"✅ Collection completed in {elapsed:.2f} seconds")
            logging.info(f"📊 Found {len(self.bid_results)} total opportunities")
            
            high_priority_count = len([r for r in self.bid_results if r['relevance_score'] >= 15])
            logging.info(f"🔥 {high_priority_count} high-priority opportunities for immediate action")
            
            return {
                'report': report,
                'json_file': json_file,
                'csv_file': csv_file,
                'report_file': report_file,
                'total_opportunities': len(self.bid_results),
                'high_priority': high_priority_count
            }
            
        except Exception as e:
            logging.error(f"❌ Collection failed: {e}")
            return {'error': str(e)}

if __name__ == "__main__":
    monitor = EnhancedBidMonitor()
    results = monitor.run_collection()
    
    if 'error' not in results:
        print("\n" + "="*60)
        print("🎯 HACH WATER QUALITY BIDDING MONITOR RESULTS")
        print("="*60)
        print(f"📈 Total Opportunities: {results['total_opportunities']}")
        print(f"🔥 High Priority: {results['high_priority']}")
        print(f"📁 Data saved to: {results['json_file']}")
        print(f"📋 CSV export: {results['csv_file']}")
        print(f"📄 Report saved to: {results['report_file']}")
        print("="*60)
        print("\nREPORT PREVIEW:")
        print(results['report'][:1000] + "..." if len(results['report']) > 1000 else results['report'])
    else:
        print(f"❌ Error: {results['error']}")