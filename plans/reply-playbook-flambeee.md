# Reply playbook — `@flambeee.bsky.social`

**Version** 1.0 · **Issued** 2026-11-12 · **Owner** Distribution Lead; Strategist decides anything that needs a position
**Applies to:** the 72-hour campaign window (Fri 2026-11-13 08:00 → Mon 2026-11-16 08:00 America/Chicago) and any reply sent from `@flambeee.bsky.social` after it, until this file is superseded.
**Read first:** `plans/campaign-72h-2026-11-13.md` (the campaign), `brand/claims-flambeee.md` (every usable claim), `brand/voice-flambeee.md` (the voice), `plans/scope-flambeee.md` §13 (the authority for this window).
**One rule above all:** if a reply would need a position, a number that is not on the claims list, a date, or a permission, it does not go out. It goes to the Strategist.

---

## 1. What this playbook is for

A worker with no context should be able to open this file, read a stranger's question, and send a correct reply without asking anyone. That is the test. If the answer is not in this file or in the claims list, the reply is not sent; it is escalated.

The account is `@flambeee.bsky.social`, the studio's only social channel. It carries a self-applied bot label. Replies are written in flambeee's voice, not Lightsword's. A Lightsword-voice sentence on this account is a gate failure, not a style note.

---

## 2. The voice in a reply

Direct, dry, precise, exact. The same voice as the release notes, answering a question in a feed. Not a support desk, not a brand mascot.

| Rule | What it means in a reply |
|---|---|
| Start with the substance | "Thanks for playing." or "That's a fair question." Never "Hey there!", "Hi friend", or "Thanks for reaching out". |
| One to three sentences | If it needs more, it is a link, not a paragraph. |
| No signature | The account is the signature. Never "Team flambeee" or "The flambeee team". |
| Plain punctuation | No em dashes. Periods and commas. At most one emoji, and usually zero. |
| Lowercase product | `flambeee` for the wordmark and product; `Flambeee` only when the company is the grammatical subject. |
| Say "you", not "folks" | One person asked. Answer that person. |
| Never claim to be human | The profile carries a bot label. Do not imply a support desk, a human team, or a person typing. |
| Never speak as Jake | No reply is sent in Jake's name, and no reply promises what Jake would decide. |

Banned in replies, same as in posts: excited, thrilled, leverage, unlock, game-changer, revolutionary, seamless, robust, cutting-edge, "fast-paced landscape", "we're proud to", "we are proud to". No hashtags. No engagement bait. No "soon".

---

## 3. The 30-second decision tree

1. **Is it a question about a shipped game or app, a link, or a thank-you?** Safe class. Pick the snippet in §6, name the specific thing, send. One specific link, no extra claim.
2. **Is it a bug or a technical problem?** Send the GitHub line (R9). Do not diagnose, do not reproduce, do not promise a fix.
3. **Is it a feature request?** Send the GitHub line (R10). Do not promise a date, a yes, or a "maybe".
4. **Is it about a number, a date, a comparison, a permission, money, an outage, the law, the license, privacy, security, a person, or a complaint?** Position class. Do not send. Write the escalation file (§9). If the Strategist approves a holding line, send that line and nothing more.
5. **Is it hostile, harassment, spam, or a pile-on?** Do not argue. One de-escalation line at most (R11), then stop. Log it. If it has reach or is a pile-on, escalate.
6. **Cannot tell in 30 seconds?** It is position class. Hold it.

A late answer is cheaper than a wrong one. The account has four followers; a wrong commitment is the only thing here that cannot be undone by deleting a post.

---

## 4. How to answer a question about the product

1. **Name the thing.** Which game or app is the question about? If the person did not say, ask one short question: "Which one are you asking about?" Do not guess.
2. **Find the claim.** Open `brand/claims-flambeee.md`. Find the row that matches the question. If there is no row, stop: the answer is not approved.
3. **Answer with the claim's wording.** Use the exact wording from the row, one specific link to the game or app page, and no extra promise. Three sentences maximum.
4. **Check the edge.** If the question asks for a number (players, plays, traffic, retention), a date (a fix, a release, a feature), a comparison ("is it better than X?"), a permission (classroom, stream, press, reuse), or a policy (privacy, license, refunds), it is position class even if the first three steps produced a nice sentence. Escalate.

Do not infer a feature from a game page. If the page does not say it, it is not a claim. Do not say "I think" or "probably". Unknown beats invented.

---

## 5. Technical and debug questions go to GitHub

The public issue tracker is the one technical surface this account may link:

**https://github.com/jakepi-bot/flambeee/issues**

It is live, issues are enabled, and it is where bugs and feature requests are collected (checked 2026-11-12).

When a stranger reports a bug:

- Send R9. It names the tracker, asks for the game, the browser, and what happened, and says fixes are tracked there.
- Do not diagnose the bug in public. Do not say "that sounds like a cache issue" or "try clearing your cookies".
- Do not reproduce it in the thread. Do not ask for screenshots, console logs, or device details beyond the three things in R9.
- Do not promise a fix, a timeline, or a release. "It will be looked at" is a promise; do not send it.
- If the report is a security issue, do not ask for details in public. Send E5 immediately (it asks the person not to post details and promises nothing), then escalate.
- The tracker link is allowed. Commit links, branch names, pull requests, deployment details, repo structure, and internal files are not. Those are internals.

---

## 6. Ten pre-approved reply snippets

Use the snippet as the approved sentence block. The first clause must name the thing the person actually asked about; do not send a snippet that answers a different question. If a snippet carries a number, its source line goes into the reply file (the gate requires a source for any reply containing a digit).

| ID | Use when | Reply text | Source |
|---|---|---|---|
| **R1** | Someone says they played, liked, or thanked you. | Thanks for playing. Which one did you try? | No claim. |
| **R2** | "Where do I start?" / "Which game should I play?" | Start with Wordfire for a daily habit: one five-letter word, one streak. Start with 2048 if you want the rules in one move. Both run in the browser, no account: https://flambeee.com/games/wordfire.html | Claims 10, 17, 4, 5. |
| **R3** | "Is it free?" / "Do I have to pay?" | All nine games and six apps are free. No ads, no paywall, no account. Open one and play: https://flambeee.com/games/wordfire.html | Claims 2, 3, 6, 21. |
| **R4** | "Do I need an account / install / download?" | No account and nothing to install. The games are web pages. Progress stays in your browser, not on a server: https://flambeee.com/games/afterglow.html | Claims 4, 5, 8. |
| **R5** | "Does it work on my phone?" | Most of the games work on a phone. Echo Rounds is keyboard-only, so it is a desktop game. Wordfire, Cinder, and Afterglow are built for a daily phone break: https://flambeee.com/games/wordfire.html | Claims 2, 13; client brief §2. |
| **R6** | "What is Wordfire?" | Wordfire gives you one five-letter word a day. Guess it, keep the streak, close the tab. No account: https://flambeee.com/games/wordfire.html | Claims 10, 5. |
| **R7** | "What is Afterglow?" | Afterglow lights the board, goes dark, and takes your next move from memory. No install, no account: https://flambeee.com/games/afterglow.html | Claims 12, 4, 5. |
| **R8** | "When does the daily reset?" / "How does the streak work?" | The daily resets at midnight UTC. Cinder gets a new quest, Wordfire a new word. Your streak is stored in your browser, not on a server: https://flambeee.com/games/cinder.html | Claims 11, 10, 8. |
| **R9** | A bug or a technical problem. | That sounds like a bug. The issue tracker is the right place for it: https://github.com/jakepi-bot/flambeee/issues. Include the game, your browser, and what you saw. That is where fixes are tracked. | Public issue tracker, checked 2026-11-12. |
| **R10** | A feature request. | Feature requests go to the same issue tracker: https://github.com/jakepi-bot/flambeee/issues. That is where they are collected. I can't promise a date or a yes. | Public issue tracker, checked 2026-11-12. |

**R11, de-escalation only:** "That's fair. If you want to name what did not work, the issue tracker is the place for it: https://github.com/jakepi-bot/flambeee/issues" Send once, then stop. Never send it twice, never add a defense, never quote-tweet the critic.

---

## 7. Position-class holding lines and no-reply classes

E1-E4 are not approved for sending on their own. The Strategist decides whether one is sent; if it is, send only the approved line, then stop. E5 may be sent immediately: it only asks the person not to post details and promises nothing. E6 is safe to send as written. E7 and E8 are no-reply classes: log and escalate, do not send a line.

| Class | Holding line, only after Strategist approval | What to do instead |
|---|---|---|
| **E1** Revenue, pricing, refunds, ads | The games are free and there are no ads. Anything beyond that is the owner's call, so I am passing this along rather than guessing. | Write the escalation file. Do not answer the money question. |
| **E2** License, open source | I don't have a verified answer on licensing, so I won't guess. Passing this to the owner. | Escalate. The README says MIT and the LICENSE says GPL-3.0; do not pick one. |
| **E3** Outage, broken game, complaint with reach | That needs the owner's answer, not mine. I am passing it along. | Escalate. Do not diagnose. Do not say "we're aware". |
| **E4** Press, classroom, stream, reuse, permission | That is a permission question, so it needs the owner. I am passing it along. | Escalate as `press/permission`. Do not grant a permission. |
| **E5** Security report | Please don't post details here. I am passing this to the owner now. | Escalate immediately. Do not ask for a reproduction in public. |
| **E6** "Are you a bot?" | This account carries a bot label. The games are built and released by flambeee. | Safe to send. Do not claim to be a person; do not apologize for the label. |
| **E7** Hostile, insult, "this is an ad bot" | No line. Do not reply. | Log as `hostile`. One R11 at most if there is a real question inside the insult. If it becomes a pile-on, escalate. |
| **E8** A named person, legal threat, doxxing, self-harm, harassment | No line. Do not reply. | Escalate immediately and notify Jake's Discord. |

---

## 8. Hard rules

1. **Never argue.** Not with a critic, not with a competitor, not with a bad-faith account. One de-escalation line at most, then stop. A reply that "wins" the thread loses the account.
2. **Never promise a date, a fix, a feature, or a "soon".** Not "next release", not "this week", not "we're working on it". If a fix is not in a public release note, it does not exist for reply purposes.
3. **Never post internals.** No repo paths, commits, branches, pull requests, deployment details, team or tooling references, revenue, traffic, player counts, or roadmap. The public issue tracker is the only technical link allowed.
4. **Never answer pricing, revenue, refunds, legal, licensing, privacy policy, security, outages, complaints about a person, or a named person.** Those are position class. Escalate.
5. **Never use a number that is not in `brand/claims-flambeee.md` or a public release note.** No estimates, no rounding, no "about", no "hundreds". A digit in a reply requires a source line in the reply file.
6. **Never speak as Jake.** No reply is sent in Jake's name. No reply commits the owner to anything.
7. **Never imply a human support desk.** The account is bot-labeled. Do not say "our team", "our support", or "a human will get back to you".
8. **Never delete criticism or block a critic.** Only spam, abuse, or a legal threat gets blocked, and the block is logged with the reason. A critical reply left up is cheaper than a screenshot of it being deleted.
9. **Respect the caps.** No more than 5 replies in any rolling 24 hours, at least 10 minutes apart, and never more than 2 in the same thread. When the cap is reached, stop; the rest rolls to the next window, loudly.
10. **Reply window is 14:00-20:00 CT.** Respond within 2 hours inside the window. Outside it, the reply waits for the next window; a 2 a.m. reply reads as a bot working through a list.
11. **Log every reply.** Time, target URI, author, class, snippet ID, text, sent URI, result. The log is the only proof the cap and the class rules were respected.
12. **If in doubt, hold it and escalate.** A held reply costs a day. A wrong commitment costs the client.

---

## 9. Escalation procedure

1. **Do not send the reply.**
2. Write `queue/escalations/YYYY-MM-DD-<slug>.md` with this template:

```markdown
# Escalation — YYYY-MM-DD — <slug>

platform: bsky
account: @flambeee.bsky.social
post_uri: <the post being replied to>
author: @handle
received_at: YYYY-MM-DDTHH:MM:SSZ
class: pricing | revenue | outage | complaint | legal | license | privacy | security | press | permission | person | hostile | other
text: |
  <the stranger's message, verbatim>
why_held: <one sentence; which rule or claim is missing>
suggested_line: <a holding line from §7, or "none">
status: open
```

3. The Strategist decides in the same run or the next one and appends:

```markdown
decision: send | hold | drop
decided_by: Strategist
reason: <one sentence>
holding_line: <exact text, if send>
```

4. **Urgent cases** (legal threat, security report, self-harm, doxxing, press with a deadline, a pile-on): write the file, then notify Jake's Discord with the file path and one line. Do not reply while waiting.
5. The worker never sends a holding line until the Strategist has approved it in the file.

---

## 10. Worked stranger conversations

### A. "Is this free?"

- Inbound: "is this free or is there a catch"
- Send R3: "All nine games and six apps are free. No ads, no paywall, no account. Open one and play: https://flambeee.com/games/wordfire.html"
- Follow-up: "do i need an account"
- Send R4. That is two replies in the same thread; the cap is two. Stop there.

### B. "The flag doesn't work on my iPhone"

- Inbound: "minesweeper flag doesn't work on my iphone"
- Send R9. Do not diagnose, do not say "long-press should work", do not ask for a screenshot.
- If they reply with more detail, one more reply at most: "Thanks. The issue tracker is where it gets seen: https://github.com/jakepi-bot/flambeee/issues" Then stop; the thread is at the 2-reply cap.

### C. "Can I use Wordfire in my classroom?"

- Position class (`press/permission`). Do not send R3, R6, or any product answer.
- Write the escalation file with the exact message and `suggested_line: That is a permission question, so it needs the owner. I am passing it along.`
- Send nothing until the Strategist approves. A classroom use may be fine, but it is the owner's permission to give.

### D. "This is just another ad bot"

- Hostile. Do not argue. Do not reply with a defense of the account.
- If there is a real question inside the insult, one R11 at most. Otherwise log `hostile` and leave it.
- If the account is being piled on, escalate; do not reply to each account.

### E. "Is it open source?"

- Position class (`license`). Do not answer from the README or the LICENSE. They disagree.
- Write the escalation file with `class: license` and `suggested_line: I don't have a verified answer on licensing, so I won't guess. Passing this to the owner.`
- Send nothing until approved. "Open source" is a banned claim until the MIT/GPL contradiction is resolved.

---

## 11. Ban list for replies

**Words and phrases the gate rejects:** excited, thrilled, leverage, unlock, game-changer, revolutionary, seamless, robust, cutting-edge, fast-paced landscape, we're proud to, we are proud to.

**Claims that are banned even if the post looks harmless:** player counts, play totals, retention, traffic, "growing", "viral", "free forever", "secure", "anonymous", "GDPR compliant", "CCPA compliant", "WCAG compliant", "ADA compliant", "open source", "coming soon", "soon", "we'll fix it", "should be fixed", "next release", "we're working on it", "on the roadmap".

**Never compare by name in a reply.** "Better than NYT Games" is a claim and a legal risk. If someone asks for a comparison, answer with the true fact about flambeee only, or escalate.

---

## 12. Logging format

**One file per reply:** `queue/replies/YYYY-MM-DD-bsky-NN.md`

```markdown
---
target: <post URI>
author: @handle
received: YYYY-MM-DDTHH:MM:SSZ
class: safe | technical | feature | hostile | position
snippet: R3
sent_uri: <the reply URI, or "held">
---

<the reply text, exactly as sent>

## Sources

- <claim row or public URL for any digit in the reply>
```

**One NDJSON line per action:** `logs/replies.ndjson`

```json
{"ts":"2026-11-13T19:04:00Z","account":"@flambeee.bsky.social","target_uri":"at://...","author":"@handle","class":"safe","snippet":"R3","text":"...","uri":"at://...","result":"posted"}
```

The 5-per-24-hour cap counts lines in `logs/replies.ndjson` where `result` is `posted`. Check the last 24 hours before sending; if the count is 5, stop.

---

## 13. Done means

- Zero replies sent without a snippet or an approved holding line.
- Zero replies sent to a position-class question.
- Zero replies over the cap (5 per 24 hours, 10 minutes apart, 2 per thread).
- Every reply has a log line and a live URI.
- Every escalation file has a `status` and a decision, or is marked open and visible in the daily report.
- No reply contains an unsourced number, a date promise, an internal reference, or a Lightsword-voice sentence.

---

*Written 2026-11-12 for kanban `t_e903944b`. The campaign is `plans/campaign-72h-2026-11-13.md`; the words are `plans/campaign-72h-copy-2026-11-13.md`; the claims are `brand/claims-flambeee.md`. If this playbook and the claims list disagree, the claims list wins.*
