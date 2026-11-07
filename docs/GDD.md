# Boss & Boss: Game Design Document

Version 0.9 · November 2026 · Owner: JP (Richmark Training / ENSY Training Services)

---

## 1. One-line pitch
You own a Malaysian company **and** you are its HR department. Every week someone walks in with a problem. Swipe left or right. Keep the business alive for 3 years without going bankrupt, getting shut down, or being loved so much your staff take over.

## 2. Why this game exists
| For | What it gives them |
|---|---|
| **Players** | A quick, funny, very Malaysian game (10–15 min a run) that feels like real office life |
| **Trainers (JP)** | A ready-made workshop activity that produces debrief material: who broke which law, where the room disagreed, hidden hiring bias |
| **Client companies** | An HR, compliance and leadership session staff actually enjoy, with a CSV record for training reports |

Market context (from research, Nov 2026): only one direct HR game has real traction on Steam (*Thank You For Your Application*, darkly comic). No game covers a **sympathetic, rules-grounded, Malaysian** HR experience, small business HR, or a hiring-bias log for debriefs. Evidence on game-based training favours **replay + facilitated debrief**, which is built in.

## 3. Design pillars
1. **Every choice is a trade-off.** No option is free; being "nice" every time also loses.
2. **Real rules, simplified.** Situations come from Malaysian employment law and practice; the debrief says what the law actually says.
3. **Malaysian, warm, funny.** Humour comes from situations and personalities, never from mocking a race, religion or group.
4. **Short and replayable.** Losing in 3 minutes is fine; the second run is where learning starts.
5. **Simple and auditable.** Plain files, no server, no tracking. Anyone can read what the game does and what a result code contains.

## 4. Core loop
```
Read the card → (preview: dots show which meters move) → swipe left/right
   → meters change → weekly income → maybe quarterly result / economic shock
   → check endings → next card
```
- One card = one week. 52 weeks = 1 year. **Win at week 156 (3 years).**
- Input: swipe the card, tap the two buttons, or ← → keys. Esc pauses.

## 5. The four meters
All start at **50**. Range 0–100. **Hitting 0 or 100 on any meter ends the run.**

| Meter | 0 ending | 100 ending |
|---|---|---|
| 💰 Cash | Bankrupt | Bought Out (a conglomerate replaces you) |
| 🙂 Morale | The Great Resignation | Staff Takeover |
| ⚖️ Compliance | Shut Down (Labour Department) | Death by Paperwork |
| 📣 Reputation | Viral for the Wrong Reasons | LinkedIn Guru |
| (survive 156 weeks) | **The Legacy** (win) | |

**Preview dots:** while hovering or dragging, a dot appears above each meter that will change: small (<10), medium (10–14), large (15+). Direction is hidden on purpose: the player must read the situation.

**Warnings:** crossing below 20 or above 80 shows a warning toast and sound, and the meter turns red.

## 6. Systems and numbers (as built)
| System | Rule |
|---|---|
| Card effects | Each option has `[cash, morale, compliance, reputation]`, typically −25…+25 |
| Difficulty ramp | Effects × `1 + min(1, week/156) × 0.6` → up to **1.6×** by year 3 |
| Weekly income | +1 cash every week |
| Quarterly result | Every 13 weeks: cash += round((morale − 45) / 4). Happy teams sell more |
| Economic shocks | Every 26 weeks (week 13, 39, 65…): one random event, e.g. ringgit dip (−8 cash), new labour amendment (−8 compliance), award nomination (+5 morale, +5 rep) |
| Anniversary | Week 52, 104: special celebration card |
| No repeats | The last 12 cards can't reappear; `once` cards appear once per run |

Balance target: a random player survives ~10–30 weeks; a careful player can reach 3 years; a perfect-information bot always wins (tested).

## 7. Card system
| Card type | How it behaves | Example |
|---|---|---|
| **Regular** | Drawn at random | Aircond broke, 34°C |
| **Once** | Appears at most once per run | Aina announces she's pregnant |
| **Follow-up** (`req` + `next`) | Queued N weeks after a specific choice | Kevin hired → 3 weeks later, staff complain about Kevin → Uncle Lim threatens to pull out → Kevin asks to be mentored |
| **Crisis** (`cond`) | Eligible only when a meter is extreme; 50% chance to jump the queue (7 in base game) | Cash < 25: "Pay salaries late?" |
| **Pack card** | From the chosen industry; 50% of draws when a pack is active | Mamak: halal certificate expired |
| **Intro** | First card of a run; each pack has its own | "Welcome to Bayan Lepas, boss!" |

**Draw order each week:** anniversary → due follow-up → crisis (50%) → pack card (50%) → base card.

Content (v0.9): **78 base cards** + **80 pack cards** (10 packs × 8, plus an intro each) = 158 situations: **43 with law tips**, **7 hiring-bias situations**, **13 choices that trigger story follow-ups**, **7 crisis cards**.

## 8. Industry expansion packs
Chosen on the start screen. Each pack = 4 local characters + intro + 8 situations, mixed with the base deck.

| Pack | Signature issues |
|---|---|
| 🔌 E&E Factory, Penang | Recruitment-fee debt, passport retention, hostel standards, automation |
| 🌴 Oil Palm Estate, Sabah | Heat stress, elephants, child labour & MSPO/RSPO, haze |
| 🛢️ Oil & Gas, Terengganu | Fair retrenchment, rotations, stop-work authority, typhoon evacuation |
| 🍛 Mamak Restaurant Chain | Tip skimming, halal certification, typhoid jabs, night allowance |
| 🏝️ Island Resort, Langkawi | Service-charge distribution, monsoon layoffs, VIP pressure |
| 🏗️ Construction, Cyberjaya | Fall protection, CIDB Green Card, subcontractor wages, MACC s.17A |
| 🚛 Logistics, Port Klang | 11.11 hour caps, driver fatigue, contractor misclassification, PDPA |
| 🏦 Bank HQ, KL Sentral | AI Copilot rollout, AML training, mis-selling KPIs, whistleblowing |
| 🏥 Private Hospital, JB | Singapore brain drain, nurse ratios, patient confidentiality |
| 💻 Tech Startup, Cyberjaya | 4-day week, layoff-by-email, monitoring software, moonlighting |

## 9. Characters and tone
- Every character has a **name, role, emoji fallback, colour, and a one-line bio** that gives them a personality (e.g. Uncle Lim: *"Invested RM50k in 2009. Mentions it every Chinese New Year."*).
- Core cast (base game): Aina, Faizal, Mei Ling, Raj, Siti, Jess, Kak Ros, Uncle Lim, Encik Hafiz (Labour Dept), Datin Rosnah, Kevin, plus visitors.
- **Tone rules:** warm, observational humour about office life. Use Manglish lightly ("can or not", "lah", "boss"). Diverse cast across ethnicity, age, gender, faith, ability. Never make a group the joke. Villains are behaviours (cutting corners), not people types.

## 10. Endings and debrief (the training layer)
At the end of each run the player sees:
| Element | How it's calculated |
|---|---|
| **HR style** | From the two scores below: Trusted Boss (law ≥80, people ≥60), By-the-Book (law ≥80), Big-Hearted Risk-Taker (people ≥60), Corner-Cutter (law <50), else Pragmatist |
| **People-first vs Profit-first** | Of decisions where morale and cash moved differently: % where morale gained more than cash |
| **Followed the law** | Of cards that have a law tip: % where the player didn't pick the risky option |
| **Pattern spotted** | Each bias-tagged choice taken (age, origin, parent, language, disability, gender) with a reflection question |
| **What the law says** | Each risky choice with the simplified legal rule |
| Endings found | Collection of the 9 endings across runs (saved on the device) |

## 11. Workshop mode
1. Trainer gives a **workshop code** and **industry**; the code seeds the randomness so everyone gets the same sequence (follow-ups still depend on each player's choices).
2. At the end, players send a **result code** (copy, or WhatsApp in one tap). Name is optional.
3. Trainer opens **Trainer view**, pastes the codes (whole WhatsApp messages are fine) and sees: endings, average scores, most common legal shortcuts, hiring patterns in the room, **most divided decisions**, and the player list. **Download CSV** for records.
4. All results stay on the trainer's device. No server.

Suggested 45-minute module: 5 min intro · 15 min play (restarts allowed) · 3 min send codes · 17 min debrief · 5 min takeaways.

## 12. Languages
English (built in), Bahasa Melayu, 华文, தமிழ். Base game fully translated in all four; pack names translated, pack cards English for now. Chinese and Tamil need native review.

## 13. Art and audio
- **Current:** cream cards on dark teal, amber accents, Bricolage Grotesque type. Characters use art files when present (`art/<id>.svg|png`), otherwise emoji.
- **Direction candidates:** see the art style exploration page (newspaper cartoon, kopitiam/Peranakan retro, and others). Decision pending.
- **Audio:** small synthesized sounds (swipe, up/down, warning, start, ending). Mute toggle.

## 14. Platforms and distribution
| Platform | How |
|---|---|
| Any browser | Static folder on a web host (GitHub Pages planned: isotope8.github.io/boss-and-boss) |
| Phone (iOS/Android) | Install from browser ("Add to Home Screen" / "Install app"); works offline |
| Windows / Mac | Install from Chrome/Edge (Safari: Add to Dock), or double-click `index.html` |
| Steam (future) | Wrap the same folder in a desktop shell (e.g. Electron) |

## 15. Editions and business model (proposal)
| Edition | Contents | Price idea |
|---|---|---|
| **Free web** | Base game + 1–2 packs, English/BM | Free (marketing funnel) |
| **Training edition** | All packs, Trainer view, facilitator guide, client-specific packs | Per-workshop or per-seat licence, bundled into HRD Corp-claimable programmes (eligibility to be confirmed) |
| **Steam** | Polished art, all packs, achievements | ~USD 5–10 (simulator sweet spot is USD 10–15 for 8–15 h; this is a shorter game) |
| **Custom packs** | A client's own industry, policies and characters | Project fee |

## 16. Roadmap
1. Choose art direction → draw full cast (56 characters).
2. Translate pack cards into BM, Chinese, Tamil; native review.
3. Legal review of every law tip by a Malaysian employment practitioner.
4. GitHub Pages launch → pilot in 2–3 workshops → tune balance from CSVs.
5. Facilitator guide (slides + debrief questions per pack).
6. Steam: art, achievements, store page, Next Fest demo.

## 17. Risks
| Risk | Mitigation |
|---|---|
| Law tips out of date or oversimplified | Disclaimer on every screen; practitioner review; dated "as of 2025" |
| Cultural missteps | Tone rules (§9); native reviewers for each language; diverse playtesters |
| Art looks generic | Commit to a distinctly Malaysian style (§13) |
| HRD Corp claimability of a game component | Confirm with HRD Corp before selling the training edition |
| Crowded "simulator" market on Steam | Lead with the hook (Malaysian satire + real rules), not "HR Simulator" |
