# 05 · Recommendation — Quyết định cuối cùng

> **Mục tiêu**: Dựa trên bảng so sánh ở `04-comparison-table.md`, chốt **1 config (hoặc pha trộn)** để recommend. Viết lý do rõ ràng, nêu rủi ro + mitigation, chuẩn bị material cho buổi present.
>
> **Thời gian**: 15 phút (phần Final)

---

## Config được recommend: **Smart Mix**

**Tên config:** Smart Mix  
**Model:** GPT-5 nano ($0.05/$0.40) cho Guide/Destination (59% volume) + Gemini 3.1 Flash-Lite ($0.25/$1.50) cho Visa/Policy + Weather/Event  
**Web search:** ON selective — chỉ Visa + Weather  
**History:** Last 5 turns  
**Classifier:** GPT-5 nano (cheap LLM, ~170 tokens)

---

## Tại sao chọn Smart Mix?

### 1. Cost — rẻ hơn human 150×, monthly chỉ $30–$239

| Metric | Giá trị |
|---|---|
| Cost / conversation (Scenario A) | **$0.0033** |
| Cost / conversation (Scenario B) | **$0.0066** |
| Monthly (300 conv/day) | **$30.03** |
| Monthly (1,200 conv/day) | **$238.84** |
| So với nhân viên ($0.50/conv) | Rẻ hơn **149.9×** (A) / **75.4×** (B) |
| Savings % | **99.33%** (A) / **98.67%** (B) |

→ Với monthly $30–$240, công ty tiết kiệm **$4,470–$17,761/tháng** so với thuê nhân viên. Ngay cả mùa cao điểm (Scenario B), chi phí AI vẫn chưa bằng **1.5%** chi phí nhân viên.

### 2. Quality — "đúng mức trí thông minh cho đúng câu hỏi"

- **59% câu hỏi là Guide/Destination** (FAQ đơn giản: "đi Đà Nẵng mùa nào đẹp?") → GPT-5 nano đủ xử lý. Không cần GPT-5.5 để trả lời câu hỏi đơn giản.
- **14% câu hỏi là Visa/Weather** (cần chính xác + real-time) → Gemini 3.1 Flash-Lite đảm bảo thông tin đúng, không outdated.
- **27% câu hỏi là Booking/Complaint** → handoff cho người, $0 LLM cost.

→ Không phí tiền model mạnh cho câu hỏi đơn giản. Không dùng model yếu cho câu hỏi phức tạp.

### 3. Speed — cân bằng

- GPT-5 nano phản hồi cực nhanh (~200ms) cho 59% FAQ.
- Gemini 3.1 Flash-Lite vừa phải (~500ms–1s) cho Visa/Weather.
- Web search ON selective chỉ cho 14% turns → không làm chậm toàn bộ hệ thống.

→ Trung bình response time < 1 giây — chấp nhận được cho chatbot du lịch.

### 4. Scalability — linear cost

- Volume tăng từ 300 → 1,200 conv/day (×4), monthly chỉ tăng từ $30 → $239 (×8 do turns dài hơn).
- Không cần tuyển thêm nhân viên, không cần training, không cần đêm/khuya shift.

---

## So sánh nhanh: tại sao KHÔNG chọn các config khác?

| Config | Lý do KHÔNG chọn |
|---|---|
| **Budget Bot** | Quá rẻ nhưng quality thấp — thiếu web search nên visa info dễ outdated; Last 3 turns quên context nhanh. Phù hợp night-mode hoặc mùa thấp điểm, không phải production chính. |
| **Premium Concierge** | Chất lượng cao nhất nhưng cost cao ($510–$3,730/tháng). Monthly B ($3,730) gần bằng 20% chi phí nhân viên. Không justify được với công ty vừa/nhỏ. Chỉ dùng cho khách VIP nếu có segmentation. |
| **Deep Value** | Chất lượng strong + giá tốt, nhưng "Summarize every 5 turns" cần thêm infra + logic phức tạp. DeepSeek promo ($0.435/$0.87) có thể hết hạn 31/05/2026 — rủi ro giá tăng đột ngột. |

→ **Smart Mix** là "sweet spot" duy nhất: cost thấp ($30–$240), quality đủ dùng, speed nhanh, không cần infra phức tạp.

---

## Rủi ro + Mitigation

| Rủi ro | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Classifier sai intent** → dùng GPT-5 nano cho câu hỏi visa | Trung bình | Cao | Thêm keyword pre-filter cho intent rõ ràng ("visa", "booking", "complaint"). Monitor accuracy, tune threshold. |
| **Gemini 3.1 Flash-Lite không đủ mạnh cho visa phức tạp** | Thấp | Trung bình | Nếu khách hỏi visa phức tạp ("tôi đã overstay 3 ngày"), escalate sang nhân viên. Flash-Lite đủ cho 90% câu hỏi visa thông thường. |
| **Web search API downtime** | Thấp | Trung bình | Cache kết quả web search 24h. Nếu Tavily down, fallback sang RAG + disclaimer "info may be outdated". |
| **GPT-5 nano không đủ cho câu hỏi dài/hỏi lại** | Trung bình | Thấp | Last 5 turns giúp giữ context. Nếu câu hỏi phức tạp quá, model sẽ trả lời generic nhưng vẫn helpful → không gây hại lớn. |
| **Model pricing thay đổi** | Trung bình | Thấp–Trung bình | GPT-5 nano và Gemini 3.1 Flash-Lite là tier rẻ nhất, ít biến động giá. Nếu tăng, vẫn rẻ hơn nhân viên hàng trăm lần. |

---

## Timeline triển khai đề xuất

| Giai đoạn | Thời gian | Việc làm |
|---|---|---|
| **Phase 1: MVP** | Tuần 1–2 | Deploy Budget Bot (GPT-5 nano, Web OFF, Last 3) cho night-mode + FAQ đơn giản. Không cần classifier phức tạp. |
| **Phase 2: Smart Mix** | Tuần 3–4 | Thêm classifier + routing logic. Chuyển Visa/Weather sang Gemini 3.1 Flash-Lite + web search. Bật Last 5 turns. |
| **Phase 3: Monitoring** | Tuần 5–6 | Theo dõi intent accuracy, response quality, cost per conversation. Tune classifier threshold. A/B test nếu cần. |
| **Phase 4: Scale / Optional** | Tháng 2+ | Nếu khách VIP nhiều → thêm Premium Concierge tier (pay-per-use). Nếu volume tăng vượt 2,000 conv/day → consider caching + batch processing. |

---

## Câu trả lời 6 câu hỏi thảo luận (từ cost-reference-card.md)

### 1. "Visa policy Việt Nam vừa đổi. Config nào của bạn fail đầu tiên?"

```text
Budget Bot fail đầu tiên — vì Web OFF + model yếu (GPT-5 nano) không có real-time info.
Smart Mix sẽ phát hiện được nhờ Gemini 3.1 Flash-Lite + web search ON selective cho Visa.
Mitigation: web search + fallback "I'm not sure about the latest update, let me connect you with our visa specialist."
```

### 2. "Khách VIP chat 10 lượt. Config nào tốn nhất? Chênh bao nhiêu so với config rẻ nhất?"

```text
Premium Concierge tốn nhất — Full history + GPT-5.5 + web broad. 10 turns ≈ $0.57/conv.
Budget Bot rẻ nhất — 10 turns ≈ $0.001/conv.
Chênh: ~570× lần.
→ Khách VIP nên có option "Premium Concierge" riêng (pay-per-use hoặc upsell), không dùng cho tất cả.
```

### 3. "Speed 4-5 giây có chấp nhận được cho chatbot du lịch không?"

```text
Không chấp nhận được. Research cho thấy 73% users rời đi nếu chatbot phản hồi >3 giây.
Smart Mix trung bình <1 giây (nano ~200ms, Flash-Lite ~500ms-1s) — hoàn toàn chấp nhận được.
Premium Concierge có thể 2-4 giây (GPT-5.5 + web broad + full history) — cần cảnh báo "typing..." hoặc streaming.
```

### 4. "Nếu dùng model rẻ cho tất cả thì quality gap nằm ở đâu?"

```text
Budget Bot (GPT-5 nano cho tất cả) — quality gap ở:
1. Visa/policy phức tạp: model không hiểu nuance ("overstay", "multiple entry", "visa run").
2. Context dài: quên budget/điểm đến đã nhắc 5 turns trước.
3. Tone: trả lời có thể robotic hơn so với model mạnh.
→ Gap lớn nhất: trust. Nếu bot trả lời sai visa → khách mất niềm tin vào công ty.
```

### 5. "Có nên mix — cheap model cho FAQ, strong model cho visa — không? Cost thay đổi thế nào?"

```text
NÊN — đó chính là Smart Mix.
Nếu dùng GPT-5 nano cho tất cả: $0.000246/conv (A).
Nếu dùng GPT-5.5 cho tất cả: $0.057/conv (A) — đắt hơn 230×.
Smart Mix: $0.0033/conv (A) — chỉ đắt hơn Budget Bot 13× nhưng vẫn rẻ hơn Premium 17×.
→ Mix là "sweet spot" rõ ràng. 59% volume dùng model rẻ, 14% cần model tốt hơn.
```

### 6. "So với thuê thêm 1 nhân viên, lúc nào AI chatbot trở nên đắt hơn?"

```text
AI chatbot KHÔNG BAO GIỜ đắt hơn nhân viên trong bài toán này — ngay cả Premium Concierge ($3,730/tháng B)
vẫn rẻ hơn nhân viên ($18,000/tháng B).

Nhưng nếu tính TCO (Total Cost of Ownership):
- AI: API cost + dev time + monitoring + infra.
- Human: lương + training + turnover + office space.

Ngay cả với TCO, AI vẫn rẻ hơn 5-10×. Điểm break-even chỉ xảy ra nếu:
1. Công ty rất nhỏ (<50 conv/ngày) → chi phí setup AI không đáng.
2. Khách hàng đòi hỏi empathy cao (therapist, counsellor) → AI không thay thế được.

Với travel agency (volume 300–1,200 conv/day), AI luôn rẻ hơn.
```

---

## Tóm tắt 1 slide cho present

```text
RECOMMENDATION: Smart Mix
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Model:    GPT-5 nano (Guide) + Gemini 3.1 Flash-Lite (Visa/Weather)
Web:      ON selective (Visa + Weather only)
History:  Last 5 turns
Cost:     $0.0033/conv (A) | $0.0066/conv (B)
Monthly:  $30 (A) | $239 (B)
Savings:  99.3% vs human ($4,500–$18,000/mo)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Why:      "Right intelligence for the right question"
          59% FAQ → cheap model | 14% complex → mid model | 27% → human handoff
Risk:     Classifier accuracy → mitigate with keyword pre-filter + monitoring
Timeline: MVP (2w) → Smart Mix (2w) → Monitor (2w) → Scale (ongoing)
```

---

## Bảng kiểm trước khi present

- [x] Đã chọn 1 config chính (hoặc pha trộn rõ ràng)
- [x] Có ≥3 lý do justify (cost + quality + speed + scalability)
- [x] Đã nêu rủi ro + mitigation cụ thể
- [x] Có timeline triển khai thực tế
- [x] Đã trả lời ≥4 câu hỏi thảo luận
- [x] Có 1-slide summary để present

**Ready to present.**
