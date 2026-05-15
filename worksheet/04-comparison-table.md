# 04 · Comparison Table — Bảng so sánh đầy đủ

> **Mục tiêu**: Tổng hợp tất cả số đã tính ở `03-cost-calculation.md` thành 1 bảng so sánh duy nhất — đây là artifact chính nhóm sẽ present.
>
> **Thời gian**: 10 phút (đầu phần Final)

---

## Vì sao có bảng so sánh?

Khi sếp hỏi "Nên deploy config nào?", bạn cần đặt lên bàn **1 bảng** thay vì đọc 3 báo cáo riêng. Bảng so sánh đầy đủ cho phép so sánh thẳng từng dòng, dễ nhìn ra tradeoff.

---

## Bảng chính

Điền số đã tính (dùng **tiktoken actual** từ `03-cost-calculation.md`).

| | Config 1 | Config 2 | Config 3 | Config 4 |
|---|---|---|---|---|
| **Tên** | Budget Bot | Premium Concierge | Smart Mix | Deep Value |
| **① Model** | GPT-5 nano ($0.05/$0.40) | GPT-5.5 ($5.00/$30.00) | GPT-5 nano + Gemini 3.1 Flash-Lite | DeepSeek V4 Pro promo ($0.435/$0.87) |
| **② Web search** | OFF | ON broad | ON selective (Visa + Weather) | ON selective (Visa + Weather) |
| **③ History** | Last 3 turns | Full history | Last 5 turns | Summarize every 5 turns |
| **Intent classifier** | GPT-5 nano | GPT-5.5 | GPT-5 nano | DeepSeek V4 Flash |
| **Cost / conv (Scenario A — 4 turns)** | **$0.000246** | **$0.056683** | **$0.003337** | **$0.008856** |
| **Cost / conv (Scenario B — 7 turns)** | **$0.000446** | **$0.103620** | **$0.006634** | **$0.017442** |
| **Monthly A** (300 conv/day × 30) | **$2.21** | **$510.15** | **$30.03** | **$79.71** |
| **Monthly B** (1,200 conv/day × 30) | **$16.04** | **$3,730.32** | **$238.84** | **$627.91** |
| **vs human $4,500/mo (A)** | rẻ **2,032×** | rẻ **8.82×** | rẻ **149.9×** | rẻ **56.5×** |
| **vs human $18,000/mo (B)** | rẻ **1,121×** | rẻ **4.84×** | rẻ **75.4×** | rẻ **28.7×** |
| **Savings % (A)** | **99.95%** | **88.66%** | **99.33%** | **98.23%** |
| **Savings % (B)** | **99.91%** | **79.28%** | **98.67%** | **96.51%** |
| **Quality estimate** | Low | High | Medium | Medium-High |
| **Speed estimate** | High | Low | Medium | Medium |
| **Điểm yếu chính** | Thiếu real-time info, quên context sớm | Cost cao khi volume lớn, chậm | Complex routing cần classifier chính xác | Cần thêm infra tóm tắt history, promo có thể hết hạn |
| **Best for** (khi nào nên dùng) | Night mode, mùa thấp điểm, FAQ đơn giản | Khách VIP, honeymoon, câu hỏi phức tạp | Mùa cao điểm volume lớn, cần cân bằng cost/quality | Doanh nghiệp muốn chất lượng strong mà budget bị siết |

---

## Quan sát nhanh từ bảng

Trước khi sang file recommendation, trả lời 4 câu — đây là material để present:

### Câu 1 — Config rẻ nhất là gì? Đắt nhất là gì?

```text
Rẻ nhất: Budget Bot (GPT-5 nano, Web OFF, Last 3) — monthly B = $16.04
Đắt nhất: Premium Concierge (GPT-5.5, Web ON broad, Full history) — monthly B = $3,730.32
Chênh: 233× lần
```

### Câu 2 — Knob nào ảnh hưởng cost nhiều nhất?

So sánh các config khác nhau ở knob nào, chênh bao nhiêu. Thường: model tier > history > web search.

```text
Model tier ảnh hưởng cost NHIỀU NHẤT.
- Đổi từ GPT-5 nano → GPT-5.5 tăng cost ~230× (Budget Bot vs Premium).
- DeepSeek V4 Pro promo cùng tier "strong" nhưng rẻ hơn GPT-5.5 ~34×.

History Full vs Last 3 chênh khoảng 15-20% ở Budget Bot (vì model rẻ),
nhưng chênh 40%+ ở Premium Concierge (vì GPT-5.5 input/output đắt,
full history tăng tokens input đáng kể mỗi turn).

Web search bật/tắt chênh ~$0.008/query + token cost (nhỏ so với model cost).
Ở GPT-5.5, 800 tokens web search = $0.004 extra input → gần như không đáng kể.
Ở GPT-5 nano, 800 tokens web search = $0.00004 → không đáng kể.
Vậy web search là knob ảnh hưởng YẾU NHẤT đến cost tổng.
```

### Câu 3 — Tại sao Scenario B không đắt ×4 lần Scenario A?

Volume Scenario B = ×4 lần Scenario A. Turns dài hơn (7 vs 4 = ×1.75). Mong đợi monthly B ≈ A × 7. Thực tế có thể thấp hơn vì sao?

Trước khi viết, nghĩ: intent mix Scenario B có gì khác? Booking + Complaint = $0 LLM ở scenario B là bao nhiêu %?

```text
Scenario B có AI-served ratio chỉ 55% (vs 85% ở A) → 45% conversations là Booking/Complaint
= handoff $0 LLM cost. Intent mix B: Guide 30%, Visa 15%, Weather 10%, Booking 35%, Complaint 10%.
→ 45% volume KHÔNG tốn LLM tokens (chỉ tốn classifier). Đây là lý do chính monthly B không phải 7× A.

Ngoài ra, Scenario B intent mix giảm Guide (cheapest, 59% → 30%) và tăng Booking (handoff, 23% → 35%).
Weighted avg cost/conv B thấp hơn so với nếu giữ cùng intent mix A.
```

### Câu  4 — Có config nào AI đắt hơn human không?

So sánh monthly từng config với human baseline ($4,500 cho A, $18,000 cho B). Nếu AI rẻ hơn → savings %. Nếu đắt hơn → cần justify.

```text
KHÔNG có config nào đắt hơn human baseline.

Thậm chí Premium Concierge (đắt nhất) vẫn rẻ hơn human:
- Scenario A: $510 vs $4,500 → tiết kiệm 88.66%
- Scenario B: $3,730 vs $18,000 → tiết kiệm 79.28%

Budget Bot rẻ hơn human tới 2,000× — gần như miễn phí.
Smart Mix rẻ hơn human 150× (A) / 75× (B) — "sweet spot" rõ ràng.

→ AI chatbot luôn rẻ hơn nhân viên trong bài toán này, ngay cả với config premium nhất.
Lợi ích ngoài cost: hoạt động 24/7, đa ngôn ngữ, scale tuyến tính, consistency 100%.
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Bảng đầy đủ — không còn ô trống
- [x] Đã có 4 câu trả lời cho 4 quan sát ở trên
- [x] Nhóm đồng thuận về số trong bảng (đã sanity check)

Xong → mở `05-recommendation.md` để viết recommendation cuối + chuẩn bị present.
