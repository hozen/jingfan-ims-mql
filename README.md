# Hach Water Quality Bidding Monitoring System

## System Overview
This system automatically monitors Chinese government procurement platforms for water quality monitoring equipment opportunities relevant to Hach sales.

## Files Generated

### Core Scripts
- `enhanced_bid_monitor.py` - Main collection engine
- `daily_bid_monitor.py` - Quick daily scan script
- `water_bid_scraper.py` - Basic scraper (legacy)

### Data Files
- `bid_data_YYYYMMDD_HHMMSS.json` - Raw data in JSON format
- `bid_data_YYYYMMDD_HHMMSS.csv` - Spreadsheet-ready export
- `hach_bid_report_YYYYMMDD_HHMMSS.md` - Formatted report

### Monitoring Structure
```
monitoring/
├── reports/     # Latest reports
├── data/        # Historical data
└── logs/        # System logs
```

## Usage

### Manual Run
```bash
python3 enhanced_bid_monitor.py
```

### Quick Daily Scan  
```bash
python3 daily_bid_monitor.py
```

## Target Platforms
1. **Taizhou Finance Bureau** (泰州市财政局)
2. **China Bidding Organization** (中国政府采购招标网)
3. **Shenzhen Water Group** (深圳环水集团)
4. **National Public Resource Trading Platform** (全国公共资源交易平台)

## Hach Relevance Scoring
- **15-25 points:** High Priority (immediate action)
- **8-14 points:** Medium Priority (monitor and review)
- **0-7 points:** Low Priority (background tracking)

### Scoring Criteria
- Specific Hach products (COD analyzers, multi-parameter monitors): +15
- Water quality monitoring systems: +8
- General water quality equipment: +3
- Equipment mentions (pH, DO, turbidity, etc.): +2 each

## Automation Setup
To run automatically, set up a cron job:
```bash
# Daily at 9 AM China time
0 9 * * * cd /Users/leishi/.openclaw/workspace && python3 daily_bid_monitor.py
```

## Contact Information Extraction
The system automatically extracts:
- Project title and number
- Publication and deadline dates  
- Budget information
- Contact person and phone
- Email and address
- Equipment requirements
- Full project content

## Next Steps
1. Run initial collection to populate database
2. Set up automated daily scanning
3. Review high-priority opportunities immediately
4. Track response rates for optimization