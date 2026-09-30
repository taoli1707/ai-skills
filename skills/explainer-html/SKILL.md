---
name: explainer-html
description: How to write HTML pages that this user can understand easily. The user reads English as a second language and learns best from concrete examples, full detail, explicit step-by-step logic, and data with sources. Use this skill every time you create or edit an HTML page, HTML file, or HTML artifact that a person will read. This includes explanations of a new topic, tutorials, "explain this code or system" pages, research summaries, reports, comparisons, decision documents, dashboards, and visual write-ups. Use it even when the user only says "make an html" or "show me this as a page" and does not mention learning. Also use it when the user wants to understand, learn, or study something and a page is a good way to explain it.
---

# Explainer HTML

This skill tells you how to build an HTML page that teaches. The rules come from research on learning, on reading in a second language, and on explanatory web pages. The research is in `references/`, with sources and numbers.

## The reader

You write for one person. This person is an engineer and learns new technical material quickly. English is not their first language. They told us how they learn best:

- concrete **examples**
- full **detail**
- explicit **logic**, step by step
- **data**, with numbers and sources

Two research findings explain why a normal page fails this reader.

| Finding | Evidence | Consequence for you |
|---|---|---|
| A second-language reader often does not notice a misunderstanding. | When a text used idioms made of common words, comprehension fell from 86% to 53%. Readers still rated their own comprehension at 60%. For metaphors, readers noticed the problem in about 4% of cases. | The reader cannot ask about a problem that they did not notice. You must remove the risk before the reader sees the page. |
| A page that is easy to read makes every reader overconfident. | A feeling of ease during reading does not predict what the reader remembers. Retrieval practice with feedback improves retention (g = 0.73). | The page must let the reader test their own understanding. |

## The five commitments

| # | Commitment | Meaning |
|---|---|---|
| 1 | Plain words, real technical terms | Common words for everything, except the technical terms of the field. Each technical term appears in its real form, is explained well where it first appears, and never changes its name. |
| 2 | Example before rule | A concrete case with real numbers comes first. The general rule comes after it. |
| 3 | Visible logic | Every step of the reasoning is written down, with its reason. |
| 4 | Data with source and confidence | Each important claim has a number, a unit, a source, and a confidence label. No invented numbers. |
| 5 | Self-check | The reader answers questions and compares with a worked answer. |

"Detail" means more depth on the main idea: more steps, more examples, exact values. It does not mean side topics. Interesting but irrelevant material reduces learning (g = -0.16 to -0.48), so remove it.

A term that the reader will meet in their situation is not a side topic. But it does not belong in the main explanation. Put such terms in the section "Words that you will hear", outside the main path.

## Workflow

### Step 1: define the question and the starting point

Write one sentence: "This page answers the question: …". This sentence becomes the `<h1>`. If the question has two or more parts, plan a page with parts (see "Pages with several parts").

Write a second sentence: "The reader asks because …, and will use the answer to …". This is the situation of the reader. A reader whose team starts to use a technology must understand the words that the team says. A reader who compares two offers must decide. The page serves this situation.

Write for a beginner in this topic, because help for beginners is worth more (d ≈ 0.5) than it costs experts. Give the expert a way to skip: a line "You need to know: …" in the header, and links in the contents list.

### Step 2: collect and verify the facts

- **Use the reader's own case** when the request contains it: their numbers, their code, their data. Do not put private details from memory (family, home, health, money) on a page unless the request is about them. Private details in the reader's own files can appear when the explanation needs them: use only the values that the explanation needs.
- **Calculate every number with code.** Do not calculate in your head. Round at the step where the real world rounds: for money, calculate in whole cents, as a bank does. For other values, calculate with full precision and round only for display.
- **Find a source for each factual claim.** Open the source when you have web access. Some tools return a summary of a page, not the page. In the tests of this skill, such a summary gave a wrong number two times. So verify each number and each name in the original text of the page, for example with a direct download and a text search. If you cannot, the label is "Medium" at most, and the sources section states how you read the source.
- **Never invent a number, a quotation, or a source.** If you cannot verify a claim, keep it only with the label "Low" and the words "not verified".
- **Match the effort to the question.** A page about the reader's code or data needs real values from a real run. A page about a general concept can use small example values that you calculate and label as "example values". Simple example values can give the reader a wrong picture of real values. So state how real values differ, with a source: "In this example the score is 0.99. With a real model, a good match often has a score between 0.3 and 0.6." Do not download large models or data sets unless the user asks.
- **Report every run.** If you run a test or a measurement, state what the data is and how you ran it. If you ran it several times, report all results, not only one. If the results differ much, say so in the limits.

### Step 3: plan before you write

1. **Term list.** The key terms that the page teaches: up to 12 for each part. (The checker warns above 15 in one part.) Use the real technical term of the field for each one, see "Technical terms". For each term: the one name you will use, and a definition of one sentence in common words. Check both directions: one name for each concept, and one concept for each name. A short form is a second name. Use the full name every time, or introduce the short form one time: "monthly payment (from here: payment)".
2. **Main example.** The concrete case, with real values.
3. **Contrast.** A second case that differs from the main example in one important feature.
4. **Wrong idea.** The most common wrong belief about this topic, if one exists.
5. **Figures.** Which idea needs a chart or diagram, and what each figure must show.
6. **Limits and assumptions.** Where the explanation stops being true, and what you assumed because the request left it open.
7. **Word budget.** Plan about 3,000 words of running text for one question, and about 1,500 for each part of a page with parts. The required boxes (short answer, wrong idea, limits, self-check, recap) need about 600 words together. See "Length".

### Step 4: write the body

Read `assets/example-body.html`. It shows every component in use. If you planned a page with parts, read also `assets/example-parts.html`. It shows the structure: parts, contents list with a marked main path, headings. If you planned one part, read it only when the build says that the page needs a marked main path. Write your content in one file, for example `body.html`. This file contains only the content that goes inside `<main>`. You do not write `<head>` or styles, and you do not need to read `assets/page.css`.

If the page needs a component that does not exist, put a small `<style>` element at the end of your body file. Use the colour variables (`var(--text)`, `var(--accent)`, `var(--s1)`). A small inline style is allowed for a layout fix, for example `style="white-space:nowrap"` on a date. Do not change the standard styles.

### Step 5: build and check

```bash
python3 ~/.claude/skills/explainer-html/scripts/build_page.py body.html \
  --title "Compound Interest Explained" --out page.html
```

The script adds the head, the standard styles, and the standard script. Then it runs the checker. For a report or a dashboard add `--kind report` or `--kind dashboard`. For text inside a software product add `--kind product` (language checks only).

Fix every FAIL. Read every WARN and decide. The line numbers in the report refer to your body file. "What the checker tests" below lists the checks, so you do not need to read the source of the checker.

### Step 6: look at the page, read it as the reader, deliver

```bash
python3 ~/.claude/skills/explainer-html/scripts/render_page.py page.html --out-dir shots/
```

The script writes pictures of the top of the page, every figure, every table, and every code block. Figures are shown in the light theme, the dark theme, and at phone width. Add `--full` to get the whole page in slices. Add `--only figure-2` or `--only table-3` to make only the pictures of one figure or one table again after a change. The phone pictures are 320 px wide. Open the pictures. Look for labels that overlap, text that is cut, table headers that break into many lines, and tables that are wider than the column. In the tests of this skill, 3 of 5 figures had overlapping labels that no program found. If the script finds no browser, tell the user that the layout was not checked visually.

Then read the final text once from the top. For each sentence ask: "Can this sentence be read in a second way?" Complete the "Final check by hand".

Save the file where the user asked. If the user named no location, use the normal output location of the environment. Do not add an explainer page to a code repository unless the user asks. Tell the user the file path, and what you did not verify.

**Correct mistakes silently and completely.** When you find a mistake in the page, at any step, correct it. Do not report the mistake to the user, and do not mention it on the page. Then search the whole file for every other place that depends on the corrected item, and update each one: the short answer, the headings, the contents list, the text, the labels and the `aria-label` of the figures, the tables, the answers of the self-check, the recap, and the glossary. A number that changes in one place and stays in another place is a new mistake. After the correction, build the page again and look at the pictures again. This rule is about mistakes that you corrected. A limit that remains, for example a source that you did not verify, still belongs on the page and in your message.

## Page structure

| # | Section | Content | When |
|---|---|---|---|
| 1 | Header | `<h1>` is a question or a claim. Then one line: date, reading time, "You need to know: …". | Always |
| 2 | The short answer | 2 to 6 sentences with the key numbers. | Always |
| 3 | Assumptions | What you assumed because the request left it open. | When you assumed something |
| 4 | On this page | Links to the sections. | 4 or more sections |
| 5 | One concrete example | A worked example with real numbers. Each step has its reason. | Always |
| 6 | The rule | The general idea behind the example. A diagram if the idea has structure, sequence, or cause. | Always |
| 7 | The data and the comparison | "Guess first" question, chart, table with exact values. Two cases side by side, and the principle after the comparison. For a calculation topic, the data and the comparison can be one section. | When data exists |
| 8 | A common wrong idea | The wrong idea, the correct idea, and why the wrong idea fails. | When one exists |
| 9 | Limits | Where the explanation stops being true. What is known and what is not known. | Always |
| 9b | Words that you will hear | Terms that belong to the situation of the reader, but not to the main idea. One or two sentences for each term, and one sentence on how the term connects to the main idea. | When the reader enters a new field or a new team |
| 10 | Check your understanding | Questions with hidden answers. | Always |
| 11 | Recap, glossary, sources | 3 to 5 main points. All defined terms. All sources with confidence labels. | Always |

Reasons for this order:

- **Short answer first.** Readers give 57% of their viewing time to the first screen. Context before the content also reduces reading effort.
- **Example before rule.** Examples with definitions beat definitions alone (effect sizes 0.74 to 1.67). Worked examples help beginners (g = 0.48).
- **Comparison.** Two cases side by side beat two cases one after the other (d = 0.50).
- **Wrong idea.** A text that names and corrects the wrong idea beats a plain explanation (g = 0.41).
- **Self-check.** Retrieval practice beats rereading (g = 0.50, and 0.73 with feedback).

**One idea per section.** Working memory holds about 3 to 5 new items. So each section introduces at most 3 or 4 new elements that the reader must hold in mind together. If the first example needs more terms, build the example in two stages: a simple version first, then the complete version.

**Headings.** A content heading is a statement that gives the main point: "The difference grows every year: USD 1,289 after 10 years". The heading of the wrong-idea section states the correct fact. Only the fixed sections keep a fixed name: "Check your understanding" and "Recap, glossary, and sources".

**Short answer and definitions.** The short answer uses common words. If it needs a key term, add a few words of explanation in parentheses. The full definition with `<dfn>` comes later, in the section that teaches the term. The same is true for the header line, the assumptions box, the contents list, and the headings: a key term can appear there before its definition. In all other places, also in tables and figures, the definition comes first.

**Guess first.** This box is optional. Ask the reader to guess a value that the reader did not see before: not in the short answer, not in a heading. If the short answer and the headings already state all key results, leave the box out.

**Self-check.** Put 1 to 3 questions after each main part. A short page has one block of 2 to 5 questions at the end. Questions need recall, calculation, or application. Most readers must be able to answer them: a question that is too difficult gives no benefit (g = 0.03). Each answer contains the reasoning, and names the typical wrong answer.

### Length

These numbers are design judgments, not research results.

| Words of running text | What you do |
|---|---|
| Up to 3,500 (about 30 minutes) | One page. |
| 3,500 to 6,000 | One page with a marked main path. The main path is complete without the other sections and has at most 3,000 words. State both reading times in the header. |
| More than 6,000 | First remove what the question does not need. If the page is still longer, ask the user: one long page, or a series of pages with one question per page. If you cannot ask, make one page with a marked main path, and say in your final message that the page is long. |

Running text is the text that the reader reads in order. Tables, the contents list, the glossary, and the list of sources are reference material and do not count. Reading time is the number of words of running text divided by 120, rounded up. The build script prints the words and the reading time, for the page and for the main path.

**How to mark the main path.** In the contents list, write `<li class="core">` for each section of the main path. The top of the page (short answer, assumptions) always belongs to the main path. A section outside the main path comes after the sections of the main path, and its heading starts with "More detail:".

### Pages with several parts

When the question has two or more parts, each part is a small page inside the page:

1. At the top: one short answer for the whole page, then the contents list.
2. Each part starts with `<p class="part">Part A</p>`, then a heading, then its own short answer box.
3. Each part has its own example, rule, and self-check, and its own key terms, up to 12.
4. The wrong idea and the limits belong to the part that they concern.
5. At the end, one time for the whole page: recap, glossary, sources.

## Components

All components are in `assets/example-body.html`.

The styles add five pieces of visible text. Do not write these words yourself:

| Where | Text that the styles add |
|---|---|
| Before each `<span class="why">` | "Reason: " |
| Before the summary of `<details class="optional">` | "Optional detail: " |
| After each `<li class="core">` in the contents list | " (main path)" |
| Above a figure, only on a narrow screen | "Move the figure sideways to see all of it." |
| Above a table, only when the table is wider than its frame | "Move the table sideways to see all of it." |

| Component | Markup | Use |
|---|---|---|
| Header line | `<p class="meta">` | Date · reading time · "You need to know". Separate with " · ". The build script fills `{{today}}`, `{{minutes}}`, and `{{main_path_minutes}}`. |
| Short answer | `<div class="box bottom-line">` | The conclusion with key numbers. |
| Assumptions | `<div class="box assume">` | What you assumed. |
| Contents | `<nav class="contents">` | Links. `class="core"` on `<li>` marks the main path. |
| Part | `<p class="part">` | Start of a part. |
| Key term | `<dfn>term</dfn> (definition)` | First use of a key term. |
| Worked example | `<div class="box example">` with `<ol class="steps">` and `<span class="why">` | Steps with reasons. |
| Guess first | `<div class="box predict">` | A question before a key result. At most 2 per page. |
| Chart | `<figure>` with `.fig-title`, `.fig-sub`, `.fig-scroll`, `.fig-read`, `.fig-source`. SVG classes `axis`, `grid`, `axis-label` | Pattern in data. |
| Diagram | `<figure class="diagram">`. SVG classes `node`, `node-name`, `node-value`, `arrow`, `arrow-head`, `arrow-label` | Structure, sequence, cause. |
| Table | `<div class="table-wrap"><table>` with `<caption>`, `class="num"`, `<th scope="row">`, then `<p class="table-read">` | Exact values, comparisons, decision rules. Keep column headers short. A long file path or identifier in a cell makes the table wide: put it in the text below the table, or allow a break with `<wbr>` after a "/". |
| Side by side | `<div class="compare">` | Two short cases in words. |
| Wrong idea | `<div class="box mistake">` | Wrong, correct, why. |
| Limits | `<div class="box limits">` | Limits of the explanation. |
| Self-check | `<div class="check">` with `<details>` | Questions with hidden answers. |
| Optional depth | `<details class="optional">` | Detail that the main idea does not need. |
| Recap | `<div class="box recap">` | Main points. |
| Glossary | `<dl class="glossary">` | All defined terms, in alphabetical order. |
| Sources | `<ol class="sources">` with `<span class="conf high">` | Sources with confidence labels. |
| Quoted text | `class="quoted"` on a block, or `<span class="quoted">` inside a sentence | Text copied from a source or from data: a quotation, the title of a paper, a text from a data file. The language rules do not apply to it. |

## Language rules

These rules have the largest effect for this reader. Apply them to every visible word: headings, labels in figures, table headers, and answers.

| # | Rule | Instead of | Write |
|---|---|---|---|
| 1 | Use the most common word for everything that is not a technical term. Never replace a technical term with a simple word. | utilize, leverage, mitigate, robust | use, use, reduce, reliable |
| 2 | Define each key term in the sentence where it first appears, or in the next sentence. Use `<dfn>`. A long definition is its own sentence: "The scheduler uses a <dfn>slot</dfn>. A slot is one outing with its start time and its end time." | "Amortization determines the split." | "<dfn>Amortization</dfn> (the plan that divides each payment into interest and loan repayment) determines the split." |
| 3 | One name for one concept, and one concept for one name. Repeat the name exactly. | "the loan … the mortgage … the debt". Or "list" for two different things. | "the loan … the loan … the loan" |
| 4 | No idioms, no metaphors, no humor, no sarcasm, no cultural references. | under the hood; rule of thumb; a ballpark number | inside the system; a simple approximate rule; an approximate number |
| 5 | One idea per sentence. Maximum 25 words. Average at most 20 words. These numbers are limits, not goals: a short sentence is good. Order: subject, verb, object. | One sentence with three clauses. | Three sentences, connected with "because", "so", "but". |
| 6 | Each sentence has only one possible first reading. Keep "that", "which", and the articles. | "The report the team wrote failed review." | "The report that the team wrote failed the review." |
| 7 | Replace a phrasal verb with a one-word verb. | figure out, carry out, get rid of, come up with | determine, perform, remove, create |
| 8 | Keep the connectives. They carry the logic. | "The rate rose. Payments rose." | "The rate rose. Therefore the payments rose." |
| 9 | Use a pronoun only when one referent is possible. Otherwise repeat the noun. | "The client sends the token to the server. It checks it." | "The client sends the token to the server. The server checks the token." |
| 10 | Active voice. Positive statements. No double negative. | "It is not uncommon for errors to be missed." | "Reviewers often miss errors." |
| 11 | At most two nouns before a noun. | "user account password reset policy" | "the policy for the reset of account passwords" |
| 12 | Spell out each abbreviation at first use. Introduce at most 3 new abbreviations per part. | "e.g.", "i.e.", "etc.", "and/or", "vs." | "for example", "that is", a complete list, "A or B or both", "compared with" |
| 13 | No contractions. | don't, it's, you'll | do not, it is, you will |
| 14 | Write "you". | "One should consider…" | "You should consider…" |

**Elaborate. Do not strip.** Simple language does not mean less content. Keep the precise term and the full content. Then add support: a definition, a second sentence that says the same thing in other words, an example, the reason. In studies, text with added explanation worked as well as simplified text.

**Unknown words are a budget.** Comprehension needs about 98% known words, which means at most 1 unknown word in 50. Spend this budget on the technical terms of the field, and on nothing else.

**Technical terms.** The reader is an engineer and will meet the real terms in books, in standards, and at work. So use each technical term exactly as the field uses it, and explain it well. Do not invent a simple name for it.

| Do not write | Write |
|---|---|
| "Concrete resists a push well and a pull badly." | "Concrete has a high <dfn>compressive strength</dfn> and a low <dfn>tensile strength</dfn>. Compression is a force that presses the material together. Tension is a force that pulls it apart." |
| "the glue" | "the <dfn>cement paste</dfn>, which is the mix of cement and water that binds the aggregate" |

A good explanation of a technical term has up to 4 parts: what the term means in plain words, the unit or the formula if one exists, one example with a value, and the relation to a term that the reader already knows. A plain word can help in the explanation, but after the explanation the page uses the technical term only. If the field has a standard symbol or abbreviation, give it too: "water to cement ratio (w/c)".

**Standard terms.** A standard term of the field stays, also when it looks like a phrasal verb or an idiom: "round up" in mathematics, "log in" in software. Define it if the reader may not know it.

**Abbreviations.** An abbreviation that the team of the reader says every day (for example the name of an index type) is a key term: define it and keep it. Units (km, °F, ms), file names, and code identifiers are not abbreviations. A name in capital letters (a brand, a product, a model) is not an abbreviation: tell the checker with `<!-- names: LEGO, NASA, M4 -->` in the body file.

**Sources and quotations.** Say in your own plain words what a source says. Quote only when the exact words matter. Then mark the quotation with `class="quoted"`, and explain it in plain words after it.

**Analogies.** An analogy is allowed only in explicit form. State which parts correspond, and state where the analogy stops being true. Use a source that every culture knows: water in pipes, roads, a kitchen. Do not use sports or television.

**First language.** If the reader has told you their first language, add the first-language word for each key term: in parentheses at first use, and in the glossary. Definitions in the first language help more than definitions in the second language. Do not guess the language from a name.

### Example of the language rules

Before:

> Under the hood, the scheduler leverages a greedy heuristic to figure out which events make the cut, which, while not optimal, is a solid rule of thumb that gets you 90% of the way there.

After:

> The scheduler chooses events with a <dfn>greedy method</dfn>. A greedy method takes the best available option at each step, and it never changes an earlier choice. This method does not always find the best possible schedule. In a test with 40 events, the greedy method reached 90% of the best possible score (source: `test/schedule.test.ts`).

What changed: two idioms and one phrasal verb are removed. One long sentence became four sentences. The key term is defined. The vague "90% of the way" became a measured number with its source. (A number like this must be a real measurement. If no measurement exists, write that no measurement exists.)

## Example rules

1. **Real values with units.** "USD 10,000 at 5% for 3 years", not "some amount at some rate".
2. **Every step, with its reason.** Do not write "it is easy to see that…".
3. **Connect the example to the rule.** Below the general formula, write the same formula again with the numbers of the example.
4. **A second case that differs in one feature.** Put the two cases side by side. State the principle after the comparison.
5. **One case where the rule fails or surprises.** This shows the limit of the rule.
6. **Neutral content.** Money, time, distance, weight, temperature.

## Logic rules

| Situation | Form |
|---|---|
| A chain of reasoning | Numbered steps. One inference per step. Each step states its reason. |
| A chain of causes | A diagram next to the text. An arrow has one meaning in the whole diagram, and the reading line states this meaning. |
| A rule with 3 or more conditions | A decision table, with a line "How to read this table". |
| A choice between options | A comparison table: one row per option, one column per criterion, the unit in the column header. With more than 5 criteria, turn the table: one row per criterion, one column per option, and the unit in the row label. The recommendation and its reason come below the table. |
| A derivation or calculation | Every algebra step is shown. |
| Behaviour that depends on a condition | State the condition: "when X is true, Y happens". Do not write "sometimes". |

Flowcharts and tables beat prose for complex conditions, but only when the reader knows how to read them. So every figure and every decision table has a reading line.

## Data rules

1. **Each important claim has four parts:** number, unit, source, confidence.
2. **Confidence labels.** Explain them one time, in the sources section. You can also put a label directly after a claim in the text.

   | Label | Meaning |
   |---|---|
   | High | Verified in a primary source, or calculated and checked. |
   | Medium | One good source, or a source with limits. |
   | Low | Not verified, or the sources disagree. |
   | Given | A value from the message of the reader, or an example value. |

3. **Kinds of source.** An external source (with link). The reader's message ("Given"). The reader's code (file and line). A calculation (state the formula). A run of a program (state the command and the date). Reasoning (the steps are on the page). A statement that follows from reasoning needs no external source, but the reader must be able to follow each step.
4. **A word for probability or frequency has a number next to it.** These words are: likely, probably, usually, often, rarely, most, many, few. Write "likely (about 70%)". Readers in 24 countries read such words very differently. If you have no number, write "No number is available", or remove the claim. The rule is for claims about how often or how probable something is. It is not for a comparison ("the most similar text") or for the fixed labels of the components.
5. **Show the denominator.** Write "3 of 16 readers (19%)", not only "19%".
6. **Separate absolute and relative change.** "The rate rose from 4% to 6%. This is 2 percentage points, or 50% relative."
7. **Rounding.** If rounded parts do not add up to the rounded total, say so in one sentence. Show enough decimals that the reader can see the order of two values that are close.
8. **One reading worldwide.**

   | Item | Write | Do not write |
   |---|---|---|
   | Date | 27 September 2026, or 2026-09-27 | 09/27/26 |
   | Time of day | 13:30 | 1:30pm |
   | Decimal marker | 0.25 | .25 or 0,25 |
   | Large number | 2 billion (2,000,000,000) | 2 billion |
   | Currency | Name it at first use, in table headers, and in figure subtitles. Write "US" directly before the dollar sign, without a space. After that, the dollar sign alone is enough when the page has one currency. | The dollar sign alone at first use |
   | Season | the month | "this fall" |

## Figures

A chart shows a pattern in data. A diagram shows structure, sequence, or cause. The rules of this skill for figures are complete. If another skill for charts is loaded, the rules of this skill decide, because they are made for this reader. In particular: no legend, no hover layer.

| Rule | Reason |
|---|---|
| Use a bar, line, or dot chart on a shared axis. No pie chart, no 3D, no bubble chart for comparison. | Position on a shared scale is read most accurately. |
| The title of a chart is a sentence that states the finding and its number. The title of a diagram is a sentence that states the main point. | The title decides what the reader takes away. |
| The figure makes visually prominent the feature that the title names. | If not, the reader reports the prominent feature instead. |
| Label each series directly, at the end of the line or on the bar. No separate legend. A short key for symbols inside a diagram is allowed. | Integrated labels beat separate labels (g = 0.63). |
| Use the series colours `var(--s1)` to `var(--s4)` in this order. At most 4 series. Series also differ by shape. Lines: solid or dashed. Points: circle or square. Bars: full colour, or a light fill with a dashed border. | These 4 colours stay distinct for colour-blind readers in both themes. About 8% of men have a colour vision deficiency. |
| `viewBox` width 560 to 720. Labels 13 px or larger. The SVG is inside `<div class="fig-scroll">`. | Labels stay readable on a phone. There the figure scrolls sideways, so the reader does not see all of it at first. Therefore the title and the text below the figure state the finding with its numbers. |
| Below the figure: "How to read this chart", and the source. | A figure helps only a reader who knows how to read it. |
| Inline SVG with `role="img"` and an `aria-label` that states the finding. | The page works without external files. |
| Calculate the coordinates with code. Then look at the picture of the figure. | Label collisions are the most common defect. |
| If a name is too long for the figure, use a short name in the figure and state the mapping in the subtitle. | A cut label is worse than a short label. |

## Tables

- Every table is inside `<div class="table-wrap">` and has a `<caption>` that states the main point.
- Numbers are right-aligned (`class="num"`), with the same number of decimals in a column.
- The unit is in the column header.
- Rows are sorted by the quantity that matters. The important row has `class="highlight"`.
- The label of a row is a row header: `<th scope="row">`.
- Give both: the chart for the pattern, the table for the exact values. Readers recall exact values worse from a chart than from text.

## Visual and interaction rules

| Rule | Evidence |
|---|---|
| Everything essential is visible without a click, without hover, and without JavaScript. | In a study of 7,055 visits, 41% of the readers who reached the end had missed content behind a click. |
| Only two things may be hidden: the answers of the self-check, and optional depth (`details.optional`). One level only. | More than two levels of disclosure have low usability. |
| No tabs, no carousel, no tooltip that carries content. | "If you make a tooltip or rollover, assume no one will ever see it." |
| Add an interactive control only when the reader must change a value: to see the idea, or to test their own numbers (see "Pages that support a decision"). The start state shows the main example, and the same result is also in static text. | An interactive version gave 53% correct answers, the static version 57%. |
| For a process, show numbered static frames. No automatic animation. | Animations are often too fast to be perceived accurately. |
| No decorative image, no stock photo, no decorative emoji. | Decorative pictures do not help. Explanatory pictures help (g = 0.23 to 0.39). |
| A figure is directly after the paragraph that introduces it. | Spatial contiguity: g = 0.63. |
| Use bold for a few key terms and results. | Signals work only when they are used sparingly. |
| Put links to sources at the end of a section or in the sources list. | Links inside the text add decisions for the reader. |

## Structure of a report or decision document

| # | Section | When |
|---|---|---|
| 1 | Header, short answer, assumptions | Always |
| 2 | On this page | 4 or more sections |
| 3 | The facts: measured values, tables, figures. Each with its source. | Always |
| 4 | The comparison of the options, and the sensitivity | When the page supports a decision |
| 5 | Recommendation, and why | When the page supports a decision |
| 6 | Limits: what is not known, what was not measured | Always |
| 7 | Sources with confidence labels | Always |
| Optional | Worked example, wrong idea, self-check, recap, glossary (when the page defines terms) | When they help |

A decision document is short. Plan about 1,500 to 2,000 words of running text. The reader wants the decision first and the evidence second. Put long evidence in tables and in optional blocks.

For `--kind report`, the checker requires the short answer and the sources, and it warns when the limits are missing. It does not require the worked example or the self-check.

## Pages that support a decision

Many requests are about a decision of the reader: their loan, their system, their purchase. Then the page must do two things: teach the idea, and serve the decision. In the tests of this skill, a page without these rules taught well, but a page written without the skill was the better tool for the decision.

| Rule | Example |
|---|---|
| The short answer answers the decision, and names the condition that changes the answer. | "The refinance pays for itself after about 26 months. If you sell the house before that, you lose money." |
| If two reasonable assumptions give different results, the short answer states both. Do not put the more exact result in a hidden block. | "With a new loan of 28 years: month 26. With a new loan of 30 years: month 20." |
| Compare the numbers of the reader with public data. If a value is unusual, say so, and list questions that the reader can ask. | "Your rate of 6.1% is 0.93 percentage points below the average of this week (7.03%). Ask the lender: is the rate fixed? Does it include points?" |
| Show the sensitivity: a table of how the result changes when each uncertain input changes. Name the input with the largest effect. | Rows: rate 6.1%, 6.3%, 6.5%. Columns: cost USD 6,000, USD 10,000, USD 15,600. |
| Match the precision to the input. When the input is "about USD 6,000", the result is "about 26 months". Exact values belong in the worked example and in tables. | Not: "you save USD 72,704.64". |
| Show an option that the reader did not ask about, if it is clearly better. | "Option C: refinance, and continue to pay the old amount." |
| A calculator for the reader's own values is a good use of an interactive control. The main case is also on the page as static text. | Inputs start with the values of the reader. |
| Separate the facts from the recommendation. Put the recommendation and its reason in a box of its own. | Facts in tables. Then: "Recommendation, and why". |

## Pages that explain code

1. **Read before you explain.** Read the named files and the code that they call. If the logic is in other files than the user named, say so on the page.
2. **Use a real run as the main example.** Run the program, or its functions, with real input. Show the values at each step. Work on a copy in a temporary folder. If the program needs the network or the current time, use the data that an earlier run saved: block the network, and set the clock to the time of that run. Then confirm that your run gives the same result as the saved result. If a real run is not possible in reasonable time, follow one example through the code by hand, and label it "followed by hand, not run".
3. **Never change the repository.** Do not edit, build into, or commit to the repository while you prepare the page.
4. **Cite file and line** for each rule: `src/schedule/assemble.ts:248`. State the commit, and state if the working copy has changes that are not committed. If you cannot run git commands, say so on the page, and state the date and time when you read the files.
5. **State each boundary exactly.** Read the comparison operator. `end > close` removes an activity that ends after the closing time, and keeps an activity that ends exactly at the closing time. Check each stated boundary against your example.
6. **A summary must contain the exceptions.** If a rule has an exception in the code, the short answer states the exception too, or it says "with one exception, see section N".
7. **Words first, then code.** Explain a rule in words. Then show at most about 10 lines of the code. Identifiers keep their exact spelling, in `<code>`.
8. **Separate behaviour from judgment.** Describe what the code does. Put anything that looks like a defect in a separate section "Possible defects", each with the evidence and the file and line. Do not fix the code unless the user asks.
9. **List every rule.** The reader forgot the logic, so a rule that is missing on the page is a rule that the reader does not know. The main path explains the rules that decide the result of the example. After the main path, a table "All rules" has one row for each rule in the code: the rule in words, its value, its file and line. Tables do not count as running text, so this table does not make the main path longer.
10. **List the settings that the reader can change:** each setting, the place where the code reads it, and its effect.
11. **Name values that the code never reads** (unused settings, unused options). The reader often believes that these values have an effect.

## Technical contract

- One file that contains everything. No external font, script, image, or stylesheet. The build script guarantees the standard parts.
- `<title>` is a name of 2 to 4 words. The long question goes in `<h1>`.
- The page works at a width of 320 px. Only tables, code blocks, and figures scroll inside their own frame.
- Light and dark themes come from the standard styles. All colour pairs pass the contrast limits (4.5 to 1 for text, 3 to 1 for marks).
- **Artifact tool:** if you publish the page as an Artifact, also load the `artifact-design` skill. The standard styles already follow its theme rules. For content, structure, and language, this skill decides.

## Other kinds of HTML

| Kind of page | What you apply |
|---|---|
| Explanation, tutorial, "help me understand" | Everything in this skill. |
| Report, research summary, comparison, decision document | Short answer first. All language, logic, and data rules. The rules for pages that support a decision. Limits and sources. The worked example and the self-check are optional. `--kind report` |
| Dashboard or data view | Language rules, data rules, figure rules, table rules. `--kind dashboard` |
| HTML that is part of a software product (application screen, email template, generated site) | The design and the audience of the product decide. Do not apply the page structure or the standard styles. Use the language rules only for text that this user will read. `check_page.py --kind product` |

## What the checker tests

| Level | Test |
|---|---|
| FAIL | A sentence with more than 25 words. An idiom or informal expression from a list of about 140. A Latin abbreviation (e.g., i.e., etc., vs.) or "and/or". A date such as 03/04/2026. |
| FAIL | A missing part: short answer, worked example, self-check with hidden answers, sources. `<details>` inside `<details>`. |
| FAIL | An external resource. Justified text. Missing `lang`, viewport, or `<title>`. The same `id` two times. A link to a place that does not exist. |
| WARN | Phrasal verbs, uncommon words, wordy expressions, contractions, double negatives, "billion" without digits, abbreviations without the full form, a term that is used before its definition, more than 15 defined terms in one part, a long paragraph, much bold text, emoji. |
| WARN | A generic heading ("Overview"). `<details>` that is not a self-check answer and not marked optional. Hover text, tabs, a legend. A figure without a finding title or reading line. Labels smaller than 12 px. A number cell that is not right-aligned. A table without scroll frame. A page with more than 3,500 words of running text and no marked main path. A main path with more than 3,000 words. |

Run `check_page.py --words` to print the word lists. The checker cannot judge meaning, and its lists are not complete. A page that passes can still be unclear. The checker does not test: one name per concept, words for probability and frequency, correct numbers, the order of example and rule, and the layout. You test these in the final check by hand.

## Final check by hand

1. Can a reader who reads only the short answer and the headings state the main point?
2. Does each key term have exactly one name, and does each name mean exactly one thing?
3. Does the example come before the rule, and does each step have its reason?
4. Is every number calculated or taken from a source? Is every source real and opened?
5. Does each chart title state the finding, and does the chart make that finding prominent?
6. Did you look at the picture of every figure and every wide table?
7. Do the self-check questions need recall or calculation? Does each answer contain the reasoning?
8. Is any sentence open to a second reading?
9. Did you remove every side topic?
10. Is every corrected value the same in all places of the file: short answer, headings, text, figures, tables, answers, recap?
11. Does each technical term appear in its real form, with a good explanation at first use?

## Reference files

Read a reference file when the reader asks for the evidence behind a rule, or when you must decide a case that the rules do not cover.

| File | Content |
|---|---|
| `references/evidence-learning.md` | Cognitive load, worked examples, multimedia principles, retrieval practice, wrong ideas. Includes a list of ideas to avoid, such as learning styles. |
| `references/evidence-language.md` | Reading in a second language: vocabulary, idioms, sentence rules, definitions, typography, numbers and dates. |
| `references/evidence-page-design.md` | Interactivity, charts, tables, web reading behaviour, diagrams, self-check questions, uncertainty. |
| `assets/example-body.html` | The body of the example page. It shows every component. |
| `assets/example-page.html` | The built example page. Open it in a browser to see the result. |

<!-- For the person who edits this file: never write a dollar sign directly before a digit here.
When the skill starts as a command with a request, Claude Code replaces such text with words of the request.
Write the amount with the currency code, for example USD 10,000. On the pages themselves, the form with the dollar sign is correct. -->
