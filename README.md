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
├── src/                # Backend / APIs / integrations (to be implemented)
├── .gitignore
└── LICENSE
```

## Related Repos

- **[Marker-TITO-replacement](https://github.com/lorddummy/Marker-TITO-replacement)** — Paperless ticket/voucher system (cash-out → digital ticket)
- **[Account-system](https://github.com/lorddummy/Account-system)** — Player account + card-in/session + balance (works in parallel with tickets)

This repo handles **count room, cage, and vault** (the house’s cash/chip flow and reconciliation). Ticket and account systems handle **player-facing** vouchers and balances.

## Status

**Early stage.** This repo holds the 2025 playbook (architecture, modules, integrations, GTM) and will hold the implementation. Target: cloud-native, mobile-first, real-time variance alerts, surveillance integration, compliance-as-a-service.

## License

See [LICENSE](LICENSE).
