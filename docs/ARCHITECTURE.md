# Architecture — The Money Flow

## Casino Money Lifecycle

### 1. Slot floor → drop (daily)

- Slot machines accumulate cash (bills inserted by players)
- Slot techs do a **hard count drop**: open each machine’s drop box, collect full boxes, replace with empty, transport to **count room** on secure carts
- Bill validators track electronic count; **physical count must match**

### 2. Table games → drop (daily)

- Players buy chips with cash at tables (cash goes in drop box under table)
- Security collects table drop boxes daily (cash + fill/credit slips) → **count room**

### 3. Count room (soft count)

- **Soft count room**: 2–4 employees, dual control, cameras
- Open drop boxes one by one, count cash with **currency counters**
- Software tracks: Machine ID → Drop box → $ amount → **Variance vs. electronic meter**
- Bag and wrap cash for bank deposit

### 4. Cage (casino bank window)

- Players cash out chips, redeem TITO tickets, get markers (credit)
- Cashiers have drawers ($50k–$150k each); **cage inventory** often $500k–$5M
- End of shift: **each drawer must balance to the penny** (count vs. transaction log → over/short)

### 5. Vault (main casino bank)

- **Master vault**: $5M–$50M+ at large properties
- **Fills**: Table needs chips → vault delivers, logs transaction
- **Credits**: Table returns excess chips → vault receives
- **Soft count deposits**: Cash from count room → vault → armored car to bank
- **Daily reconciliation**: Opening + deposits − withdrawals + fills − credits = closing (must balance to the penny)

### 6. Accounting / compliance

- Daily reports: slot drop, table drop, cage over/short, vault balances, variances
- Gaming tax (e.g. GGR), compliance reporting to gaming commission

---

## Core Problems This Software Solves

| Problem | Current pain | What we do |
|--------|----------------|------------|
| **Manual data entry** | Count room types numbers into Excel/AS/400; typos cause wrong-machine attribution and variance investigations | Auto-capture from currency counters; barcode/RFID on drop boxes; digital chain of custody |
| **Variance investigation** | 5–6 hours per variance (surveillance, logs, paperwork); fines if unresolved | Auto-flag variances >threshold; link to surveillance (timestamp + machine); trend analysis (“short 7 days in a row”) |
| **Cashier balancing** | End-of-shift over/short; 2+ hours to find errors; no proof | Real-time drawer balance; transaction-level audit; link to video for disputes |
| **Fill/credit chaos** | Paper 3-part slips; manual entry; 2–4 hours to reconcile if off | Digital fill/credit requests; real-time table inventory; auto-reconciliation |
| **Vault reconciliation** | 3+ hours daily; paper slips; variance found 24 hours later | Real-time vault ledger; auto expected vs. actual; immediate variance alerts |
| **Compliance reporting** | 10–15 hours/month compiling reports; email/print to commission | One-click reports to commission spec; digital submit; 7-year retention |

---

## The 8 Core Modules

1. **Soft count** — Bill counting, drop box receipt, variance vs. meter, bag & tag, variance workflow, dual control
2. **Hard count** — Coin/token (rare now; most use TITO)
3. **Cage** — Shift start/end, drawer balance, TITO redemption, chip redemption, markers, reconciliation
4. **Vault** — Opening/closing balance, fill/credit approval and logging, armored car, cage replenishment
5. **Table games inventory** — Float, fills, credits, drop, win/loss formula and tracking
6. **Compliance & audit** — Daily/monthly reports, commission submission, ad-hoc audit, retention
7. **Surveillance integration** — Bookmark/clip by timestamp; “View Video” for disputes and variance
8. **Analytics & BI** — Dashboards (slot/table/cage/vault), variance alerts, trend analysis

See [MODULES.md](MODULES.md) for detailed workflows and features.
