# Tech Stack (2025)

## Backend

- **API:** FastAPI (Python) or Node.js + NestJS (TypeScript). Async, fast, auto-docs.
- **Database:** PostgreSQL (primary). ACID for money; transactions, balances, audit. Managed: AWS RDS, Neon, Supabase.
- **Time-series:** TimescaleDB (Postgres extension) for counts, meter reads, trend analysis.
- **Cache:** Redis — current vault balance, cage drawer balances, low-latency reads.
- **Events:** Apache Kafka or AWS Kinesis — count room produces 2k+ events per run; real-time processing and downstream reporting.
- **Queue:** RabbitMQ or AWS SQS — fill requests, notifications, async jobs.
- **Storage:** AWS S3 — compliance docs, reports, backups; 7-year retention, versioning, WORM where required.

## Frontend

- **Web (CFO, compliance, ops):** React + TypeScript, Tailwind, shadcn/ui, Recharts or ECharts, React Query.
- **Mobile (count room, vault, cage):** React Native or Flutter. Barcode scan, offline-capable, dual-control flows, push for variance alerts.
- **Kiosk:** Locked-down tablets (iPad/Windows) running app full-screen for count room terminals.

## Infrastructure

- **Cloud:** AWS (SOC 2, PCI DSS). RDS, S3, Lambda, ECS/EKS.
- **Containers:** Docker; orchestration: EKS or ECS/Fargate.
- **CI/CD:** GitHub Actions — build, test, deploy.
- **Monitoring:** Datadog (metrics, logs, APM); alerts e.g. variance &gt;$500. Sentry for errors.
- **Security:** Encryption at rest (KMS), TLS 1.3, secrets in AWS Secrets Manager. Full audit logging (who, what, when, IP). SOC 2 Type II, annual pentest.

## Security / compliance

- **SOC 2 Type II** — Required for casino/accounting (e.g. Prescient Assurance).
- **Penetration testing** — Annual (e.g. Bishop Fox, NCC Group).
- **Audit trail** — Every balance change and material action logged; immutable where required by regulation.
