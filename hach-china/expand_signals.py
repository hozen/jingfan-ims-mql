#!/usr/bin/env python3
"""Expand signals for all 10 accounts back to 2026-01-01"""

import re

with open('a-tier-demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# New historical signals for each account (since 2026-01-01)
new_signals = {
    'beijing': '''
      { urgency:'MED', title:'北京市水务局 2026 年预算公布', desc:'北京市水务局发布 2026 年部门预算，水质监测设备采购预算 ¥1200 万，同比 +15%', action:'提前接触预算执行单位，了解采购计划', date:'1 月 15 日', source:'北京市水务局官网', sourceUrl:'https://swj.beijing.gov.cn/' },
      { urgency:'LOW', title:'第九水厂 2025 年度运营报告发布', desc:'第九水厂发布 2025 年运营报告，水质达标率 99.8%，但提及仪器老化问题', action:'借机推介仪器更新方案，强调新标准合规', date:'1 月 8 日', source:'北京市自来水集团官网', sourceUrl:'https://www.beijingwater.com.cn/' },
      { urgency:'MED', title:'2026 年北京市重点工程计划发布', desc:'北京市发改委发布 2026 年重点工程计划，含 3 座新水厂建设', action:'跟进新水厂项目，提前介入设计方案', date:'1 月 5 日', source:'北京市发改委', sourceUrl:'https://fgw.beijing.gov.cn/' },
''',
    'shanghai': '''
      { urgency:'HIGH', title:'上海市水务局 2026 年工作重点发布', desc:'上海市水务局发布 2026 年工作重点，明确超低排放改造 6 月底验收', action:'准备验收监测方案，联系已改造水厂', date:'1 月 20 日', source:'上海市水务局', sourceUrl:'https://swj.sh.gov.cn/' },
      { urgency:'MED', title:'城投水务 2026 年采购计划曝光', desc:'据招标代理机构透露，城投水务 2026 年计划采购在线监测仪器约 ¥300 万', action:'提前准备技术方案，联系技术负责人', date:'1 月 12 日', source:'🔒 内部情报 · 招标代理反馈', sourceUrl:'https://www.qcc.com/' },
      { urgency:'LOW', title:'上海市智慧水务建设指南发布', desc:'上海市发布智慧水务建设指南，要求 2026 年核心水厂数据全接入', action:'准备 Hach 数字化平台对接方案', date:'1 月 5 日', source:'上海市经信委', sourceUrl:'https://sheitc.sh.gov.cn/' },
''',
    'guangzhou': '''
      { urgency:'MED', title:'广州市水务局 2026 年部门预算公布', desc:'广州市水务局 2026 年部门预算公布，水质监测设备预算 ¥800 万', action:'提前接触预算执行单位，了解采购计划', date:'1 月 18 日', source:'广州市水务局', sourceUrl:'https://swj.gz.gov.cn/' },
      { urgency:'LOW', title:'广州水务投资集团 2025 年报发布', desc:'广州水务投资集团发布 2025 年报，营收 ¥45 亿，同比 +8%', action:'借机拜访，了解 2026 年投资计划', date:'1 月 10 日', source:'中国水网', sourceUrl:'https://www.h2o-china.com/' },
      { urgency:'MED', title:'广东省地下水监测点位新增计划', desc:'广东省生态环境厅发布地下水监测点位新增计划，广州新增 15 个点位', action:'跟进监测点位仪器配置需求', date:'1 月 3 日', source:'广东省生态环境厅', sourceUrl:'https://gdee.gd.gov.cn/' },
''',
    'chengdu': '''
      { urgency:'HIGH', title:'第五污水处理厂立项获批', desc:'成都市发改委批复第五污水处理厂项目，设计规模 10 万 t/d，投资 ¥8.5 亿', action:'立即跟进，从设计阶段介入仪器选型', date:'2 月 20 日', source:'成都市发改委', sourceUrl:'https://fgw.chengdu.gov.cn/' },
      { urgency:'MED', title:'兴蓉环境 2026 年资本支出计划', desc:'兴蓉环境公告 2026 年资本支出计划，设备更新预算 ¥5000 万', action:'准备设备更新方案，联系技术负责人', date:'1 月 25 日', source:'巨潮资讯网', sourceUrl:'http://www.cninfo.com.cn/' },
      { urgency:'LOW', title:'四川省水务厅 2026 年工作要点', desc:'四川省水务厅发布 2026 年工作要点，推进智慧水务建设', action:'准备智慧水务解决方案', date:'1 月 8 日', source:'四川省水务厅', sourceUrl:'https://swt.sc.gov.cn/' },
''',
    'sinopec': '''
      { urgency:'HIGH', title:'中石化 2026 年国产化替代清单发布', desc:'中石化发布 2026 年国产化替代清单，在线水质监测仪器列入', action:'准备国产化技术论证报告，联系事业部', date:'2 月 15 日', source:'中国石化新闻网', sourceUrl:'https://news.sinopec.com/' },
      { urgency:'MED', title:'炼油事业部 2026 年环保预算公布', desc:'炼油事业部 2026 年环保预算 ¥2.5 亿，含在线监测设备更新', action:'准备更新方案，强调合规与可靠性', date:'1 月 22 日', source:'🔒 内部情报 · 事业部预算文件', sourceUrl:'' },
      { urgency:'LOW', title:'生态环境部炼化企业专项检查通知', desc:'生态环境部发布炼化企业专项检查通知，3-4 月执行', action:'提醒客户检查前做好仪器校准', date:'1 月 10 日', source:'生态环境部', sourceUrl:'https://www.mee.gov.cn/' },
''',
    'huaneng': '''
      { urgency:'HIGH', title:'华能集团 2026 年框架采购招标预告', desc:'华能集团发布 2026 年框架采购招标预告，仪器仪表类别 3 月启动', action:'立即准备投标文件，联系物资部', date:'2 月 28 日', source:'华能集团采购平台', sourceUrl:'https://ec.chng.com.cn/' },
      { urgency:'MED', title:'华能国际 2025 年报发布', desc:'华能国际发布 2025 年报，营收 ¥2500 亿，同比 +5%', action:'借机拜访，了解 2026 年技改计划', date:'1 月 28 日', source:'上交所', sourceUrl:'http://www.sse.com.cn/' },
      { urgency:'LOW', title:'电力行业超低排放改造验收指南发布', desc:'中电联发布电力行业超低排放改造验收指南', action:'准备验收监测方案', date:'1 月 15 日', source:'中电联', sourceUrl:'https://www.cec.org.cn/' },
''',
    'sinopharm': '''
      { urgency:'MED', title:'药监局 2026 年飞行检查计划发布', desc:'国家药监局发布 2026 年飞行检查计划，制药用水系统为重点', action:'提醒客户做好检查准备，提供合规支持', date:'2 月 10 日', source:'国家药监局', sourceUrl:'https://www.nmpa.gov.cn/' },
      { urgency:'LOW', title:'中国药典 2025 版征求意见稿发布', desc:'中国药典 2025 版征求意见稿发布，制药用水标准有更新', action:'准备标准解读材料', date:'1 月 20 日', source:'国家药典委员会', sourceUrl:'https://www.chp.org.cn/' },
      { urgency:'MED', title:'国药控股 2026 年资本支出计划', desc:'国药控股公告 2026 年资本支出计划，生产基地升级预算 ¥3 亿', action:'跟进生产基地水质仪器升级需求', date:'1 月 12 日', source:'港交所', sourceUrl:'https://www.hkex.com.hk/' },
''',
    'semiconductor': '''
      { urgency:'HIGH', title:'中芯国际 2026 年资本支出计划公布', desc:'中芯国际公告 2026 年资本支出 $80 亿，含厂务系统升级', action:'跟进 UPW 系统监测设备需求', date:'2 月 25 日', source:'上交所', sourceUrl:'http://www.sse.com.cn/' },
      { urgency:'MED', title:'工信部半导体用水新规征求意见', desc:'工信部发布半导体用水新规征求意见稿，2027 年执行', action:'准备新规解读与合规方案', date:'1 月 30 日', source:'工信部', sourceUrl:'https://www.miit.gov.cn/' },
      { urgency:'LOW', title:'SEMI F63 超纯水标准更新', desc:'SEMI 发布 F63 超纯水标准更新版，新增 5 项指标', action:'准备新标准检测方案', date:'1 月 15 日', source:'SEMI 官网', sourceUrl:'https://www.semi.org/' },
''',
    'steel': '''
      { urgency:'HIGH', title:'宝武集团 2026 年超低排放改造计划', desc:'宝武集团发布 2026 年超低排放改造计划，6 月底前完成验收', action:'准备验收监测方案，联系湛江基地', date:'2 月 18 日', source:'中国宝武官网', sourceUrl:'https://www.baowugroup.com/' },
      { urgency:'MED', title:'宝钢股份 2026 年设备更新预算', desc:'宝钢股份公告 2026 年设备更新预算 ¥1.2 亿，含在线监测', action:'准备设备更新方案', date:'1 月 26 日', source:'上交所', sourceUrl:'http://www.sse.com.cn/' },
      { urgency:'LOW', title:'钢铁工业水污染物排放标准修订启动', desc:'生态环境部启动钢铁工业水污染物排放标准修订', action:'参与标准修订研讨，提前布局', date:'1 月 10 日', source:'生态环境部', sourceUrl:'https://www.mee.gov.cn/' },
''',
    'food': '''
      { urgency:'MED', title:'伊利股份 2026 年资本支出计划', desc:'伊利股份公告 2026 年资本支出计划，新工厂建设预算 ¥50 亿', action:'跟进呼和浩特智慧工厂水质仪器需求', date:'2 月 22 日', source:'上交所', sourceUrl:'http://www.sse.com.cn/' },
      { urgency:'LOW', title:'乳品用水新标准征求意见稿发布', desc:'卫健委发布乳品用水新标准征求意见稿，2027 年执行', action:'准备标准解读与合规方案', date:'1 月 28 日', source:'国家卫健委', sourceUrl:'https://www.nhc.gov.cn/' },
      { urgency:'MED', title:'FSSC 22000 V6 标准升级要求', desc:'FSSC 22000 发布 V6 标准升级要求，水质监测要求提高', action:'准备 FSSC 22000 合规支持方案', date:'1 月 15 日', source:'FSSC 22000 官网', sourceUrl:'https://www.fssc22000.com/' },
''',
}

# Find and replace signals for each account
account_keys = {
    'beijing': 'beijing:',
    'shanghai': 'shanghai:',
    'guangzhou': 'guangzhou:',
    'chengdu': 'chengdu:',
    'sinopec': 'sinopec:',
    'huaneng': 'huaneng:',
    'sinopharm': 'sinopharm:',
    'semiconductor': 'semiconductor:',
    'steel': 'steel:',
    'food': 'food:',
}

for acc_key, acc_marker in account_keys.items():
    # Find the signals array for this account
    pattern = rf"({acc_marker}[^{{]*?name: '[^']*'.*?signals: \[)([^{{]*?\}},\n\s*\{{[^}}]*?urgency:'LOW'[^}}]*?\}},\n\s*\])([^,]*?,\n\s*opps:)"
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        before_signals = match.group(1)
        existing_signals = match.group(2)
        after_signals = match.group(3)
        
        # Insert new signals before existing ones
        new_content = before_signals + new_signals[acc_key] + '      ' + existing_signals + after_signals
        content = content[:match.start()] + new_content + content[match.end():]
        print(f'✅ Added signals for {acc_key}')
    else:
        print(f'❌ Could not find signals for {acc_key}')

with open('a-tier-demo.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone! Signals expanded for all accounts.')
