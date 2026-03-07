#!/usr/bin/env python3
"""
Hach Sales Dashboard Generator
Creates HTML reports with instrument mapping and project categorization
"""

import json
from datetime import datetime

class HachSalesDashboard:
    def __init__(self):
        # Hach instrument catalog for mapping
        self.hach_instruments = {
            'analyzers': {
                'cod': ['CODAnalyzer 500 Series', 'COD Reactor', 'COD Colorimeter'],
                'ammonia': ['Ammonia Analyzer', 'Ammonia Ion Selective Electrode'],
                'phosphorus': ['Phosphorus Analyzer', 'Total Phosphorus Kit'],
                'nitrogen': ['Total Nitrogen Analyzer', 'TKN Analyzer'],
                'ph': ['pH/ORP Analyzers', 'pH Sensors', 'pH Transmitters'],
                'dissolved_oxygen': ['DO Analyzers', 'DO Sensors', 'Optical DO'],
                'turbidity': ['Turbidity Analyzers', 'Nephelometric Turbidity'],
                'residual_chlorine': ['Residual Chlorine Analyzers', 'Chlorine Sensors']
            },
            'monitoring_systems': {
                'multi_parameter': ['Multi-Parameter Monitors', 'SCADA Integration', 'Data Loggers'],
                'online_monitoring': ['Online Monitoring Systems', 'Remote Monitoring', 'Wireless Sensors'],
                'wastewater': ['Wastewater Monitors', 'Sewage Treatment Monitoring'],
                'surface_water': ['Surface Water Monitoring', 'River Monitoring', 'Lake Monitoring']
            },
            'software': {
                'scada': ['SCADA Software', 'HMI Systems', 'Control Systems'],
                'data_management': ['Data Management Software', 'Lab Information Systems'],
                'reporting': ['Reporting Software', 'Compliance Reporting', 'Analytics'],
                'remote_access': ['Remote Access Software', 'Cloud Platforms', 'Mobile Apps']
            },
            'services': {
                'om_maintenance': ['O&M Services', 'Preventive Maintenance', 'Emergency Response'],
                'calibration': ['Calibration Services', 'Validation', 'Quality Assurance'],
                'training': ['Training Services', 'Operator Training', 'Technical Support'],
                'consulting': ['Consulting Services', 'System Design', 'Implementation']
            }
        }

        # Current opportunities with enhanced categorization
        self.opportunities = [
            {
                'id': 'HUB003',
                'title': '湖北省生态环境监测中心站2025年湖北省地表水自动监测系统运行维护项目',
                'organization': '湖北省生态环境监测中心站',
                'location': '湖北省',
                'type': 'O&M服务',
                'category': 'services',  # Primary business type
                'secondary_categories': ['monitoring_systems'],
                'hach_instruments': ['multi_parameter', 'online_monitoring', 'om_maintenance', 'calibration'],
                'relevance_score': 25,
                'priority': 'HIGHEST',
                'status': 'ACTIVE',
                'deadline': '2025年',
                'source': '湖北省招标平台',
                'value_estimate': '500万-1000万元',
                'hach_products': [
                    'Multi-Parameter Monitors for surface water',
                    'Online Monitoring Systems with SCADA integration',
                    'O&M Services with 24/7 response',
                    'Calibration and validation services'
                ],
                'competitor_analysis': 'Local Chinese manufacturers + Hach',
                'hach_advantage': 'Provincial-level experience, proven reliability'
            },
            {
                'id': 'HUB001',
                'title': '麻城市乡镇生活污水处理厂水质在线监测系统运维服务采购项目(2025-2026年度)',
                'organization': '麻城市政府',
                'location': '湖北省麻城市',
                'type': 'O&M服务',
                'category': 'services',
                'secondary_categories': ['monitoring_systems', 'analyzers'],
                'hach_instruments': ['cod', 'ph', 'dissolved_oxygen', 'om_maintenance', 'remote_access'],
                'relevance_score': 22,
                'priority': 'HIGH',
                'status': 'ACTIVE',
                'deadline': '2025年-2026年',
                'source': 'https://hubei.zhaobiao.cn/',
                'value_estimate': '50万-100万元',
                'hach_products': [
                    'COD Analyzer for wastewater treatment',
                    'pH/DO Analyzers for process monitoring',
                    'Remote monitoring software',
                    'Comprehensive O&M services'
                ],
                'competitor_analysis': 'Local competitors vs Hach quality',
                'hach_advantage': 'Rural treatment expertise, cost-effective O&M'
            },
            {
                'id': 'HUB002',
                'title': '环县自来水集团污水处理厂水质污染源自动监控系统第三方运维服务',
                'organization': '环县自来水集团有限公司',
                'location': '甘肃省环县',
                'type': '第三方运维服务',
                'category': 'services',
                'secondary_categories': ['monitoring_systems', 'software'],
                'hach_instruments': ['multi_parameter', 'scada', 'om_maintenance', 'training'],
                'relevance_score': 20,
                'priority': 'HIGH',
                'status': 'ACTIVE_INQUIRY',
                'deadline': '待确认',
                'source': 'https://www.huanxian.gov.cn/zls/cg/content_81516',
                'value_estimate': '30万-80万元',
                'hach_products': [
                    'Automatic monitoring systems for pollution sources',
                    'SCADA integration and control systems',
                    'Third-party O&M services',
                    'Operator training programs'
                ],
                'competitor_analysis': 'Automation companies vs Hach monitoring',
                'hach_advantage': 'Pollution source monitoring specialty'
            },
            {
                'id': 'HEN001',
                'title': '侯寨渗滤液项目水质在线监测设备运维服务采购公告',
                'organization': '郑州市项目单位',
                'location': '河南省郑州市',
                'type': '运维服务采购',
                'category': 'services',
                'secondary_categories': ['analyzers', 'monitoring_systems'],
                'hach_instruments': ['cod', 'ammonia', 'phosphorus', 'om_maintenance'],
                'relevance_score': 18,
                'priority': 'MEDIUM_HIGH',
                'status': 'ACTIVE',
                'deadline': '2025-11-10',
                'source': '千里马招标网',
                'value_estimate': '20万-50万元',
                'hach_products': [
                    'COD Analyzer for leachate treatment',
                    'Ammonia and Phosphorus analyzers',
                    'Specialized monitoring for industrial waste',
                    'Maintenance services for harsh environments'
                ],
                'competitor_analysis': 'Industrial monitoring specialists',
                'hach_advantage': 'Leachate treatment experience, robust equipment'
            },
            {
                'id': 'NAN001',
                'title': '南京市秦淮河水质在线自动监测系统运行维护项目',
                'organization': '南京市水务局',
                'location': '江苏省南京市',
                'type': '河流监测O&M',
                'category': 'monitoring_systems',
                'secondary_categories': ['analyzers', 'services'],
                'hach_instruments': ['surface_water', 'multi_parameter', 'om_maintenance'],
                'relevance_score': 16,
                'priority': 'REFERENCE',
                'status': 'RECENT_COMPLETION',
                'deadline': '2025年8-12月',
                'source': 'https://shuiwu.nanjing.gov.cn/',
                'value_estimate': '已完成 - 14.428万元',
                'hach_products': [
                    'Surface water monitoring systems',
                    'River monitoring equipment',
                    'O&M services for municipal waters'
                ],
                'competitor_analysis': 'Won by 南京通达海科技股份有限公司',
                'hach_advantage': 'Track for follow-up opportunities'
            }
        ]

    def generate_html_dashboard(self):
        """Generate comprehensive HTML dashboard"""
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hach Water Quality Bidding Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .stats-bar {{
            display: flex;
            justify-content: space-around;
            background: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .stat {{
            flex: 1;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .content {{
            padding: 30px;
        }}
        .filters {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .filter-group {{
            display: inline-block;
            margin-right: 20px;
        }}
        .filter-group label {{
            font-weight: bold;
            margin-right: 10px;
        }}
        .filter-group select {{
            padding: 8px 12px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            background: white;
        }}
        .opportunity-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .opportunity-card {{
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }}
        .opportunity-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .priority-highest {{
            border-left: 5px solid #e74c3c;
        }}
        .priority-high {{
            border-left: 5px solid #f39c12;
        }}
        .priority-medium {{
            border-left: 5px solid #3498db;
        }}
        .priority-reference {{
            border-left: 5px solid #95a5a6;
        }}
        .opportunity-header {{
            display: flex;
            justify-content: between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        .priority-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: auto;
        }}
        .badge-highest {{
            background: #e74c3c;
        }}
        .badge-high {{
            background: #f39c12;
        }}
        .badge-medium {{
            background: #3498db;
        }}
        .badge-reference {{
            background: #95a5a6;
        }}
        .opportunity-title {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            margin: 0;
            line-height: 1.4;
        }}
        .opportunity-meta {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
            font-size: 0.9em;
        }}
        .meta-item {{
            display: flex;
            flex-direction: column;
        }}
        .meta-label {{
            font-weight: bold;
            color: #7f8c8d;
            margin-bottom: 3px;
        }}
        .meta-value {{
            color: #2c3e50;
        }}
        .hach-products {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .products-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        .products-title::before {{
            content: "🔧";
            margin-right: 8px;
        }}
        .product-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .product-list li {{
            padding: 5px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        .product-list li:last-child {{
            border-bottom: none;
        }}
        .business-categories {{
            display: flex;
            gap: 8px;
            margin: 15px 0;
            flex-wrap: wrap;
        }}
        .category-tag {{
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            color: white;
        }}
        .tag-services {{
            background: #27ae60;
        }}
        .tag-analyzers {{
            background: #8e44ad;
        }}
        .tag-monitoring_systems {{
            background: #3498db;
        }}
        .tag-software {{
            background: #e67e22;
        }}
        .action-section {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .action-title {{
            font-weight: bold;
            color: #856404;
            margin-bottom: 8px;
        }}
        .action-content {{
            color: #856404;
            font-size: 0.9em;
        }}
        .competitive-section {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .competitive-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }}
        .footer {{
            background: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
        .legend {{
            background: #ecf0f1;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .legend-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        .legend-items {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
        }}
        .legend-color {{
            width: 15px;
            height: 15px;
            border-radius: 3px;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Hach Water Quality Bidding Dashboard</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT+8 | Live Monitoring Active</p>
        </div>
        
        <div class="stats-bar">
            <div class="stat">
                <span class="stat-number">{len([o for o in self.opportunities if o['status'] == 'ACTIVE'])}</span>
                <span class="stat-label">Active Opportunities</span>
            </div>
            <div class="stat">
                <span class="stat-number">{len([o for o in self.opportunities if o['priority'] in ['HIGHEST', 'HIGH']])}</span>
                <span class="stat-label">High Priority</span>
            </div>
            <div class="stat">
                <span class="stat-number">{len([o for o in self.opportunities if o['category'] == 'services'])}</span>
                <span class="stat-label">O&M Services</span>
            </div>
            <div class="stat">
                <span class="stat-number">{len([o for o in self.opportunities if o['category'] == 'monitoring_systems'])}</span>
                <span class="stat-label">Hardware Systems</span>
            </div>
        </div>
        
        <div class="content">
            <div class="filters">
                <div class="filter-group">
                    <label>Priority:</label>
                    <select id="priorityFilter">
                        <option value="all">All Priorities</option>
                        <option value="HIGHEST">Highest</option>
                        <option value="HIGH">High</option>
                        <option value="MEDIUM_HIGH">Medium-High</option>
                        <option value="REFERENCE">Reference</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Business Type:</label>
                    <select id="categoryFilter">
                        <option value="all">All Types</option>
                        <option value="services">Services</option>
                        <option value="monitoring_systems">Hardware Systems</option>
                        <option value="analyzers">Analyzers</option>
                        <option value="software">Software</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Location:</label>
                    <select id="locationFilter">
                        <option value="all">All Locations</option>
                        <option value="湖北">Hubei Province</option>
                        <option value="河南">Henan Province</option>
                        <option value="江苏">Jiangsu Province</option>
                        <option value="甘肃">Gansu Province</option>
                    </select>
                </div>
            </div>
            
            <div class="legend">
                <div class="legend-title">Priority Levels & Business Types</div>
                <div class="legend-items">
                    <div class="legend-item">
                        <div class="legend-color" style="background: #e74c3c;"></div>
                        <span>Highest Priority (Provincial/Government)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #f39c12;"></div>
                        <span>High Priority (Municipal)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #27ae60;"></div>
                        <span>Services (O&M, Maintenance)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #3498db;"></div>
                        <span>Hardware (Monitors, Systems)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #8e44ad;"></div>
                        <span>Analyzers (COD, pH, DO)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #e67e22;"></div>
                        <span>Software (SCADA, Reporting)</span>
                    </div>
                </div>
            </div>
            
            <div class="opportunity-grid">
"""

        # Generate opportunity cards
        for opp in sorted(self.opportunities, key=lambda x: (x['priority'] == 'HIGHEST', x['priority'] == 'HIGH', x['relevance_score']), reverse=True):
            
            priority_class = f"priority-{opp['priority'].lower().replace('_', '-')}"
            badge_class = f"badge-{opp['priority'].lower().replace('_', '-')}"
            
            html += f"""
                <div class="opportunity-card {priority_class}" data-priority="{opp['priority']}" data-category="{opp['category']}" data-location="{opp['location']}">
                    <div class="opportunity-header">
                        <h3 class="opportunity-title">{opp['title']}</h3>
                        <span class="priority-badge {badge_class}">{opp['priority'].replace('_', ' ')}</span>
                    </div>
                    
                    <div class="opportunity-meta">
                        <div class="meta-item">
                            <span class="meta-label">Organization</span>
                            <span class="meta-value">{opp['organization']}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Location</span>
                            <span class="meta-value">{opp['location']}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Relevance Score</span>
                            <span class="meta-value">{opp['relevance_score']}/25</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Estimated Value</span>
                            <span class="meta-value">{opp['value_estimate']}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Deadline</span>
                            <span class="meta-value">{opp['deadline']}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Status</span>
                            <span class="meta-value">{opp['status'].replace('_', ' ')}</span>
                        </div>
                    </div>
                    
                    <div class="business-categories">
                        <span class="category-tag tag-{opp['category']}">{opp['category'].replace('_', ' ').title()}</span>
                        {''.join([f'<span class="category-tag tag-{cat}">{cat.replace("_", " ").title()}</span>' for cat in opp['secondary_categories']])}
                    </div>
                    
                    <div class="hach-products">
                        <div class="products-title">Relevant Hach Instruments</div>
                        <ul class="product-list">
"""
            for product in opp['hach_products']:
                html += f"<li>{product}</li>"
            
            html += f"""
                        </ul>
                    </div>
                    
                    <div class="competitive-section">
                        <div class="competitive-title">💡 Hach Advantage</div>
                        <div style="color: #2c3e50; font-size: 0.9em;">{opp['hach_advantage']}</div>
                    </div>
                    
                    <div class="action-section">
                        <div class="action-title">🎯 Immediate Action Required</div>
                        <div class="action-content">{opp.get('source', 'Contact for details')}</div>
                    </div>
                </div>
            """

        html += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Hach Water Quality Bidding Monitor | Next scan: Daily at 9:00 AM</p>
            <p>For technical support or feature requests, contact your IT administrator</p>
        </div>
    </div>
    
    <script>
        // Simple filtering functionality
        document.getElementById('priorityFilter').addEventListener('change', filterOpportunities);
        document.getElementById('categoryFilter').addEventListener('change', filterOpportunities);
        document.getElementById('locationFilter').addEventListener('change', filterOpportunities);
        
        function filterOpportunities() {{
            const priorityFilter = document.getElementById('priorityFilter').value;
            const categoryFilter = document.getElementById('categoryFilter').value;
            const locationFilter = document.getElementById('locationFilter').value;
            
            const cards = document.querySelectorAll('.opportunity-card');
            
            cards.forEach(card => {{
                const priority = card.dataset.priority;
                const category = card.dataset.category;
                const location = card.dataset.location;
                
                let show = true;
                
                if (priorityFilter !== 'all' && priority !== priorityFilter) {{
                    show = false;
                }}
                
                if (categoryFilter !== 'all' && category !== categoryFilter) {{
                    show = false;
                }}
                
                if (locationFilter !== 'all' && !location.includes(locationFilter)) {{
                    show = false;
                }}
                
                card.style.display = show ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""
        
        return html

    def generate_instrument_matrix(self):
        """Generate instrument opportunity matrix"""
        
        matrix = f"""
# Hach Instrument Opportunity Matrix
Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instrument Categories & Opportunities

### COD Analyzers
"""
        
        cod_opportunities = [opp for opp in self.opportunities if 'cod' in opp['hach_instruments']]
        if cod_opportunities:
            for opp in cod_opportunities:
                matrix += f"- **{opp['id']}** ({opp['location']}): {opp['value_estimate']}\n"
        else:
            matrix += "- No current COD opportunities\n"
        
        matrix += f"""
### Multi-Parameter Monitoring Systems
"""
        multi_opportunities = [opp for opp in self.opportunities if 'multi_parameter' in opp['hach_instruments']]
        if multi_opportunities:
            for opp in multi_opportunities:
                matrix += f"- **{opp['id']}** ({opp['location']}): {opp['value_estimate']}\n"
        else:
            matrix += "- No current multi-parameter opportunities\n"
        
        matrix += f"""
### O&M Services
"""
        om_opportunities = [opp for opp in self.opportunities if 'om_maintenance' in opp['hach_instruments']]
        if om_opportunities:
            for opp in om_opportunities:
                matrix += f"- **{opp['id']}** ({opp['location']}): {opp['value_estimate']}\n"
        else:
            matrix += "- No current O&M opportunities\n"
        
        matrix += f"""
### SCADA & Software Solutions
"""
        scada_opportunities = [opp for opp in self.opportunities if 'scada' in opp['hach_instruments']]
        if scada_opportunities:
            for opp in scada_opportunities:
                matrix += f"- **{opp['id']}** ({opp['location']}): {opp['value_estimate']}\n"
        else:
            matrix += "- No current SCADA opportunities\n"
        
        return matrix

    def save_reports(self):
        """Save all reports"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate HTML dashboard
        html_content = self.generate_html_dashboard()
        html_file = f'hach_dashboard_{timestamp}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate JSON data
        json_file = f'hach_opportunities_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.opportunities, f, ensure_ascii=False, indent=2)
        
        # Generate instrument matrix
        matrix_content = self.generate_instrument_matrix()
        matrix_file = f'instrument_matrix_{timestamp}.md'
        with open(matrix_file, 'w', encoding='utf-8') as f:
            f.write(matrix_content)
        
        return {
            'html_file': html_file,
            'json_file': json_file,
            'matrix_file': matrix_file,
            'total_opportunities': len(self.opportunities),
            'high_priority': len([o for o in self.opportunities if o['priority'] in ['HIGHEST', 'HIGH']]),
            'active_opportunities': len([o for o in self.opportunities if o['status'] == 'ACTIVE'])
        }

if __name__ == "__main__":
    dashboard = HachSalesDashboard()
    results = dashboard.save_reports()
    
    print("📊 Generated Hach Sales Dashboard")
    print(f"📱 HTML Dashboard: {results['html_file']}")
    print(f"📁 JSON Data: {results['json_file']}")
    print(f"🔧 Instrument Matrix: {results['matrix_file']}")
    print(f"🎯 Total Opportunities: {results['total_opportunities']}")
    print(f"🔥 High Priority: {results['high_priority']}")
    print(f"⚡ Active: {results['active_opportunities']}")
    print("\n💻 Open the HTML file in your browser to view the dashboard!")