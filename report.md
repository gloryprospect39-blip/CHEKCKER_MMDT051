# Project 6 Report: Myanmar Checkers AI Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Primary AI Algorithm:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** Kay
- **MMDT ID:** MMDT051

---

## Section 1: AI Agent Configuration
- **Primary AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Pruning Technique:** Alpha-Beta Pruning
- **Evaluation Heuristic Strategy:** Piece advantage, advancement, mobility, and king safety

---

## Section 2: Complexity & Evaluation Function Analysis
- **Board Configuration:** 8x8 dark-square board with 12 pieces per side, alternating diagonal movement, and mandatory capture rules for Myanmar Checkers.
- **Piece Valuation & Rules:** Plain pieces are valued at 100 points, kings at 180 points, captures remove opponent pieces by jumping over them, and promotions occur when a piece reaches the last row.
- **Heuristic Features Used:** Material balance, piece advancement toward promotion, center control, mobility, and protection of high-value pieces to favor tactical and positional strength.

---

## Section 3: Local Verification & Feature Checklist
*Check the algorithms, agents, and features you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Myanmar Checkers Game Engine & Board State Representation
- [x] Legal Move Generation and Capture Mechanics
- [x] Minimax Search Algorithm with Alpha-Beta Pruning
- [x] Rule-Based / Heuristic AI Agent
- [x] Uniform Random Baseline Agent
- [x] Interactive Web Visualizer with Playable Board & Game Feedback

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://example.com/myanmar-checkers-ai
- **Video Presentation Link:** https://drive.google.com/drive/folders/1uaPMZveDRk3ZznSX0SZNF4Tt3Xf-gz3t?usp=drive_link

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain how Alpha-Beta pruning optimizes decision-making in large-branching board games like Checkers without sacrificing tactical depth.**
    Alpha-Beta pruning reduces unnecessary search by cutting branches when a move is already worse than a previously found best option. In Checkers, this keeps the minimax tree manageable while still exploring the most promising lines deeply enough to preserve tactical threats, captures, and king promotion decisions. It makes the search much faster without ignoring the important moves that actually influence the outcome.
- **Compare classical Adversarial Search & Heuristic Evaluation in Checkers with modern Generative AI / Deep Reinforcement Learning game agents (e.g., AlphaZero, MCTS, Value Networks, Process Reward Models).**
    Classical minimax and heuristic evaluation are transparent, efficient, and easy to tune for deterministic games such as Checkers because they explicitly reason about legal moves and board value. Modern agents such as AlphaZero and MCTS learn evaluation and policy estimates from self-play, often producing stronger strategic play by recognizing patterns beyond hand-crafted features. The main trade-off is that deep learning systems require much more training data and compute, while classical search remains explainable and lightweight for smaller or custom game engines.
