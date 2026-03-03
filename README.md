# Count Room / Cage / Vault Automation & Reconciliation

**The single most under-served, highest-margin, stickiest software category in casino tech.**

- Every casino loses **$50k–$500k+ per year** to counting errors, theft, and reconciliation labor
- Count room operations are **the #1 audit focus** for gaming commissions (any discrepancy = massive fines + license risk)
- Existing software is **30+ years old** (AS/400 green screens, Windows XP apps)
- Once you're managing their money, **they cannot rip you out** (too risky, too integrated with accounting)
- **Deal sizes:** $200k–$2M per property (one-time) + $50k–$300k/year (SaaS/support)
- Buyers have budget authority and regulatory pressure to upgrade **now**

## What This Is

End-to-end **Count Room**, **Cage**, and **Vault** automation and reconciliation software:

1. **Soft count** — Bill counting from slot/table drop boxes, variance vs. electronic meters, bag & tag, audit trail
2. **Cage** — Cashier drawer management, TITO redemption, chip redemption, markers, shift balancing
3. **Vault** — Fills & credits, armored car, cage replenishment, daily reconciliation
4. **Table games inventory** — Opening float, fills, credits, drop, win/loss
5. **Compliance & audit** — Gaming commission reports, variance reporting, 7-year retention
6. **Surveillance integration** — One-click video for disputes and variance investigation
7. **Analytics & BI** — Real-time dashboards for CFO, variance alerts, trend analysis

## Money Flow (Where This Software Fits)

```
Slot/Table DROP → COUNT ROOM (soft count) → VAULT → Armored car / Bank
                         ↓
CAGE (cashiers) ←→ VAULT (fills, replenishment)
                         ↓
              Accounting / Compliance / Gaming Commission
```

## Repo Structure

```
Count-Room-Cage-Vault-Automation/
├── README.md           # This file
├── docs/               # Playbook: architecture, modules, integrations, GTM, tech stack
├── backend/            # Working API and dashboard
│   ├── app/            # FastAPI app, models, routers, seed
│   ├── static/         # Dashboard (HTML/JS)
│   └── requirements.txt
├── src/                # Additional modules / integrations (future)
├── .gitignore
└── LICENSE
```

## Run the application

**Requirements:** Python 3.10+

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API:** http://localhost:8000  
- **Interactive docs:** http://localhost:8000/docs  
- **Dashboard:** http://localhost:8000/static/dashboard.html  

On first run, the app creates the SQLite database and seeds a demo property, drop boxes, cashiers, tables, and an opening vault balance. Use the API or dashboard to run count sessions, open/close cage drawers, record vault transactions, table inventory, and compliance reports.

## Related Repos

- **[Marker-TITO-replacement](https://github.com/lorddummy/Marker-TITO-replacement)** — Paperless ticket/voucher system (cash-out → digital ticket)
- **[Account-system](https://github.com/lorddummy/Account-system)** — Player account + card-in/session + balance (works in parallel with tickets)

This repo handles **count room, cage, and vault** (the house’s cash/chip flow and reconciliation). Ticket and account systems handle **player-facing** vouchers and balances.

## Status

**Working MVP.** This repo includes a runnable FastAPI backend and dashboard for count room (sessions, drop boxes, count results, variances), cage (cashiers, drawers, transactions, reconciliation), vault (balance, transactions, reconciliation), table inventory (win/loss), and compliance reports (daily slot drop, daily table, variance report). Target next: cloud-native deploy, real-time variance alerts, surveillance integration, commission submission.

## License

See [LICENSE](LICENSE).
