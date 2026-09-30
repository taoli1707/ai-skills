# Evidence: page design for explainer pages

Research date: 2026-09-27. Read this file when you need the reason behind a page-design rule in SKILL.md, or when the reader asks "why is the page built this way?".

## Contents

1. How to read the verification tags
2. Interactivity
3. Charts
4. Tables versus charts
5. Web reading behaviour
6. Explanation structure
7. Showing logic
8. Diagrams
9. Accessibility and technical basics
10. Self-check questions
11. Uncertainty and sources
12. Gaps: what was not verified

## 1. How to read the verification tags

| Tag | Meaning |
|---|---|
| V-PDF | The paper was downloaded and the text was read. Numbers are as printed. |
| V-page | The page was opened. Numbers are reliable. Quoted wording may differ slightly. |
| V2 | Verified only through a secondary page that reports the primary source. |
| S | Seen only in a search-result snippet. Not opened. |
| R | Recalled from memory. Not verified. |

Use V-PDF and V-page findings with confidence. Treat S and R findings as unconfirmed.

## 2. Interactivity

### 2.1 Most readers do not use optional controls

Evidence (V-PDF): Conlen, Kale, Heer 2019. More than 50,000 sessions on three interactive articles.

| Article | Measure | Result |
|---|---|---|
| Dimensionality reduction (7,055 visits) | Reached the end | 76% |
| Same | Of those, clicked to view another algorithm | 59% (so 41% of "finished" readers missed content) |
| Same | Median use of the details button and the slider | 0 |
| Guitar (55,193 sessions) | Tuned all six strings | 23% |
| Same | Clicked the beat-frequency button | 14% |
| Same | Changed playback | 2% |
| Beat Basics | Used the large graphic vs the inline links | 75% vs 54% |
| Beat Basics | Median time, mobile vs desktop | 20 s vs 86 s |

Evidence (V-PDF): Archie Tse, New York Times, 2016: "If you make a tooltip or rollover, assume no one will ever see it. If content is important for readers to see, don't hide it."

Sources:
- https://idl.cs.washington.edu/files/2019-IdyllAnalytics-EuroVis.pdf
- https://github.com/archietse/malofiej-2016

Confidence: high that a minority uses optional interaction. The share varies from 2% to 85% with how visible and how easy the control is.

Rule: every essential statement, number, and figure is visible with no click, no hover, and no JavaScript.

### 2.2 Interaction does not improve reasoning by itself

Evidence (V-PDF): Mosca et al. 2021, N = 472. Interactive version 53% correct. Static version 57% correct. The difference is not significant (p = 0.41). Only 43% of people used the controls.

Evidence (V-page): Hohman et al. 2020: "there is limited empirical evaluation of the effectiveness of interactive articles".

Sources:
- https://www.cs.tufts.edu/~remco/publications/2021/CHI2021-Interaction.pdf
- https://distill.pub/2020/communicating-with-interactive-articles/

Confidence: medium. One task type.

Rule: add a control only when the reader must change a value to see the idea. Otherwise show 2 to 4 static states side by side.

### 2.3 Predicting before seeing the data improves recall

Evidence (V-PDF): Kim, Reinecke, Hullman 2017, 378 participants.

| Condition | Reduction in recall error (percentage points) |
|---|---|
| Predict and explain | 4.08 |
| Predict with feedback | 3.54 |
| Explain only | 3.52 |
| Predict only | 2.30 |

Boundary: charts produced 36% more error than text when the task was to recall exact values.

Source: https://idl.cs.washington.edu/files/2017-ExplainingTheGap-CHI.pdf

Rule: before 1 or 2 key results, ask the reader to guess. Then show the answer. Put exact values in text or a table, not only in a chart.

### 2.4 Animation is rarely better than static pictures

Evidence (V-PDF): Tversky, Morrison, Betrancourt 2002: "Animations are often too complex or too fast to be accurately perceived."

Source: https://hci.stanford.edu/courses/cs448b/papers/Tversky_AnimationFacilitate_IJHCS02.pdf

Rule: show a process as numbered static frames. No autoplay.

## 3. Charts

### 3.1 Position on a shared axis is read most accurately

Evidence (V-PDF): Heer and Bostock 2010 (3,481 responses), repeating Cleveland and McGill. Position beat length. Angle and area were worse. Charts 40 px tall gave more error. There was little benefit above 80 px. Gridlines improved accuracy.

Source: http://vis.stanford.edu/files/2010-MTurk-CHI.pdf

Rule: use bar, dot, or line charts on a shared axis. Avoid pie and bubble charts when the reader must compare sizes. Use light gridlines.

### 3.2 Decoration helps memory of the image, not understanding

Evidence (V-PDF): Bateman et al. 2010 (20 participants). No difference in accuracy. Better recall after 2 to 3 weeks for decorated charts.
Evidence (V-PDF): Borkin et al. 2013 (2,070 charts). The authors state they tested memory of the image, "not the comprehension".
Evidence (V-page): Borkin et al. 2016: "titles and supporting text should convey the message".

Sources:
- https://sites.stat.columbia.edu/gelman/communication/Bateman2010.pdf
- http://olivalab.mit.edu/Papers/Borkin_etal_MemorableVisualization_TVCG2013.pdf

Rule: remove decoration that is not related to the message. Keep the message title, the annotations, and one accent colour.

### 3.3 The title decides what the reader takes away

Evidence (V-page): Kong et al. 2018: readers took "opposing messages from the same visualization" when the title changed.
Evidence (V-page): Kim, Setlur, Agrawala 2021: if the caption describes a feature that is not visually prominent, readers report the prominent feature instead.
Evidence (V-page): Stokes et al. 2022: 302 participants preferred the charts with the most annotation.

Sources:
- https://arxiv.org/abs/2101.08235
- https://arxiv.org/abs/2208.01780

Rule: the chart title is a sentence that states the finding and its number. Highlight in the chart the feature that the title names.

### 3.4 Label the data directly

Evidence (V-page): Schroeder and Cenkci 2018, 58 comparisons, n = 2,426, g = 0.63 in favour of integrated layouts over split layouts.
Evidence (V-page): Okabe and Ito: label on the graph, because matching colours across a distance is very difficult.

Sources:
- https://eric.ed.gov/?id=EJ1186641
- https://jfly.uni-koeln.de/color/

Rule: put the label at the end of the line or on the bar. Put each figure directly after the paragraph that introduces it.

## 4. Tables versus charts

Evidence (V-PDF): Gelman, Pasarica, Dodhia 2002: "Tables are more effective if the goal is to read off exact numbers. However, the interest in a statistical paper typically lies in comparisons".
Evidence (V-PDF): Few: tables for looking up exact values, graphs when the message is in the shape of the data.
Evidence (V2): Schwabish 2020 table guidelines.

Sources:
- https://sites.stat.columbia.edu/gelman/research/published/tables5.pdf
- https://themockup.blog/posts/2020-09-04-10-table-rules-in-r/

Rule: use a chart for the pattern and a table for the exact values. For a data-driven reader, give both. Table rules: right-align numbers, use the same number of decimals in a column, put units in the header, sort rows by the quantity that matters.

## 5. Web reading behaviour

All from Nielsen Norman Group (V-page).

| Finding | Numbers | Source |
|---|---|---|
| Most users scan | 79% scanned, 16% read word by word | https://www.nngroup.com/articles/how-users-read-on-the-web/ |
| Little is read | At most 28% of the words, more likely 20% | https://www.nngroup.com/articles/how-little-do-users-read/ |
| Attention is at the top | 57% of viewing time above the fold, 74% in the first two screens | https://www.nngroup.com/articles/scrolling-and-attention/ |
| Progressive disclosure | More than 2 levels "typically have low usability" | https://www.nngroup.com/articles/progressive-disclosure/ |
| Accordions | Avoid when readers need most of the content | https://www.nngroup.com/articles/accordions-complex-content/ |

Boundary: these are general web users. A motivated learner reads more. The 79% figure is from 1997.

Rule: conclusion first. Headings are full statements. One idea per paragraph, with the point in the first sentence.

## 6. Explanation structure

No study tests the whole sequence "what, why, how, example, counter-example, limits". The sequence is built from the separate findings below.

| Finding | Evidence | Source |
|---|---|---|
| Examples beat definitions alone | Rawson et al. 2015, effect sizes 0.74 to 1.67. Order of example and definition did not matter. (V-page) | https://eric.ed.gov/?id=EJ1071985 |
| Worked examples | Barbieri et al. 2023, g = 0.48, 55 studies. Mathematics only. (V-page) | https://eric.ed.gov/?id=EJ1364058 |
| Self-explanation | Bisra et al. 2018, g = 0.55, 69 effect sizes (V-page) | https://eric.ed.gov/?id=EJ1186664 |
| Concrete first, then abstract | Fyfe et al. 2014, review (V-page) | https://eric.ed.gov/?id=EJ1036777 |
| Explanation includes alternatives and counter-examples | Diátaxis, practitioner framework (V-page) | https://diataxis.fr/explanation/ |
| Short task-based units | Carroll: 25 cards replaced a 94-page manual in about half the learning time (V2) | https://www.instructionaldesign.org/theories/minimalism/ |

## 7. Showing logic

| Finding | Evidence | Source |
|---|---|---|
| A causal diagram next to the text improves understanding of causal sequences | McCrudden et al. 2007 (V-page). No gain in memory for main ideas. | https://pure.psu.edu/en/publications/the-effect-of-causal-diagrams-on-text-learning/ |
| Flowcharts and lists beat prose for complex conditions, but only after the reader knows how to read them | Holland and Rose 1981 (V-PDF) | https://files.eric.ed.gov/fulltext/ED213027.pdf |
| Building argument maps improves reasoning | Cullen et al. 2018, d = 0.71 (V-page). This is for building a map in a 12-week course. It is not evidence that reading a map helps. | Europe PMC |

Rule: draw a causal diagram next to any causal chain. Use a decision table for rules with 3 or more conditions, and add one line that says how to read it. Number each step of a derivation and give the reason for each step.

## 8. Diagrams

Evidence (V-PDF): Larkin and Simon 1987. Diagrams group the information that is used together and remove the need to match labels. But "diagrams are useful only to those who know the appropriate computational processes".
Evidence (V-page): Heiser and Tversky 2006. Diagrams without arrows were read as structure. Diagrams with arrows were read as function and causation.

Source: https://mechanism.ucsd.edu/bill/teaching/F12/cs200/Readings/larkin.whyadiagramissometimesworth.1987.pdf

Rule: labels go inside the figure. Arrows mean movement, sequence, or causation only. One arrow style per meaning. Add one sentence that says how to read the diagram.

## 9. Accessibility and technical basics

| Requirement | Detail | Source |
|---|---|---|
| Text contrast | 4.5:1. For large text (about 24 px, or 18.5 px bold), 3:1 | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html |
| Chart marks | 3:1 against adjacent colours | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html |
| Colour | Never the only carrier of meaning | https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html |
| Narrow screens | No two-direction scrolling at 320 CSS px. Tables and diagrams are exempt. | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html |
| Text block | At most 80 characters wide, line spacing 1.5, not justified | https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html |
| Colour blindness | 8% of Caucasian males, 5% of Asian males, 4% of African males | https://jfly.uni-koeln.de/color/ |
| Dark mode | Light mode performed better for normal vision. Offer both. | https://www.nngroup.com/articles/dark-mode/ |

## 10. Self-check questions

Evidence (V-page): Szpunar, Khan, Schacter 2013, experiment 2. 16 people per group. A 21-minute lecture in four segments.

| Group | Mind wandering | Final-segment test score |
|---|---|---|
| Tested after each segment | 19% | 89% |
| Restudied | 39% | 65% |
| Not tested | 41% | 70% |

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/

Evidence (V-page, abstract): Adesope et al. 2017: practice tests beat restudy. https://eric.ed.gov/?id=EJ1141817

Confidence: high that retrieval helps. Low on the best format inside a web page, because the studies used lectures and prose, with small samples.

Rule: after each major section, 1 to 3 questions that need recall or application. The answer is hidden in `<details>` and includes the reasoning.

## 11. Uncertainty and sources

| Finding | Evidence | Source |
|---|---|---|
| Stating uncertainty costs little trust | Van der Bles et al. 2020, n = 5,780: "only a small decrease in trust" (V-page) | Europe PMC |
| Verbal probability words are misread | Budescu et al. 2014, 25 samples in 24 countries. Adding numeric ranges improved understanding. (V-page) | https://ideas.repec.org/a/nat/natcli/v4y2014i6d10.1038_nclimate2194.html |
| A defined scale | IPCC: likely = 66 to 100%, very likely = 90 to 100%, virtually certain = 99 to 100% (V-PDF) | https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf |
| Inform, do not persuade | Blastland et al. 2020 (V-PDF) | https://media.nature.com/original/magazine-assets/d41586-020-03189-1/d41586-020-03189-1.pdf |

Rule: pair every verbal uncertainty word with a number. Each key claim has a source and a confidence label.

## 12. Gaps: what was not verified

- Not opened: Cleveland and McGill 1984 original, Tufte's own text, van Gelder's papers.
- Effect sizes not confirmed in an opened source: Adesope 2017 overall effect, Schneider 2018 signaling effect, Budescu "27% to 40%" figure.
- The New York Times "10 to 15% of readers interact" figure was confirmed only through a republished secondary article.
- No evidence was found, in either direction, for: scrollytelling for learning, the best spacing of questions in web text, or whether reading an argument map improves comprehension.
- "One self-contained file with no external resources" is supported by an archival argument only. There is no measured evidence.
