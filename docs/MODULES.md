# The 8 Core Modules

## Module 1: Soft Count (Bill Counting & Reconciliation)

**Hardware:** Currency counters (Cummins JetScan, Glory GFS, G+D 2250), barcode scanners (drop box ID), RFID/weight scales (optional).

**Workflow:**

1. **Pre-count** — Generate count sheet (all drop boxes from slot system); assign team; dual control lock.
2. **Drop box receipt** — Scan cart/route, scan each box, weigh (flag if empty/suspicious), chain of custody.
3. **Counting** — Scan box → software shows expected meter; run bills through counter; **auto-capture count** (USB/serial or manual confirm); show **variance** (expected vs. actual); flag if >threshold.
4. **Variance workflow** — Auto-create case; assign to slot ops; link to surveillance; trend (“short 7 days”); close with notes for audit.
5. **Bag and tag** — Tamper-evident bag, barcode; scan → link bag to machine/count/date.
6. **End of count** — Soft count report, variance report, export to accounting/slot system, submit to commission.

**Key features:** Dual control, surveillance integration, real-time variance alerts, trend analysis.

---

## Module 2: Hard Count (Coin/Token)

Rare (most properties use TITO). Same idea as soft count but for coins: counter/sorter, capture count, reconcile to meter.

---

## Module 3: Cage (Cashier Window)

**Hardware:** Bill/coin dispensers, chip sorters, TITO validators (IGT, Aristocrat), printers.

**Workflow:**

- **Shift start** — Cashier login (biometric+PIN); vault issues drawer (imprest); software logs opening balance.
- **Transactions** — Chip redemption, TITO redemption (validate via ticket system API, then void), cash-for-chip, markers (with credit check, manager override if >$5k). Each transaction updates drawer balance in real time.
- **Shift end** — Expected closing (opening ± all transactions); cashier counts drawer; **variance** (over/short); supervisor review; sign-off.
- **Cage reconciliation** — Aggregate all cashier variances; net cage variance; export to accounting.

**Key features:** Real-time drawer balance, transaction audit trail, variance flagging, dual auth for high-value, integration with player tracking and TITO.

---

## Module 4: Vault Management

**Hardware:** Currency/chip counters, scales, barcode, biometric access.

**Workflow:**

- **Opening** — Dual control; expected opening from prior close; spot-check bags/racks.
- **Fills** — Pit requests fill (table, amount); vault approves; prepare and barcode rack; security to table; dealer/pit scan (dual control); vault balance −.
- **Credits** — Table returns chips; vault receives, scans; vault balance +.
- **Armored car** — Prepare bags; scan manifest; log pickup; vault balance −; optional API to carrier.
- **Cage replenishment** — Cage requests; vault issues; cage receipt; vault −, cage +.
- **Closing** — Expected closing (formula); physical count; **variance**; investigate; sign-off.

**Key features:** Real-time inventory, fill/credit approval workflow, dual control, variance alerts, optional armored-car integration.

---

## Module 5: Table Games Inventory

**Formula:** `Opening float + Fills − Credits + Drop − Closing float = Win (or Loss)`.

**Tracking:** Opening float by table; fills/credits (from vault module); drop (from table/count); closing float. Auto win/loss; flag anomalies (e.g. table lost $15k vs. $8k average).

**Integrations:** Table management (Shufflemaster, Tangam, TCSJOHNHUXLEY) for drop and optional float.

---

## Module 6: Compliance & Audit Reporting

**Typical commission requirements:**

- Daily slot drop (by machine, bank, denomination, variance).
- Daily table report (by table, game, shift).
- Monthly GGR.
- Annual variance report (>$500, root cause, corrective action).
- Ad-hoc (e.g. who worked count room on date X; all fills to table Y in quarter).

**Features:** One-click report generation, format to commission spec, digital submit (where portals exist), tamper-proof storage, 7-year retention.

---

## Module 7: Surveillance Integration

**VMS:** Genetec, Milestone, March, Avigilon.

**Use cases:**

- Count room: bookmark “count started”; on variance, create clip (machine, time window).
- Cage dispute: “View Video” for transaction timestamp → open VMS at camera + time.
- Fill/credit: bookmark unusual fill; vault access audit (who entered when).

**Features:** Trigger record/bookmark, retrieve clip URL, “View Video” from app by transaction/case.

---

## Module 8: Analytics & BI Dashboard

**For CFO / Controller:**

- Slot: total drop, by denom, variance %, top/bottom machines.
- Table: win by game, hold %, best/worst tables.
- Cage: transaction counts, chip/TITO redemptions, markers, cashier variance summary.
- Vault: cash/chip on hand, fills/credits, armored car.
- Alerts: critical (e.g. machine short 7 days), warning (unusual fills), info (over/short within tolerance).

**Trends:** Drop/win over 30/90 days; variance and over/short trends.
