#!/bin/bash
# Hach Water Quality Bidding Monitor - Automated Daily Scan
# Runs daily at 9:00 AM China time

WORKSPACE="/Users/leishi/.openclaw/workspace"
LOGFILE="$WORKSPACE/monitoring/logs/daily_scan_$(date +%Y%m%d).log"

echo "===============================================" >> $LOGFILE
echo "HACH BIDDING MONITOR - $(date)" >> $LOGFILE
echo "===============================================" >> $LOGFILE

cd $WORKSPACE

# Run the daily scan
python3 daily_bid_monitor.py >> $LOGFILE 2>&1

# Check for high priority opportunities
HIGH_PRIORITY_COUNT=$(grep -c "HIGH PRIORITY" $LOGFILE)

if [ $HIGH_PRIORITY_COUNT -gt 0 ]; then
    echo "" >> $LOGFILE
    echo "🚨 HIGH PRIORITY OPPORTUNITIES DETECTED!" >> $LOGFILE
    echo "🔔 Check the report file for details" >> $LOGFILE
    
    # Save timestamp for notification
    echo "$(date): HIGH_PRIORITY_FOUND" > $WORKSPACE/monitoring/alerts/last_high_priority.txt
fi

# Clean up old logs (keep 30 days)
find $WORKSPACE/monitoring/logs/ -name "*.log" -mtime +30 -delete 2>/dev/null

echo "Scan completed at $(date)" >> $LOGFILE
echo "===============================================" >> $LOGFILE