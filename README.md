# Clinical Research Intake Structurer

[![Run Unit Tests](https://github.com/lthom1180/clinical-intake-structurer/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/clinical-intake-structurer/actions/workflows/test.yml)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blueviolet.svg)
![Accessibility](https://img.shields.io/badge/WCAG-2.1%20AA%20Compliant-success.svg)

A lightweight, high-performance web application designed to parse unstructured clinical trial notes and extract schema-validated eligibility criteria. Built with **FastAPI**, **Pydantic**, **SQLAlchemy**, and the **Google GenAI SDK**, this tool bridges the gap between unstructured clinical data and structured relational storage.

---

## 🏗️ Architectural & Design Decisions

When engineering data-pipeline tools for research and healthcare environments, data integrity, security, and developer ergonomics are paramount. This application implements several key architectural patterns:

* **Strict Schema Validation (Pydantic):** Unvalidated LLM output introduces data corruption risks. By enforcing explicit Pydantic models (`ClinicalCriteriaExtraction`) and utilizing the Gemini API's `response_schema`, the application guarantees that extracted outputs adhere strictly to expected types before persistence—eliminating fragile regex parsing and reducing hallucination risks.
* **Persistent Relational Storage (SQLAlchemy + SQLite):** Extracted criteria are serialized and saved to a robust SQL database layer, providing researchers with an audit trail and historical record of processed notes.
* **Zero-Friction "Demo Mode":** To allow evaluators and hiring teams to test the app instantly without configuring paid API keys, the backend includes an intelligent fallback service. If `GEMINI_API_KEY` is omitted or set to `demo`, the app returns deterministic, realistic mock extractions based on keyword analysis.
* **Cloud-Ready Containerization:** The application is fully containerized using a multi-stage-friendly `Dockerfile` and `docker-compose`. Crucially, the container runs under a **non-root user (`appuser`)**, ensuring strict security compliance required by enterprise orchestration platforms like **OpenShift and Kubernetes**.

---

## ♿ Accessibility (WCAG 2.1 AA Standards)

Research and clinical software must be equitable and accessible to all users. The single-page frontend (`static/index.html`) is built from the ground up to meet **WCAG 2.1 AA** digital accessibility standards:
* **Semantic HTML & Form Associations:** Every input field is explicitly tied to a descriptive `<label>`, avoiding ambiguous placeholder-only designs.
* **Screen Reader & Live Updates:** Status messages and asynchronous extraction updates are wrapped in ARIA live regions (`aria-live="polite"`) to announce state changes to assistive technologies.
* **Keyboard Navigation & Contrast:** Features high-contrast color ratios, visible custom focus rings, and logical tab indexing.

---

## 🚀 Quick Start (Docker Compose)

The fastest way to run the application locally is via Docker Compose—no local Python environment required.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/clinical-intake-structurer.git](https://github.com/YOUR_GITHUB_USERNAME/clinical-intake-structurer.git)
   cd clinical-intake-structurer
