#!/usr/bin/env python3
"""
Daily Bidding Monitor for Hach Sales Team
Quick scan and notification system
"""

import os
import sys
import json
from datetime import datetime
from enhanced_bid_monitor import EnhancedBidMonitor

class DailyMonitor:
    def __init__(self):
        self.monitor = EnhancedBidMonitor()
        self.results = None
        
    def run_quick_scan(self):
        """Run a quick scan for new opportunities"""
        print("🔍 Running daily quick scan for Hach...")
        self.results = self.monitor.run_collection()
        
        if 'error' not in self.results:
            return self.generate_summary()
        else:
            return f"❌ Error during scan: {self.results['error']}"
    
    def generate_summary(self):
        """Generate executive summary"""
        if not self.results['total_opportunities']:
            return """
📊 **HACH DAILY BIDDING SCAN**
🕐 {timestamp}

✅ **Status:** No new opportunities found
🔍 **Platforms Checked:** Taizhou Finance Bureau, China Bidding Organization
⏰ **Next Scan:** Tomorrow at same time

💡 **Tip:** This is normal - not every platform posts daily. The system continues monitoring in background.
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        high_priority = self.results['high_priority']
        total = self.results['total_opportunities']
        
        summary = f"""
📊 **HACH DAILY BIDDING SCAN**
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if high_priority > 0:
            summary += f"""🚨 **URGENT - {high_priority} HIGH PRIORITY OPPORTUNITIES FOUND!**

🔥 **Action Required:** Contact immediately before deadlines
📈 **Total Opportunities:** {total}
📁 **Details:** Check saved report and CSV files

**Files Generated:**
- 📄 Report: {self.results['report_file']}
- 📊 Data (JSON): {self.results['json_file']}  
- 📋 Export (CSV): {self.results['csv_file']}
"""
        else:
            summary += f"""✅ **Status:** {total} opportunities found (no high priority)
🔍 **Platforms Checked:** All configured sources
📈 **Next Steps:** Review medium/low priority opportunities

**Files Generated:**
- 📄 Report: {self.results['report_file']}
- 📊 Data: {self.results['csv_file']}
"""
        
        summary += "\n⏰ **Next Scan:** Tomorrow at same time"
        return summary

if __name__ == "__main__":
    daily = DailyMonitor()
    summary = daily.run_quick_scan()
    print(summary)