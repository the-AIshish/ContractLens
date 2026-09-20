# ContractLens — Commercial Governance Platform

A Streamlit-based enterprise contract governance dashboard for monitoring, analyzing, and actioning commercial agreements.

## Features

- **Executive Overview** — Portfolio health KPIs, managed value, unmitigated risk exposure, and 30-day milestone horizon
- **Agreements & Commitments** — Contract ingestion workflow, dual-pane commitment register with live source-grounded evidence drawer, and pre-filled pushback email drafts per clause
- **Change Intelligence** — Side-by-side baseline vs. supplier counter-draft comparison with commercial risk readings and recommended playbook responses
- **Decision Copilot** — Natural-language Q&A with clause-cited grounded answers across §§2.2, 3.1, 4.2, and 5.2
- **Operational Assurance** — Evidence ledger (Audit feed / Review gates toggle), governance posture card, and unit execution cost metrics

## Quick Start

```bash
# Install dependencies
pip install streamlit

# Run the app (Python 3.14 — disable file watcher to avoid watchdog crash)
py -m streamlit run app.py --server.fileWatcherType none
```

Open (https://contractlens-vropmhypenrblamsgcyhvc.streamlit.app/) in your browser.

## Sample Data

The repository includes two sample contract documents:

- `base_sourcing_agreement.txt` — Auric Consumer Brands baseline MSA (Buyer-favorable)
- `supplier_redline_counter.txt` — Pacific Rim Formulations counter-draft with redlined changes

Upload either file via the **Agreements & Commitments** ingestion panel to trigger the status pipeline.

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) + [Newsreader](https://fonts.google.com/specimen/Newsreader) — Typography
- Python standard library only (no external AI/LLM dependencies in this version)

## Project Structure

```
contractlens/
├── app.py                        # Main Streamlit application
├── base_sourcing_agreement.txt   # Sample baseline contract
├── supplier_redline_counter.txt  # Sample supplier counter-draft
└── README.md
```
