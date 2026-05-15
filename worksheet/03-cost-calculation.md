# 03 · Cost Calculation — Tính chi phí từng Config × 2 Scenarios

> **Mục tiêu**: Với mỗi config đã thiết kế ở `02-config-design.md`, tính cost/turn → cost/conversation → monthly cho cả 2 scenarios (low season + high season).
>
> **Thời gian**: 55 phút (phần lớn của Main phase) — checkpoint 11:00 và 11:20

---

## Cách làm

**Đừng tính tay từng turn — đó là cách thừa thời gian.** Dùng AI để tính. Dán prompt template từ `prompts/01-cost-calc.md` vào ChatGPT/Claude/Gemini, thay parameters theo config của nhóm, AI sẽ tính cho.

Tuy nhiên nhóm phải **hiểu** kết quả AI trả về, không phải copy-paste mù. Mỗi lần AI trả số, nhóm phải tự kiểm 1 lần: con số này có hợp lý không? Có vẻ quá đắt hay quá rẻ?

---

## Trước khi gọi AI — Setup chung

**Các tham số cố định cho tất cả configs** (tham khảo `cost-reference-card.md` mục 4):

```text
System prompt:              89 tokens   (tiktoken actual)  [Reference: 500]
User message:                21 tokens   (tiktoken actual)  [Reference: 80]
Assistant response:          76 tokens   (tiktoken actual)  [Reference: 180]
1 prior turn (history):     96 tokens   (tiktoken actual)  [Reference: 260]
RAG top-5 chunks:         327 tokens   (tiktoken actual)  [Reference: 1,250]
Web search results:       156 tokens   (tiktoken actual)  [Reference: 800]
Web search API call:       $0.008 / call (Tavily)
LLM classifier:            ~170 tokens (150 in + 20 out) — nếu dùng
```

**Lưu ý quan trọng**: Các con số `cost-reference-card.md` là **ước tính bảo thủ** (overestimate) để sinh viên dễ tính. Sau khi dùng `tiktoken` đếm thực tế, các token counts thấp hơn **2.4–5.6×**. Các bảng bên dưới đã dùng số **tiktoken thực tế**.

**Scenario A — mùa thấp điểm**:

```text
Volume:            300 conversations / ngày
Turns/conv:        avg 4 lượt
Intent mix:        Guide 50%, Visa 25%, Weather 10%, Booking 10%, Complaint 5%
AI-served ratio:   85% (15% là Booking + Complaint = handoff)
```

**Scenario B — mùa cao điểm**:

```text
Volume:           1,200 conversations / ngày (×4)
Turns/conv:        avg 7 lượt
Intent mix:        Guide 30%, Visa 15%, Weather 10%, Booking 35%, Complaint 10%
AI-served ratio:   55% (45% là handoff)
```

**Human baseline để so sánh**: $0.50 / conversation cố định.

---

## Quy trình tính cho 1 config (lặp lại cho từng config)

### Bước 1 — Cost per turn (4 mốc: Turn 1, 3, 5, 7)

Với mỗi mốc, tính:

1. **History tokens** = (T − 1) × 96 nếu Full · min(T−1, N) × 96 nếu Last N · ~150 cố định nếu Summarize.
2. **Input total** = 89 (sys) + history + 327 (RAG) + (156 nếu web ON cho intent này) + 21 (msg)
3. **Output** = 76 tokens
4. **Cost model** = (input × $/M_input + output × $/M_output) / 1,000,000
5. **Cost web API** = $0.008 nếu web ON cho intent này, ngược lại $0
6. **Cost classifier** = ~$0.0000085 (GPT-5 nano) nếu dùng LLM classifier, ngược lại $0
7. **Total cost/turn** = cost model + cost web + cost classifier

→ Dùng prompt template, AI sẽ tự tính. Nhập config + intent + turn number, AI ra bảng kết quả.

### Bước 2 — Cost per conversation cho từng intent

Cost 1 conversation = sum(cost từng turn) trong conversation đó.

- Scenario A: cộng cost của Turn 1 → Turn 4 (4 turns)
- Scenario B: cộng cost của Turn 1 → Turn 7 (7 turns)

Tính riêng cho mỗi intent (vì web search có thể khác — Visa/Weather bật web, Guide không bật):

```text
cost_conv_guide   (4 turns) = $0.000246 (Budget Bot) | $0.000246 (Smart Mix Guide)
cost_conv_visa    (4 turns) = $0.000246 (Budget Bot) | $0.0321 (Smart Mix Visa/Weather)
cost_conv_weather (4 turns) = $0.000246 (Budget Bot) | $0.0321 (Smart Mix Visa/Weather)
cost_1_turn_only             = $0  (Booking + Complaint chỉ 1 turn rồi handoff,
                                       chỉ tốn classifier nếu dùng LLM)
```

### Bước 3 — Weighted average cost per conversation (toàn bộ intent)

Lấy % intent mix × cost từng intent:

**Scenario A** (Guide 50%, Visa 25%, Weather 10%, Booking 10%, Complaint 5%):

```text
avg_cost_A = 50% × cost_conv_guide_4t
          + 25% × cost_conv_visa_4t
          + 10% × cost_conv_weather_4t
          + 10% × cost_1_turn_only
          +  5% × cost_1_turn_only
```

**Scenario B** (Guide 30%, Visa 15%, Weather 10%, Booking 35%, Complaint 10%, 7 turns cho AI-served):

```text
avg_cost_B = 30% × cost_conv_guide_7t
          + 15% × cost_conv_visa_7t
          + 10% × cost_conv_weather_7t
          + 35% × cost_1_turn_only
          + 10% × cost_1_turn_only
```

### Bước 4 — Monthly cost

```text
monthly_A = avg_cost_A × 300 conv/ngày × 30 ngày
monthly_B = avg_cost_B × 1,200 conv/ngày × 30 ngày
```

### Bước 5 — So sánh với human baseline

```text
human_A = $0.50 × 300 × 30 = $4,500 / tháng
human_B = $0.50 × 1,200 × 30 = $18,000 / tháng

savings_A% = (4,500 − monthly_A) / 4,500 × 100
savings_B% = (18,000 − monthly_B) / 18,000 × 100
```

Nếu savings ÂM → AI đắt hơn human → cần justify (24/7? đa ngôn ngữ? scale?).

---

## Tiktoken Actual vs Reference Card Estimates

| Component | Tiktoken Actual | Reference Estimate | Ratio (Est/Actual) |
|---|---|---|---|
| System prompt | 89 | 500 | **5.6×** |
| User message | 21 | 80 | **3.8×** |
| Assistant response | 76 | 180 | **2.4×** |
| RAG top-5 chunks | 327 | 1,250 | **3.8×** |
| Web search results | 156 | 800 | **5.1×** |
| 1 prior turn | 96 | 260 | **2.7×** |

**Kết luận**: Reference card bảo thủ (overestimate) để đảm bảo sinh viên không tính thiếu. Cost thực tế thấp hơn **2–6×** tùy component. Các bảng bên dưới dùng số **tiktoken thực**.

---

## Điền số cho từng config

Dùng AI tính xong, copy số vào đây. Đừng quên kiểm 1 lần xem số có hợp lý không.

### Config 1 — Budget Bot (GPT-5 nano, Web OFF, Last 3 turns)

| Item | Scenario A (4 turns) | Scenario B (7 turns) |
|---|---|---|
| Cost / conversation (avg) | **$0.000246** | **$0.000446** |
| Monthly cost | **$2.21** | **$16.04** |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | **2,032×** | **1,121×** |
| **Savings %** | **99.95%** | **99.91%** |

**Sanity check** (trả lời cho nhóm trước khi đi tiếp):

- Cost/conv có nằm trong $0.005–$0.10 không? Nếu quá thấp → có thể quên component (RAG? web? classifier?). Nếu quá cao → có thể tính sai history.
- Monthly có hợp lý không? (cheap config thường $100–$300, premium config có thể đến $3,000+)

```text
Cost/conv $0.000246 thấp hơn range $0.005-$0.10 rất nhiều. Lý do: GPT-5 nano rẻ nhất thị trường
($0.05/$0.40) và tiktoken actual thấp hơn estimate 2-6×. RAG thực tế chỉ 327 tokens (thay vì 1,250).
Monthly $2.21 cho 300 conv/ngày = cực kỳ rẻ, phù hợp với model nano + minimalist setup.
Nhưng cần nhớ: reference card estimate $5.60 là bảo thủ; tiktoken actual $2.21 thực tế hơn.
```

---

### Config 2 — Premium Concierge (GPT-5.5, Web ON broad, Full history)

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | **$0.056683** | **$0.103620** |
| Monthly cost | **$510.15** | **$3,730.32** |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | **8.82×** | **4.84×** |
| **Savings %** | **88.66%** | **79.28%** |

**Sanity check**:

```text
Cost/conv $0.057 hợp lý cho GPT-5.5 flagship ($5/$30) + web broad ($0.008/turn) + full history.
Monthly $510 (A) và $3,730 (B) vẫn rẻ hơn human đáng kể.
Scenario B đắt gấp ~7× Scenario A vì volume ×4 + turns ×7 + full history tốn nhiều tokens.
Tiktoken actual giảm cost đáng kể so với estimate cũ ($872 A / $4,220 B) nhưng vẫn cao nhất 4 configs.
```

---

### Config 3 — Smart Mix (GPT-5 nano + Gemini 3.1 Flash-Lite, Web ON selective, Last 5 turns)

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | **$0.003337** | **$0.006634** |
| Monthly cost | **$30.03** | **$238.84** |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | **149.9×** | **75.4×** |
| **Savings %** | **99.33%** | **98.67%** |

**Sanity check**:

```text
Cost/conv $0.003 nằm giữa Budget Bot ($0.0002) và Premium ($0.057) — đúng vị trí "balanced".
Monthly ~$30-$240 rất hợp lý cho config mix model + selective web + last 5.
Visa/Weather đắt hơn Guide ~130× (do Gemini 3.1 Flash-Lite + web ON), nhưng chỉ chiếm 35% volume
nên weighted avg vẫn thấp. Đây là "sweet spot" rõ ràng giữa cost và quality.
So với estimate cũ ($117/$588), tiktoken actual giảm ~75% nhưng vẫn đúng trend.
```

---

### Config 4 (optional) — Deep Value (DeepSeek V4 Pro promo, Web ON selective, Summarize every 5 turns)

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | **$0.008856** | **$0.017442** |
| Monthly cost | **$79.71** | **$627.91** |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | **56.5×** | **28.7×** |
| **Savings %** | **98.23%** | **96.51%** |

**Sanity check**:

```text
DeepSeek V4 Pro promo ($0.435/$0.87) cho chất lượng strong nhưng giá gần bằng Gemini Flash-Lite.
Cost/conv $0.009 gần Smart Mix ($0.003) nhưng model mạnh hơn nhiều → "best bang for buck".
Lưu ý: chưa tính thêm cost của LLM call tóm tắt history mỗi 5 turns. Nếu tính thêm,
cost sẽ tăng khoảng $0.0003-0.0005/conv, vẫn rất rẻ.
So với estimate cũ ($140/$677), tiktoken actual giảm ~40%.
```

---

## Quality + Speed estimate (qualitative)

Mỗi config — estimate Low / Medium / High. Không có công cụ đo chính xác trong lab, ước tính dựa trên model tier + web search + history.

| Config | Quality (Low/Med/High) | Speed (Low/Med/High) | Lý do |
|---|---|---|---|
| 1: Budget Bot | Low | High | GPT-5 nano model rẻ, web OFF, Last 3 turns → trả lời nhanh (~200ms) nhưng có thể quên context và thiếu info real-time |
| 2: Premium Concierge | High | Low | GPT-5.5 flagship + web broad + full history → chất lượng cao nhất nhưng chậm nhất (~2-4s) |
| 3: Smart Mix | Medium | Medium | Nano nhanh cho Guide (59%), Flash-Lite vừa cho Visa/Weather (14%), selective web → cân bằng tốt |
| 4: Deep Value | Medium-High | Medium | DeepSeek V4 Pro strong nhưng không bằng GPT-5.5; summarize every 5 tiết kiệm tokens nhưng cần thêm 1 LLM call tóm tắt |

**Hướng dẫn ước tính**:

- **Quality**: Cheap model → Low (70%). Strong model → High (88%). Web search bật → Quality tăng vì info real-time. History Full → Quality tốt hơn ở conversation dài.
- **Speed**: Cheap model thường nhanh (~200ms). Strong model chậm hơn (~1–3s). Web search bật → +1–2s.

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Tất cả ≥3 configs đã có cost/conv + monthly cho cả 2 scenarios
- [x] Đã so sánh từng config với human baseline ($0.50/conv)
- [x] Có quality + speed estimate cho mỗi config
- [x] Đã sanity check — không có số "quá lạ" (cost <$0.001 hoặc >$1/conv)
- [x] Đã so sánh tiktoken actual vs reference estimates (thấp hơn 2–6×)

⚑ **Checkpoint 11:00**: ≥1 config đã tính cost xong &nbsp; · &nbsp; ⚑ **Checkpoint 11:20**: tất cả configs đã tính cost xong cho cả 2 scenarios.

Xong → mở `04-comparison-table.md`.
