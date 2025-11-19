#!/usr/bin/env python3
import csv
import sys
import argparse
from pathlib import Path

# ---------------------------
# Coaching cheat-sheet library
# ---------------------------

COACHING_LIBRARY = {
    "No vision exists or it's ignored; work is task-driven.": {
        "root": "Team is shipping tasks, not outcomes. Leadership hasn't articulated direction or made it relevant.",
        "intervention": "Facilitate a Product Vision Workshop (users, problem, outcomes, anti-goals). Link epics to vision.",
        "agreement": "We check all new work against our product vision.",
        "success": "Vision referenced in ceremonies; team can explain purpose; fewer zombie backlog items."
    },
    "Stories are task lists with no value.": {
        "root": "Team focuses on tasks, not outcomes or user value.",
        "intervention": "Run a Value-First Story Writing workshop. Rewrite stories using value-based templates.",
        "agreement": "Every story includes a measurable outcome.",
        "success": "ACs reference outcomes; PO slices by outcome; task-only stories disappear."
    },
    "Decisions rely on opinion or seniority.": {
        "root": "Lack of data literacy or usable feedback loops.",
        "intervention": "Run a Data Discovery Day (analytics, support tickets, heatmaps). Identify top insights.",
        "agreement": "We use evidence for all major decisions.",
        "success": "Fewer opinion standoffs; team references data; backlog ordering becomes data-driven."
    },
    "Priorities shift due to external pressure.": {
        "root": "No prioritisation discipline; stakeholder chaos.",
        "intervention": "Teach WSJF-lite or cost-of-delay. Coach PO on confident boundary setting.",
        "agreement": "We prioritise based on value and learning, not noise.",
        "success": "Mid-sprint changes drop; roadmap stabilises; better stakeholder alignment."
    },
    "Done means deployed; no follow-up.": {
        "root": "Team sees delivery as the end instead of learning.",
        "intervention": "Introduce monthly Impact Review sessions. Track real usage and outcomes.",
        "agreement": "We check outcomes after each release.",
        "success": "Backlog evolves post-release; bad ideas killed earlier; better alignment to value."
    },

    # TEAM DYNAMICS
    "Issues hidden; fear dominates.": {
        "root": "Lack of psychological safety; unpredictable leadership reactions.",
        "intervention": "Run a Safety Check + anonymised retro. Coach leaders on non-reactive listening.",
        "agreement": "We raise issues early without fear.",
        "success": "More risks surfaced; deeper retros; calmer team behaviour."
    },
    "Blame and secrecy.": {
        "root": "Shame culture or fear of mistakes.",
        "intervention": "Introduce blameless postmortems. Focus on systems, not people.",
        "agreement": "We treat mistakes as learning signals.",
        "success": "More experimentation; less defensiveness; faster improvements."
    },
    "Work siloed; bottlenecks common.": {
        "root": "Knowledge monopolies and lack of pairing habits.",
        "intervention": "Run Skill Sharing Week. Pair rotations + knowledge map.",
        "agreement": "No one person owns critical areas alone.",
        "success": "Higher bus factor; smoother flow; faster onboarding."
    },
    "Conflicts ignored or explosive.": {
        "root": "Avoidance or no conflict resolution skills.",
        "intervention": "Teach Nonviolent Communication. Facilitate conflict mediations.",
        "agreement": "We address friction early with honesty.",
        "success": "Fewer blow-ups; faster resolution; healthier team tone."
    },
    "Frequent overtime and burnout.": {
        "root": "Overcommitment; poor forecasting; uncontrolled WIP.",
        "intervention": "Sustainable Pace Reset. Analyse causes; set hard limits.",
        "agreement": "We do not trade health for speed.",
        "success": "Less overtime; steadier flow; improved morale."
    },

    # FLOW & DELIVERY
    "Hidden work; unlimited WIP.": {
        "root": "Lack of transparency and flow mind-set.",
        "intervention": "Introduce strict WIP limits. Run daily flow review.",
        "agreement": "We finish work before starting more.",
        "success": "Cycle time drops; fewer multitasking issues; honest board."
    },
    "No metrics used.": {
        "root": "Fear of exposure or lack of literacy.",
        "intervention": "Create dashboards (cycle time, throughput, work profile). Weekly Flow Review.",
        "agreement": "We inspect flow data weekly.",
        "success": "Higher predictability; fewer surprises; better retros."
    },
    "Bottlenecks persist.": {
        "root": "Local optimisation; lack of systemic thinking.",
        "intervention": "Do Value Stream Mapping. Target one bottleneck per 2 weeks.",
        "agreement": "When stuck, we swarm.",
        "success": "Faster unblock times; smoother end-to-end flow."
    },
    "Forecasts are guesses or commitments.": {
        "root": "Lack of flow literacy; dates treated as promises.",
        "intervention": "Teach Monte Carlo forecasting + ranges. Run forecasting workshop.",
        "agreement": "We never give single-date commitments.",
        "success": "Forecast accuracy improves; stakeholder trust rises."
    },
    "Large items dominate; big bang.": {
        "root": "Poor slicing habits; weak refinement.",
        "intervention": "Run Story Splitting Dojo (12 slicing patterns).",
        "agreement": "Stories must be finishable within a few days.",
        "success": "Shorter cycle time; faster learning loops."
    },

    # TECHNICAL EXCELLENCE
    "Little/no automation; painful regression.": {
        "root": "Fear or lack of testing skills.",
        "intervention": "Start Golden Path Testing (automate top 3 flows).",
        "agreement": "We automate critical paths first.",
        "success": "Regression bugs drop; safer deployments."
    },
    "Refactoring avoided.": {
        "root": "Low confidence due to no tests.",
        "intervention": "Daily Improvement Time + top 5 hotspot list.",
        "agreement": "We leave code cleaner than we found it.",
        "success": "Complexity decreases; cleaner diffs; fewer hot spots."
    },
    "Individuals work alone.": {
        "root": "Anti-collaboration habits or ego.",
        "intervention": "Mob Fridays + pairing rotation.",
        "agreement": "We pair on complex or risky work.",
        "success": "Faster problem solving; knowledge spread."
    },
    "Manual and risky deployments.": {
        "root": "No CI/CD discipline.",
        "intervention": "Build automated deployment pipeline stage by stage.",
        "agreement": "Every change passes through CI.",
        "success": "Higher deploy frequency; lower failure rate."
    },
    "Reviews slow or hostile.": {
        "root": "Gatekeeping or unclear standards.",
        "intervention": "Healthy Code Review Habits workshop.",
        "agreement": "Reviews focus on learning, not policing.",
        "success": "Higher review speed; better tone; improved code quality."
    },

    # DISCOVERY
    "No validation.": {
        "root": "Delivery-first culture.",
        "intervention": "Assumption Mapping + Lean UX loops.",
        "agreement": "We test assumptions before building.",
        "success": "Less waste; more validated learning."
    },
    "Usability ignored.": {
        "root": "Design downstream or absent.",
        "intervention": "Design Crit Fridays; shift-left design.",
        "agreement": "UX engaged before development.",
        "success": "Fewer UX issues; happier users."
    },
    "Discovery only upfront.": {
        "root": "Waterfall habits.",
        "intervention": "Dual-track discovery rhythm.",
        "agreement": "Discovery runs in parallel with delivery.",
        "success": "Better decisions; fewer surprises."
    },
    "Assumptions implicit.": {
        "root": "Uncertainty not surfaced.",
        "intervention": "Hypothesis writing training.",
        "agreement": "We make assumptions explicit.",
        "success": "Cleaner outcomes; tighter feedback loops."
    },
    "No design thinking.": {
        "root": "Design seen as decoration.",
        "intervention": "Problem Framing Workshop.",
        "agreement": "We explore options before choosing solutions.",
        "success": "Better solutions; less rework."
    },

    # WAYS OF WORKING
    "Events skipped or hollow.": {
        "root": "People don’t know the purpose.",
        "intervention": "Purpose Reset for ceremonies.",
        "agreement": "Every event must produce a decision.",
        "success": "Shorter meetings; clearer outcomes."
    },
    "No retros.": {
        "root": "Fear or cynicism.",
        "intervention": "Introduce 10-minute rapid retros.",
        "agreement": "We inspect and adapt every sprint.",
        "success": "More improvements; deeper trust."
    },
    "Agreements ignored.": {
        "root": "Too vague or aspirational.",
        "intervention": "Rewrite agreements as behaviours.",
        "agreement": "We update agreements monthly.",
        "success": "Less friction; more consistency."
    },
    "Impediments ignored.": {
        "root": "No tracking or escalation discipline.",
        "intervention": "Use an Impediment Kanban. Clear 1/week.",
        "agreement": "We track and clear impediments weekly.",
        "success": "Flow improves; fewer frustrations."
    },
    "Chaotic cadence.": {
        "root": "Poor planning discipline.",
        "intervention": "Rebuild team cadence with clear inputs/outputs.",
        "agreement": "We follow a predictable rhythm.",
        "success": "Less chaos; more stable flow."
    },

    # LEADERSHIP
    "Leaders cause impediments.": {
        "root": "Misalignment or misunderstanding.",
        "intervention": "Leader Enablement Session.",
        "agreement": "Leaders remove impediments within 5 days.",
        "success": "Faster unblock times; calmer team."
    },
    "Constant interruptions.": {
        "root": "Stakeholder pressure or weak boundaries.",
        "intervention": "Introduce Intake Policies.",
        "agreement": "Interruptions go through the PO.",
        "success": "Fewer interruptions; higher sprint completion."
    },
    "Project-based churn.": {
        "root": "Old governance model.",
        "intervention": "Create Value Team Funding Proposal.",
        "agreement": "Stable teams are default.",
        "success": "Lower attrition; steadier velocity."
    },
    "Leaders act waterfall.": {
        "root": "Habit or fear.",
        "intervention": "Shadow + behaviour coaching.",
        "agreement": "Leaders model curiosity and learning.",
        "success": "More autonomy; fewer escalations."
    },
    "Governance blocks iteration.": {
        "root": "Waterfall compliance assumptions.",
        "intervention": "Redesign governance to support increments.",
        "agreement": "Governance enables delivery.",
        "success": "Shorter lead time; fewer blocked releases."
    },

    # ARCHITECTURE
    "Changes break things regularly.": {
        "root": "Poor architectural understanding.",
        "intervention": "Architecture 101 sessions + pairing.",
        "agreement": "We understand changes before we make them.",
        "success": "Fewer incidents; safer deployments."
    },
    "Architecture dictated.": {
        "root": "Top-down control.",
        "intervention": "Introduce ADRs with team participation.",
        "agreement": "Architecture decisions are collaborative.",
        "success": "Better designs; greater buy-in."
    },
    "Big-bang rewrites.": {
        "root": "Lack of incremental techniques.",
        "intervention": "Teach Strangler Fig pattern.",
        "agreement": "We evolve architecture incrementally.",
        "success": "Lower risk; smoother releases."
    },
    "Strategy unknown.": {
        "root": "Poor communication.",
        "intervention": "Create Technology Radar.",
        "agreement": "Technical strategy is visible.",
        "success": "Better alignment; fewer conflicting designs."
    },
    "Risks discovered too late.": {
        "root": "No risk scanning habit.",
        "intervention": "Introduce risk-based planning.",
        "agreement": "We surface risks every planning session.",
        "success": "Fewer surprise failures."
    },

    # DEPENDENCIES
    "Hidden dependencies cause chaos.": {
        "root": "No visibility across teams.",
        "intervention": "Create dependency map.",
        "agreement": "We expose dependencies immediately.",
        "success": "Fewer surprises; faster coordination."
    },
    "Plans in isolation.": {
        "root": "No aligned cadence.",
        "intervention": "Quarterly Big Room Planning Lite.",
        "agreement": "We plan together for shared goals.",
        "success": "Higher coordination; fewer clashes."
    },
    "Regular blocking by other teams.": {
        "root": "Poor collaboration patterns.",
        "intervention": "Create service-level expectations.",
        "agreement": "We respond to requests within agreed time.",
        "success": "Faster unblock; better relationships."
    },
    "Ownership unclear.": {
        "root": "Lack of clarity.",
        "intervention": "Define ownership model (RACI/Team API).",
        "agreement": "Every shared component has an owner.",
        "success": "Fewer delays; clearer responsibilities."
    },
    "No value stream understanding.": {
        "root": "Local optimisation mindset.",
        "intervention": "Value Stream Mapping workshop.",
        "agreement": "We optimise system flow.",
        "success": "Lower lead time; fewer handoffs."
    }
}


# ------------------------------
# Backlog generator core
# ------------------------------

def generate_backlog(assessment_csv, maturity_csv, output_file):
    # Load maturity definitions to map L1 statements
    findings = []
    with open(assessment_csv, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            findings.append(row)

    # Load team's scores
    scores = []
    with open(maturity_csv, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(row)

    backlog_items = []

    for score in scores:
        statement = score["Statement"]
        level = int(score["Score"])

        if level > 2:
            continue  # Only backlog for L1 or L2

        # Find the L1 statement definition for mapping
        for finding in findings:
            if finding["Statement"] == statement:
                l1 = finding["L1"]
                break
        else:
            continue

        if l1 not in COACHING_LIBRARY:
            continue

        entry = COACHING_LIBRARY[l1]

        backlog_items.append({
            "Statement": statement,
            "Symptom": l1,
            "Root Cause": entry["root"],
            "Intervention": entry["intervention"],
            "Working Agreement": entry["agreement"],
            "Success Measures": entry["success"]
        })

    # Write backlog
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Statement", "Symptom", "Root Cause", "Intervention",
            "Working Agreement", "Success Measures"
        ])
        writer.writeheader()
        writer.writerows(backlog_items)

    print(f"Backlog generated → {output_file}")


# ------------------------------
# CLI
# ------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an Agile Coaching Backlog from a team maturity assessment."
    )
    parser.add_argument("assessment_csv", help="CSV of all assessment behaviours")
    parser.add_argument("team_scores_csv", help="Team maturity scores (Statement, Score)")
    parser.add_argument("output", help="Output CSV for generated backlog")

    args = parser.parse_args()

    generate_backlog(args.assessment_csv, args.team_scores_csv, args.output)