# Evidence: writing for a reader who uses English as a second language

Research date: 2026-09-27. Read this file when you need the reason behind a language rule in SKILL.md, or when the reader asks "why do you write this way?".

Most participants in these studies were students or language learners. They were not senior technical professionals. This limit applies to almost every finding below.

## Contents

1. Verification tags
2. Vocabulary: how many unknown words a reader can accept
3. What is difficult for second-language readers
4. Rules from controlled-language standards
5. Sentence length and readability scores
6. Definitions of terms (glosses)
7. One term for one concept
8. Simplify or elaborate
9. Typography
10. Numbers, units, dates
11. Pictures, tables, worked examples
12. Gaps: what was not verified

## 1. Verification tags

| Tag | Meaning |
|---|---|
| OPENED | The source was opened and the claim was read there. |
| SECONDARY | The primary source was blocked. The claim was read in another opened source. |
| SNIPPET | Seen only in search-result text. Treat as unverified. |
| RECALL | From memory. Not checked. |

## 2. Vocabulary: how many unknown words a reader can accept

| Finding | Evidence | Source |
|---|---|---|
| Comprehension rises steadily with the share of known words. There is no sudden threshold. | 661 readers, 8 countries. 90% known words: about 50% comprehension. 95%: about 60%. 98 to 99%: about 70%. 100%: about 75%. (OPENED) | Schmitt, Jiang, Grabe 2011. https://www.lextutor.ca/cover/papers/schmitt_etal_2011.pdf |
| At 95% known words, most readers do not reach adequate comprehension. | Hu and Nation 2000, 66 learners. At 80% coverage: 0 readers adequate. At 90%: 19%. At 95%: 35 to 41%. (SECONDARY) | https://eric.ed.gov/?id=EJ626518 |
| 98% coverage needs about 8,000 word families. | 745 students. (OPENED) | Laufer and Ravenhorst-Kalovski 2010. https://files.eric.ed.gov/fulltext/EJ887873.pdf |
| Rare words cost second-language readers more time than they cost native readers. | 30 Chinese-English and 19 Dutch-English bilinguals. (OPENED) | Cambridge, Bilingualism: Language and Cognition |
| Word difficulty predicts text difficulty better than sentence measures. | Model on 1,181 texts. Strongest feature: age of acquisition of content words. (OPENED) | Cambridge, Studies in Second Language Acquisition |
| Specialised texts have many technical words. | 1 in 3 words in an anatomy text. 1 in 5 in an applied linguistics text. (OPENED) | Chung and Nation 2003 |

Rule: treat unknown words as a budget. Target at most 1 unknown word in 50 words (98% known). Every new term counts as unknown until the page defines it.

## 3. What is difficult for second-language readers

| Feature | Evidence | Strength |
|---|---|---|
| Idioms and multi-word expressions | 101 adult learners. Two texts used the same common words. When the words formed expressions such as "by and large", comprehension fell from 86.03% to 52.58%. Self-rated comprehension fell only from 87.38% to 60.29%. Readers overestimated what they understood. (OPENED) Martinez and Murphy 2011. | Strong |
| Metaphor | International students at a British university. About 40% of the difficult items made of familiar words involved metaphor. Students noticed the problem in only about 4% of cases. (OPENED) Littlemore et al. 2011. | Strong |
| Irony and sarcasm | 150 advanced speakers. Accuracy: 83% literal, 71% ironic. (OPENED) https://pmc.ncbi.nlm.nih.gov/articles/PMC10666523/ | Good |
| Garden-path sentences (the first reading is wrong) | Chinese-English bilinguals: 36.60% correct on garden-path sentences, 79.28% on normal sentences. (OPENED) https://pmc.ncbi.nlm.nih.gov/articles/PMC9539755/ | Strong |
| Phrasal verbs | 128 learners knew on average 40% of the meanings of very common phrasal verbs. (SECONDARY) Garnier and Schmitt 2016. | Medium |
| Cultural references | Readers recalled more of the own-culture text and distorted the foreign-culture text. (OPENED) Steffensen et al. 1979. | Classic |
| Passive voice | Understood, but slower. For surprising content, accuracy fell: native 79 to 83%, Japanese learners 64 to 66%, Mandarin learners 68 to 73%. (OPENED) | Medium |
| Ambiguous pronouns | A problem mainly when two possible referents are equally prominent, for example after "A and B". (OPENED) Contemori et al. 2019. | Specific |
| Single negation | Small effect: 99.21% against 97.89% accuracy. (OPENED) | Weak |
| Abbreviations | 73% of 18.2 million abstracts contain an acronym. Only 0.2% of acronyms are used regularly. (OPENED) Not specific to second-language readers. | Indirect |
| Noun stacks, nominalizations, double negatives | Style-guide rules exist. No second-language experiment was found. | Weak |

Key point: the reader often does not notice the misunderstanding. So the reader cannot ask about it. The writer must remove the risk.

Source for idioms: http://www.drronmartinez.com/uploads/4/4/8/2/44820161/effect_of_frequency_and_idiomaticity_on_reading_comprehension_martinez_and_murphy_tq_2011.pdf

## 4. Rules from controlled-language standards

| Standard | Concrete rules | Source |
|---|---|---|
| ASD-STE100 Simplified Technical English | Maximum 20 words per sentence in instructions, 25 in descriptions. Maximum 6 sentences per paragraph. No noun clusters longer than 3 words. Active voice. One meaning per word. (SECONDARY) | https://en.wikipedia.org/wiki/Simplified_Technical_English |
| US Federal Plain Language Guidelines | One idea per sentence. Paragraphs of 3 to 8 sentences. At most 3 abbreviations per document. Write "for example", not "e.g.". Avoid "and/or". Avoid hidden verbs. (OPENED) | https://digital.gov/guides/plain-language/writing/clear-short |
| ISO 24495-1:2023 | Success is measured by how well readers can use the document, not by readability formulas. (OPENED, preview pages) | ISO preview |
| Microsoft Style Guide, global communications | Keep "that" and "who". Keep articles. At most two phrases joined with "and", "or", "but". One word for one concept. (OPENED) | https://learn.microsoft.com/en-us/style-guide/global-communications/writing-tips |
| Google developer style guide, translation | Avoid phrasal verbs. At most two nouns as modifiers. Replace an unclear pronoun with the noun. (OPENED) | https://developers.google.com/style/translation |
| Simple English Wikipedia | Subject, verb, object order. At most one subordinate clause. No idioms. No contractions. (OPENED) | https://simple.wikipedia.org/wiki/Wikipedia:How_to_write_Simple_English_pages |

Evidence that Simplified English works: 175 aircraft technicians understood significantly more, "particularly for the Difficult workcards and for non-native English speakers". (OPENED, abstract) https://researchconnect.buffalo.edu/en/publications/simplified-english-for-aircraft-workcards/

## 5. Sentence length and readability scores

| Finding | Evidence | Source |
|---|---|---|
| The popular numbers on sentence length have a weak source. | GOV.UK cites "14 words: more than 90% understood, 43 words: less than 10%". The source is a writing trainer, not a study. Do not quote these numbers as research. (OPENED) | GOV.UK blog, 2014 |
| Readability formulas predict difficulty poorly for second-language readers. | On 300 texts in 3 levels, Flesch-Kincaid classified 49.3% correctly. Chance is 33.3%. (OPENED) | Crossley et al. 2011. https://files.eric.ed.gov/fulltext/EJ926371.pdf |
| Simplified text helps, but the gain is modest. | 48 learners. Comprehension: 0.81 beginner version, 0.76 intermediate, 0.72 original. (OPENED) | Crossley et al. 2014. https://files.eric.ed.gov/fulltext/EJ1031308.pdf |
| Explicit connectives help. | Readers benefit from "because" and "therefore" in first and second language. (OPENED, abstract) | Degand and Sanders 2002 |

Rule: sentence length is a limit, not a goal. Do not delete connectives to reach a score.

## 6. Definitions of terms (glosses)

| Finding | Evidence | Source |
|---|---|---|
| Glosses help word learning. | 42 studies, 3,802 participants. With glosses: 45.3% of target words known. Without: 26.6%. (OPENED, abstract) | Yanagisawa et al. 2020 |
| First-language glosses worked better than second-language glosses. | Same meta-analysis. | Same |
| A separate glossary is among the least effective forms. | Same meta-analysis. | Same |
| A gloss next to the word gives lower load and better comprehension than a gloss in the margin. | 39 learners. (OPENED) | Marefat et al. 2016. https://www.jite.org/documents/Vol15/JITEv15ResearchP478-501Marefat2692.pdf |
| For comprehension, the effect of glosses is less reliable than for vocabulary. | 56% of first-language gloss studies found no significant comprehension effect. (OPENED) | Taylor 2014 |

Rule: define the term in the sentence where it first appears. The glossary at the end is a backup. If the reader's first language is known, add the first-language word for each key term.

Note: gloss studies disagree about pop-up definitions. Separate research on web pages shows that most readers never see hover content (see evidence-page-design.md, section 2). For this reason, this skill puts definitions in visible text.

## 7. One term for one concept

All standards demand it (section 4). Direct experiments are rare. One author searched for experiments and found none. Indirect evidence: word overlap between neighbouring sentences is one of three variables in an index that explained 86% of the variance in second-language reading difficulty (Crossley et al. 2011, OPENED).

Logic: each synonym is one more word that may be unknown. It also makes the reader ask "is this the same thing?".

Confidence: high that the rule is right. Low for a measured effect size.

## 8. Simplify or elaborate

| Study | Result |
|---|---|
| Yano, Long, Ross 1994. 483 Japanese college students. (OPENED, abstract) | Simplified was highest, but not significantly different from elaborated. |
| Rahimi and Rezaei 2011. 185 engineering students, science texts. (OPENED) | Both improved comprehension about equally. |
| Later review (SECONDARY) | Elaborated text appears better for higher-level understanding. |

"Elaborated" means: keep the original content and terms, and add a definition, a paraphrase, an example, or the reason.

Rule: do not remove content or precise terms. Add support. Then keep each sentence short. The page becomes longer. That is acceptable.

## 9. Typography

| Finding | Evidence | Source |
|---|---|---|
| About 55 characters per line gave better comprehension than 100. | (SECONDARY) | Dyson 2004 |
| Maximum 80 characters per line. | WCAG 1.4.8 (OPENED) | W3C |
| Larger text is better. | 104 participants. Comprehension was significantly better at 18 and 26 points. Texts were in Spanish, on an old monitor. (OPENED) | Rello et al. 2016. https://pielot.org/pubs/Rello2016-Fontsize.pdf |
| Line spacing about 1.5. Extremes (0.8 and 1.8) were worse. | Same study, and WCAG. (OPENED) | Same |
| Left-aligned is better than justified. | (OPENED, abstract) | Ling and van Schaik 2007 |
| Typography is not the main factor for non-native readers. | 459 adults (native English, Spanish, Mandarin). Font width and spacing had "minimal impact". Content was the main factor. (OPENED, abstract) | UCF dissertation 2024 |

Rule: follow normal good practice. Spend the effort on words and content.

## 10. Numbers, units, dates

All sources are guidance documents, not experiments. All OPENED.

| Risk | Rule | Source |
|---|---|---|
| 03/04/2026 means 4 March in the USA and 3 April in most of Europe. | Write "27 September 2026" or "2026-09-27". | https://www.w3.org/International/questions/qa-date-format |
| The comma is the decimal marker in many countries. | Use a period as the decimal marker. Write 0.25, not .25. Use one grouping style in the whole page. | NIST SP 811, chapter 10 |
| "Billion" means 10^12 in some countries. | Show the digits next to the word: "2 billion (2,000,000,000)". | NIST SP 811, chapter 7 |
| Seasons differ between hemispheres. | Name the month, not the season. | Microsoft Style Guide |
| Chinese, Japanese, and Korean group large numbers by 10,000. (RECALL) | Showing the digits helps the reader convert. | Not verified |

## 11. Pictures, tables, worked examples

| Finding | Evidence |
|---|---|
| Words plus pictures beat words alone. | General evidence is strong, but effect sizes from independent studies are modest (see evidence-learning.md). |
| Evidence specific to second-language readers is positive but mixed. | A 2022 review: most studies favour words plus pictures. Some find no difference. (OPENED) |
| A diagram of text structure helps only if it matches the real structure of the content. | Jiang and Grabe 2007. (OPENED) |
| Tables and lists | Microsoft and ASD-STE100 tell writers to replace complex sentences with lists and tables. No second-language experiment was found. |

## 12. Gaps: what was not verified

- ASD-STE100 official text: the site refused access. Rules come from secondary sources.
- ISO 24495-1 full text: only the preview pages were read.
- Hu and Nation 2000 original: a scanned file without readable text.
- No second-language experiments were found for: abbreviations, nominalizations, double negatives, tables, synonym variation.
- Not researched: whether words of Latin origin are harder for readers with a Chinese, Japanese, or Korean first language.
- The font size "17 px" in the standard styles is a design judgment. The research value is "18 points or larger", from one study on an old monitor.
