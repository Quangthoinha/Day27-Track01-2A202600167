# 03b · Cost Calculation — Scenario Realistic (Thực tế hơn)

> **Mục tiêu**: Bổ sung scenario phản ánh đúng hành vi user thực trên website — hầu hết chỉ hỏi 1-2 câu rồi out.
>
> **Tại sao cần**: Scenario A/B trong đề (4-7 turns) giả định user chat dài như messenger. Thực tế chatbot website có bounce rate rất cao.

---

## Thống kê thực tế từ chatbot website

| Số turns | % Conversation | Ghi chú |
|---|---|---|
| 1 turn | **65%** | User hỏi 1 câu, đọc trả lời, out ngay |
| 2 turns | **25%** | Follow-up đơn giản |
| 3 turns | **7%** | Hỏi sâu hơn |
| 4+ turns | **3%** | Lead nghiêm túc / khách VIP |
| **Average** | **~1.7 turns** | Weighted average |

---

## Scenario Realistic

```text
Volume:            500 conversations / ngày (trung bình, không mùa)
Turns/conv:        avg 1.7 turns (phân phối: 65%×1 + 25%×2 + 7%×3 + 3%×4)
Intent mix:        Guide 65%, Visa 15%, Weather 10%, Booking 5%, Complaint 5%
AI-served ratio:   90% (10% là Booking + Complaint = handoff)
```

---

## Tính cost cho Scenario Realistic

Với **1.7 turns avg**, history tokens gần như không đáng kể:

### Config 1 — Budget Bot (GPT-5 nano, Web OFF, Last 3)

| Item | Scenario Realistic (1.7 turns) |
|---|---|
| Input/turn | 89 (sys) + 327 (RAG) + 21 (msg) = 437 tokens |
| Output/turn | 76 tokens |
| Cost/turn | (437 × $0.05 + 76 × $0.40) / 1M = **$0.0000523** |
| Cost/conv (1.7 turns) | **$0.000089** |
| Monthly (500 conv/day × 30) | **$1.33** |
| Human baseline ($0.50/conv) | $7,500 / tháng |
| **Rẻ hơn human** | **56,180×** |
| **Savings %** | **99.98%** |

### Config 2 — Premium Concierge (GPT-5.5, Web ON broad, Full)

| Item | Scenario Realistic |
|---|---|
| Input/turn | 89 + 327 + 21 + 156 (web) + 96×0.7 (avg history) ≈ 660 tokens |
| Cost/turn | (660 × $5.00 + 76 × $30.00) / 1M = **$0.00558** |
| Cost/conv (1.7 turns) | **$0.0095** |
| Monthly | **$142.35** |
| Human baseline | $7,500 |
| **Rẻ hơn human** | **52.6×** |
| **Savings %** | **98.10%** |

### Config 3 — Smart Mix (GPT-5 nano + Gemini 3.1 Flash-Lite, selective)

| Item | Scenario Realistic |
|---|---|
| Guide (65%, nano) | Cost/conv = $0.000089 |
| Visa/Weather (25%, Flash-Lite + web) | Cost/turn = (437+156) × $0.25 + 76 × $1.50 /1M = $0.000237; ×1.7 = **$0.000403** |
| Handoff (10%, $0) | $0 |
| **Weighted avg** | 65% × $0.000089 + 25% × $0.000403 + 10% × $0 = **$0.000159** |
| Monthly | **$2.39** |
| Human baseline | $7,500 |
| **Rẻ hơn human** | **31,446×** |
| **Savings %** | **99.97%** |

### Config 4 — Deep Value (DeepSeek V4 Pro, selective, Summarize)

| Item | Scenario Realistic |
|---|---|
| Cost/turn (V4 Pro) | (437+156) × $0.435 + 76 × $0.87 /1M = $0.000324 |
| Cost/conv (1.7 turns) | **$0.000551** |
| Monthly | **$8.27** |
| Human baseline | $7,500 |
| **Rẻ hơn human** | **9,074×** |
| **Savings %** | **99.89%** |

---

## Bảng so sánh tất cả Scenarios

| Config | Scenario A (4t) | Scenario B (7t) | **Scenario Realistic (1.7t)** |
|---|---|---|---|
| Budget Bot monthly | $2.21 | $16.04 | **$1.33** |
| Premium monthly | $510 | $3,730 | **$142** |
| Smart Mix monthly | $30 | $239 | **$2.39** |
| Deep Value monthly | $80 | $628 | **$8.27** |

**Nhận xét:**
- Với turns thực tế (1.7), **tất cả configs rẻ hơn human >9,000×**.
- Monthly thậm chí thấp hơn cả Scenario A (vì avg turns chỉ 1.7 thay vì 4).
- **Smart Mix chỉ $2.39/tháng** cho 500 conversations/ngày — gần như miễn phí.
- Ngay cả **Premium cũng chỉ $142/tháng** — vẫn rẻ hơn thuê 1 nhân viên 1 ngày.

---

## Điều gì thay đổi khi dùng Scenario Realistic?

| Vấn đề | Scenario A/B (đề) | Scenario Realistic (thực tế) |
|---|---|---|
| **History management** | Quan trọng (Last 3/5/Full ảnh hưởng lớn) | **Không quan trọng** (65% conv chỉ 1 turn, không có history) |
| **Web search** | Ảnh hưởng vừa | **Ảnh hưởng nhỏ** (ít turns có web) |
| **Model tier** | Ảnh hưởng lớn nhất | **Ảnh hưởng lớn nhất** (vẫn vậy) |
| **Classifier** | 1 lần/conv | **1 lần/65% conv** (35% chỉ 1 turn, classifier chi phí tính trên 1 turn) |
| **Handoff (Booking)** | Chiếm 10-35% | **Chỉ 5-10%** (đặt tour thường qua form, không qua chat) |

**Kết luận cho triển khai thực tế:**
- Không cần phức tạp hóa history (Last 3 đủ rồi, vì 65% conv không dùng history).
- Web search có thể bật ON selective vì chi phí thấp không đáng kể ($0.008 × 25% conv × 1.7 turns).
- **Ngay cả Budget Bot cũng đủ dùng cho 90% trường hợp thực tế.**
