# Integrations

## Hardware

### Currency counters

- **Cummins Allison JetScan** — RS-232/USB/Ethernet; proprietary protocol (SDK ~$2k). Data: bill count, denomination, rejects.
- **Glory GFS-120** — USB/Ethernet; Glory GCOM protocol (documented).
- **Giesecke+Devrient 2250** — High-end; vendor API/SDK.
- **Approach:** Direct serial/USB on count room PC, or vendor middleware exposing REST; capture count + denomination for each drop.

### Barcode scanners

- **Zebra DS4308**, **Honeywell Voyager 1200g** — USB HID (keyboard wedge). Scan = text input; app listens for barcode (drop box ID, bag ID, rack ID).

### Chip counters / sorters

- **Glory GFR-100** — RFID chips; Ethernet; vendor SDK.
- **Shufflemaster ChipTrak** — Vision-based; REST.
- Many properties: manual count with dual entry in app (two employees enter, must match).

### RFID (drop boxes / racks)

- **Zebra FX9600** (fixed), **MC3300** (handheld) — LLRP or vendor API. Auto-identify box/rack without barcode.

### Weight scales

- Industrial (Mettler Toledo, Ohaus); RS-232/USB. Weigh drop box; flag if &lt;100g (empty/suspicious).

### Biometric access

- **HID DigitalPersona**, **Suprema BioStation** — REST/webhooks. Enforce dual control (e.g. two people to start count).

---

## Slot management systems (meter / expected count)

- **IGT Advantage** — SDS SOAP or direct DB (Oracle/SQL Server) for meter readings. 40–80 hrs.
- **Aristocrat Oasis 360** — REST or SOAP; direct DB. 60–100 hrs.
- **Everi CMS** — SOAP. 40–60 hrs.
- **Konami Synkros** — REST. 30–50 hrs.
- **Acres Foundation** — REST, webhooks. 20–40 hrs.

**Use:** Expected $ per drop box (machine ID) for variance calculation.

---

## Table management

- **Shufflemaster (Light & Wonder)** Fusion, TableLink — REST; drop, fills, credits.
- **Tangam** TableEye, ChipTrak — REST.
- **TCSJOHNHUXLEY** Blaze, Chipper — vendor API.
- 40–80 hrs each for fill/credit and table inventory.

---

## Accounting

- **QuickBooks** — REST (OAuth). Export journal entries.
- **SAP / Oracle Cloud ERP** — SOAP/REST. 80–200 hrs depending on version.

---

## Surveillance (VMS)

- **Genetec Security Center** — C# SDK or REST; trigger record, bookmark, get clip URL. 60–100 hrs.
- **Milestone XProtect** — REST. 50–80 hrs.

**Use:** “View Video” for transaction/count timestamp; variance investigation clips.

---

## Armored car

- **Brinks / Loomis / Garda** — Email/EDI or vendor API (e.g. Loomis Connect) for manifests and receipts. 20–40 hrs if API exists.

---

## Gaming commission portals

- **Nevada GCB** — Web upload (no public API as of 2025); export to their template.
- **NJ DGE / MI MGCB** — Web portals; build adapters for one-click submit when APIs available.

---

## Our own systems

- **Marker-TITO-replacement** — Validate/void ticket on redemption at cage; optional account credit on redeem.
- **Account-system** — Player account for markers (credit limit), optional balance for loads and cash-out.
