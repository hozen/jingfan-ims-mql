# Standard Work (SW): A-Tier Customer Management
### Hach China | Marketing Team | AI-Augmented | v1.0 | 2026-03

---

## 0. Scope & Principles

**Target:** ~50 A-tier accounts (municipal + industrial), China domestic
**Owner:** Marketing team (in collaboration with field sales)
**Philosophy:** AI handles research and monitoring; humans handle judgment and relationships

**A-tier customer profile for Hach China typically includes:**
- Municipal: Major city waterworks (自来水集团), basin authorities, large WWTP operators
- Industrial: Power (火电/核电), petrochemical (石化), semiconductor, pharma, F&B, steel

---

## 1. One-Time Setup — Account Master Profile

> **AI does 80%, human validates 20%**

### 📋 Prompt 1.1 — Account Intelligence Card Generator

```
You are a B2B market intelligence analyst specializing in China's water quality industry.
Your task is to generate a structured Account Intelligence Card for a key customer of Hach China.

Company: [COMPANY_NAME]
Industry Vertical: [MUNICIPAL / INDUSTRIAL — specify sub-type]
Known Hach products already deployed: [LIST OR "Unknown"]

Please research and fill in the following fields:

1. ORGANIZATION OVERVIEW
   - Business scope and scale
   - Ownership type (国企/民企/外资)
   - Key operating locations in China
   - Annual revenue estimate (if public)
   - Parent group / subsidiaries relevant to water quality

2. DECISION-MAKING STRUCTURE
   - Likely departments involved in instrument procurement (e.g., 环保部, 生产部, 采购部)
   - Typical procurement process (direct purchase / tender / framework agreement)
   - Estimated decision timeline

3. REGULATORY & COMPLIANCE DRIVERS
   - Applicable national/local standards (GB standards, 排放标准, industry-specific)
   - Recent compliance pressure or regulatory changes affecting them
   - Environmental inspection history (if notable)

4. CURRENT HACH FOOTPRINT (ESTIMATED)
   - Products/categories likely in use based on industry norms
   - White space: product categories they likely need but we haven't captured

5. COMPETITIVE LANDSCAPE
   - Known competitors active in this account or vertical (YSI, Endress+Hauser, 哈希竞品 etc.)
   - Likely vendor selection criteria for this customer type

6. OPPORTUNITY SIGNALS
   - Recent expansion plans, new facilities, or infrastructure projects
   - Recent tenders or procurement notices (政府采购/招标)
   - Budget cycle and fiscal year timing

7. RECOMMENDED ENGAGEMENT APPROACH
   - Key value propositions most relevant to this account
   - Suggested first talking points
   - Relationship entry point recommendation

Output format: Structured JSON + a 150-word executive summary in Chinese.
```

---

### 📋 Prompt 1.2 — Stakeholder Mapping

```
Based on the following company: [COMPANY_NAME], industry: [VERTICAL]

Identify the typical stakeholder map for water quality instrument procurement in a Chinese [municipal waterworks / industrial facility] of this scale.

For each stakeholder role, provide:
- Job title (Chinese + English)
- Their primary concern / evaluation criteria
- Their influence level in procurement (Decision Maker / Influencer / User / Gatekeeper)
- Best engagement channel (technical seminar, regulatory briefing, peer reference, etc.)
- Likely pain points that Hach instruments address

Focus on China-specific organizational norms. Include:
- 总经理/副总 level (strategic)
- 环保/水务技术 level (technical)
- 采购/招标办 level (procurement)
- 一线操作 level (end user)
```

---

## 2. Ongoing Monitoring — Weekly Signal Digest

> **Fully AI-driven. Human reviews only flagged items.**

### 📋 Prompt 2.1 — Weekly Signal Monitoring

```
You are a market intelligence agent monitoring signals for Hach China's key account: [COMPANY_NAME].

Please search for and summarize any of the following signal types from the past 7 days:

SIGNAL CATEGORIES (rank by urgency):
🔴 HIGH: New tender/bid announcement (招标/采购公告) related to water quality instruments
🔴 HIGH: Regulatory enforcement action or environmental penalty affecting this company
🟡 MEDIUM: Company expansion announcement (new facility, capacity increase)
🟡 MEDIUM: Leadership change at VP level or above
🟡 MEDIUM: Competitor win or new competitor activity at this account
🟢 LOW: Industry news relevant to their vertical
🟢 LOW: Policy/standard update that affects their compliance obligations
🟢 LOW: Key contact LinkedIn activity or public speech

Sources to check:
- 中国政府采购网 (ccgp.gov.cn)
- 全国招标投标公共服务平台
- 企查查 / 天眼查 company news
- 行业媒体: 中国水网, 仪器信息网, 环保在线
- General news search: [COMPANY_NAME] + water/环保/仪器

Output format:
{
  "account": "[COMPANY_NAME]",
  "week": "[YYYY-WW]",
  "signals": [
    {
      "urgency": "HIGH/MEDIUM/LOW",
      "type": "[signal category]",
      "summary": "[2-3 sentence summary]",
      "source": "[URL or source name]",
      "recommended_action": "[what should sales/marketing do]"
    }
  ],
  "overall_status": "GREEN/YELLOW/RED",
  "digest_summary": "[3-sentence summary in Chinese for sales team]"
}
```

---

## 3. Monthly Account Pulse

> **AI-prepared, human spot-checks flagged accounts**

### 📋 Prompt 3.1 — Monthly Pulse Generator

```
Generate a Monthly Account Pulse report for Hach China key account: [COMPANY_NAME]

Input data:
- Account Intelligence Card: [PASTE CARD]
- Weekly signals from past 4 weeks: [PASTE SIGNAL DIGESTS]
- CRM data: Last sales visit [DATE], last marketing touchpoint [DATE], open opportunities [LIST]
- Sales rep notes: [PASTE ANY NOTES]

Generate the following:

1. ACCOUNT STATUS: GREEN / YELLOW / RED with one-line rationale

2. MONTH SUMMARY (3 bullets):
   - What changed this month
   - Relationship health indicator
   - Key opportunity status

3. TOP SIGNALS THIS MONTH (max 3, ranked by importance)

4. RELATIONSHIP GAPS:
   - Days since last meaningful touchpoint
   - Stakeholder coverage gaps (who haven't we talked to?)
   - Competitor risk level: LOW / MEDIUM / HIGH

5. NEXT 30-DAY RECOMMENDED ACTIONS (max 3):
   - Action | Owner (Sales/Marketing) | Deadline | Expected outcome

6. EXECUTIVE SUMMARY (Chinese, 100 words, suitable for sending to sales manager)
```

---

## 4. Pre-Visit Brief

> **Auto-triggered when sales logs a visit in CRM. Zero extra work for sales rep.**

### 📋 Prompt 4.1 — Pre-Visit Intelligence Brief

```
Generate a pre-visit brief for a Hach China sales visit.

Visit details:
- Account: [COMPANY_NAME]
- Contact: [NAME, TITLE]
- Visit date: [DATE]
- Visit purpose: [STATED PURPOSE OR "Routine relationship visit"]
- Sales rep: [NAME]

Background (pull from system):
- Account Intelligence Card: [LATEST VERSION]
- Last visit summary: [DATE + NOTES]
- Open opportunities: [LIST]
- Recent signals (past 30 days): [SIGNAL DIGEST]

Generate:

1. CONTACT BRIEF (for [CONTACT NAME])
   - Role and influence level
   - Known priorities and pain points
   - Last interaction summary
   - Personal notes (if any in CRM)

2. ACCOUNT STATUS SNAPSHOT
   - 3 most important things happening at this account right now

3. SUGGESTED AGENDA (for a 45-60 min visit)
   - Opening (relationship / what's new with them)
   - Business discussion points
   - Product/solution to introduce (based on white space)
   - Ask / next step to confirm before leaving

4. TALKING POINTS (3-5 bullets)
   - Each linked to a known pain point or signal

5. THINGS TO AVOID / SENSITIVITIES

6. IDEAL OUTCOME OF THIS VISIT

Output in Chinese. Keep it concise — fits on one printed page.
```

---

## 5. Competitive Intelligence Capture (Post-Visit)

### 📋 Prompt 5.1 — Post-Visit Debrief Extractor

```
A Hach China sales rep just completed a visit. Extract structured competitive intelligence from their notes.

Raw visit notes: [PASTE NOTES OR VOICE TRANSCRIPT]

Extract:
1. Competitor mentions:
   - Company name
   - Products mentioned
   - Pricing signals (if any)
   - Customer sentiment toward competitor

2. Customer pain points mentioned (new or confirmed)

3. Procurement signals:
   - Budget available? Any amounts mentioned?
   - Timeline for decision?
   - Tender expected?

4. Relationship signals:
   - Customer sentiment toward Hach
   - Key contacts' personal priorities
   - Any relationship risks

5. Recommended follow-up actions (max 3, with owner and deadline)

6. Update flags:
   - Should Account Intelligence Card be updated? What fields?
   - Any signals to escalate to Strategy team?

Output as structured JSON + 50-word summary for CRM entry.
```

---

## 6. Quarterly Deep Review

### 📋 Prompt 6.1 — Quarterly Account Strategy

```
Generate a Quarterly Account Strategy Review for Hach China A-tier account: [COMPANY_NAME]

Input:
- Full Account Intelligence Card (latest)
- Past 3 months of Monthly Pulses
- CRM: All visits, opportunities, orders in past quarter
- Competitive intelligence captured this quarter

Generate:

1. QUARTER IN REVIEW
   - Revenue vs. target
   - Relationship depth change (better/same/worse)
   - Key events that shaped the account this quarter

2. SWOT FOR THIS ACCOUNT (Hach's position)

3. OPPORTUNITY ANALYSIS
   - Top 3 opportunities for next quarter
   - Estimated value, probability, timeline
   - Key action required to advance each

4. COMPETITIVE POSITION UPDATE
   - Where are we strong? Where are we vulnerable?
   - Any displacement risk?

5. NEXT QUARTER ENGAGEMENT PLAN
   - Touchpoint cadence (visits, events, digital)
   - Stakeholder coverage plan
   - Marketing support needed (content, events, briefings)

6. RESOURCE REQUEST (if needed)
   - What does this account need that marketing should provide?

Output: PowerPoint-ready bullet format + executive summary in Chinese (150 words)
```

---

## 7. Resource Allocation Matrix

| Activity | A-tier (50) | B-tier | C-tier |
|----------|-------------|--------|--------|
| Account Intelligence Card | Full, live | Simplified | None |
| Weekly monitoring | All 50 | Top 50 B | None |
| Monthly Pulse | All 50 | Quarterly | None |
| Pre-visit brief | Every visit | On request | None |
| Post-visit debrief extraction | Every visit | Major visits | None |
| Custom content | Yes | Template | Mass |
| Quarterly strategy review | Yes | Semi-annual | None |

---

## 8. Tooling Stack (China-Compatible)

| Need | Tool |
|------|------|
| Company monitoring | 企查查 / 天眼查 alerts |
| Tender tracking | 中国政府采购网 + 招采云 |
| News monitoring | 中国水网 RSS + 仪器信息网 + 微信公众号 |
| AI drafting | Claude / GPT-4 / 文心一言 |
| Stakeholder research | LinkedIn + 脉脉 |
| CRM | Salesforce (Hach CN standard) |
| Signal digest delivery | WeChat Work (企业微信) bot |

---

## 9. Success Metrics

| Metric | Before AI | Target |
|--------|-----------|--------|
| Time to build account profile | 2-3 days | < 2 hours |
| % A accounts with fresh intel | Ad hoc | 100% monthly |
| Sales prep time per visit | 30-60 min | < 10 min |
| Competitive signal response | Weeks | Days |
| Marketing touchpoint coverage | Low | 100% A accounts quarterly |

---

## Pilot Plan

| Week | Action |
|------|--------|
| 1-2 | Select 10 A accounts, run Prompt 1.1 + 1.2, generate Account Cards |
| 3 | Share cards with sales reps, collect feedback |
| 4 | Set up weekly monitoring workflow (Prompt 2.1) for 10 accounts |
| Month 2 | Expand to all 50 A accounts |
| Month 3 | Integrate pre-visit brief into CRM trigger workflow |

---
*Living document. Update as you learn what signals matter most for Hach China A accounts.*
