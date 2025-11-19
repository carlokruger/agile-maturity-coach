# Agile Coaching Backlog Generator

The **Agile Coaching Backlog Generator** is a command-line tool that transforms
Agile Maturity Assessment scores into a concrete, actionable **coaching backlog**.

Instead of vague maturity heat-maps, this tool produces:

- Coaching backlog items
- Root cause analysis
- Suggested coaching interventions
- Working agreement proposals
- Success measures

Only behaviours scored **1 (Chaotic)** or **2 (Emerging)** generate backlog items.

This enables Agile Coaches, Scrum Masters, Delivery Leads, and Engineering Managers
to convert maturity assessments into practical improvement work that teams can action
immediately.

---

## ✨ Features

- Behaviour-based maturity model input  
- Automatic mapping from symptoms → interventions  
- CSV-to-CSV transformation  
- Generates concrete coaching backlog items  
- Helps teams identify systemic improvement opportunities  
- Supports structured coaching programmes  

---

## 📦 Project Structure

├── coaching_backlog_generator.py     # Main CLI tool

├── assessment.csv                    # Full behaviour-based assessment model (L1–L5 statements)

├── team_scores.csv                   # Example team scoring template

└── README.md                         # Documentation

You can rename or reorganise as you see fit.

---

## 📥 Input Files

### **1. Assessment Model (assessment.csv)**

This file contains the full behaviour-based Agile Maturity Model with all 45–50 behaviours,
each with L1–L5 behavioural descriptions.

Example:

| Category | Statement | L1 | L2 | L3 | L4 | L5 |
|----------|-----------|----|----|----|----|-----|
| Flow & Delivery | Forecasting uses historical data | Forecasts are guesses or commitments. | Some data used inconsistently. | … | … | … |
| Team Dynamics | Mistakes are discussed openly | … | … | … | … | … |

This file defines the **symptoms** that map to coaching interventions.

---

### **2. Team Scores (team_scores.csv)**

This is a CSV containing how a single team scored each behaviour.

Example:

| Statement | Score |
|-----------|-------|
| Forecasting uses historical data | 1 |
| Work in progress is visible and actively managed | 3 |
| The team works from a clear product vision… | 2 |

- **Score** must be an integer from **1–5**.
- Only **1 or 2** generate coaching backlog items.

---

## 🚀 Usage

Ensure that Python 3 is installed.

Run the generator:
python3 coaching_backlog_generator.py assessment.csv team_scores.csv backlog.csv

This produces a `backlog.csv` file containing:

- Symptom  
- Root Cause  
- Coaching Intervention  
- Working Agreement  
- Success Measures  

This file can be imported directly into:

- Jira  
- Trello  
- Clubhouse/Shortcut  
- GitHub Projects  
- Notion  
- Confluence  
- Miro  

---

## 📄 Output Example

A generated backlog item looks like:
Statement: Forecasting uses historical data
Symptom: Forecasts are guesses or commitments.
Root Cause: Lack of flow literacy; dates treated as promises.
Intervention: Teach Monte Carlo forecasting + confidence ranges. Facilitate a forecasting workshop.
Working Agreement: “We never give single-date commitments.”
Success Measures: Forecast accuracy improves; fewer surprises; stakeholder trust increases.

Backlog items are intentionally:

- Behavioural  
- Measurable  
- Coachable  
- Actionable  

---

## 🎯 Purpose

Many Agile assessments produce insights but not **interventions**.

This tool bridges that gap by:

- Converting assessment findings into a backlog of coaching actions  
- Providing structured, consistent improvement pathways  
- Reducing ambiguity in team development  
- Helping coaches scale their impact across multiple teams  

---

## 🛣️ Roadmap

Future enhancements may include:

- Markdown output support  
- Jira ticket auto-generation  
- Web-based UI  
- Dashboard visualisations (radar charts, heat-maps)  
- Priority scoring for coaching backlog items  
- Plugin system for extending the coaching library  
- API endpoints for integrations  

Contributions and suggestions are welcome.

---

## 🤝 Contributing

Pull requests are welcome.

To contribute:

1. Fork the repo  
2. Create a feature branch  
3. Submit a PR with a clear explanation  
4. Ensure behaviour mappings and CSV formats remain consistent  

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📚 Acknowledgements

This project is built on a comprehensive behaviour-based Agile Maturity Model
and coaching intervention library designed to turn team assessments into
actionable, measurable improvements for real-world teams.
