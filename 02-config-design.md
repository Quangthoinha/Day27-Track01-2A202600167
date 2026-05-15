# 02 · Configuration Design - Đặt tên + Chốt knobs cho ≥3 Configs

> **Mục tiêu**: Biến phác thảo ở `01-base-flow.md` thành ≥3 configurations chi tiết, mỗi config có tên + 3 knobs đã chốt + lý do chọn.
>
> **Thời gian**: 15 phút (đầu phần Main, trước khi tính cost)

---
## Config 1

**Tên config**: "Budget Bot"

### 3 Knobs

**① Model tier**:

```text
Response model: Gemini Flash-Lite → giá $0.10 / $0.40 per 1M tokens
Classifier model: Keyword matching → giá $0 (miễn phí)
```

**② Web search**:

```text
☑ OFF
□ ON selective - bật cho intent: ___
□ ON broad
```

**③ History management**:

```text
☑ Last 3 turns
□ Last 5
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

- Config này phục vụ tình huống nào tốt nhất? (mùa thấp điểm? night-time? volume cao đột biến?)
- Trade-off chính là gì? (Rẻ nhưng kém chất lượng? Đắt nhưng chính xác?)
- Khách hàng nào sẽ hài lòng nhất với config này? Khách nào sẽ thất vọng?

```text
1. Phục vụ mùa thấp điểm (low season) khi volume thấp - cần minimize cost mà vẫn handle được tourist hỏi thông tin cơ bản.
2. Với Guide chiếm 59% câu hỏi (điểm đến phổ biến), RAG knowledge base đủ đáp ứng mà không cần web search.
3. Tourist hỏi nhanh, đơn giản - Last 3 turns đủ context cho câu hỏi ngắn.
```

### Rủi ro lớn nhất của config này

```text
Visa info có thể outdated nếu không có web search - nếu visa policy đổi, bot sẽ trả lời sai thông tin, gây mất uy tín với khách.
```

---

## Config 2

**Tên config**: "Smart Router"

### 3 Knobs

**① Model tier**:

```text
Response model: 
  - Gemini Flash-Lite cho Guide (59% intents) → giá $0.10 / $0.40
  - DeepSeek V4 Pro cho Visa/Weather (14% intents) → giá $1.74 / $3.48
  - Claude Sonnet 4.6 cho Complaint (5% intents) → giá $3.00 / $15.00
Classifier model: Keyword matching → giá $0
```

**② Web search**:

```text
□ OFF
☑ ON selective - bật cho intent: Visa/Policy, Weather/Event
□ ON broad
```

**③ History management**:

```text
□ Last 3 turns
☑ Last 5 turns
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
1. Phục vụ daily operation - cân bằng giữa cost và quality. Guide chiếm 59% → dùng cheap model cho phần lớn queries để tiết kiệm.
2. Visa/Weather cần accuracy cao vì thông tin thay đổi thường xuyên → dùng strong model + web search để đảm bảo thông tin mới nhất.
3. Complaint chiếm 5% nhưng ảnh hưởng brand lớn → cần Claude Sonnet để respond cẩn thận, tránh escalte.
```

### Rủi ro lớn nhất của config này

```text
Routing phức tạp hơn - cần maintain multiple model endpoints + logic routing, có thể tăng operational overhead.
```

---

## Config 3

**Tên config**: "Premium Concierge"

### 3 Knobs

**① Model tier**:

```text
Response model: Claude Sonnet 4.6 → giá $3.00 / $15.00 per 1M tokens
Classifier model: Claude Haiku 4.5 (dedicated) → giá $1.00 / $5.00 per 1M tokens
```

**② Web search**:

```text
□ OFF
□ ON selective - bật cho intent: Visa/Policy, Weather/Event
☑ ON broad (bật cho hầu hết intents)
```

**③ History management**:

```text
□ Last 3 turns
□ Last 5 turns
☑ Full history (nhớ tất cả)
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
1. Phục vụ khách VIP / high-value bookings - những khách chi nhiều tiền cho luxury tours, cần trải nghiệm seamless và personal.
2. Full history đảm bảo context không bị mất - khách VIP thường chat dài (7-10 turns), nhớ toàn bộ conversation tạo cảm giác được quan tâm.
3. Web search broad + Claude Sonnet cho chất lượng cao nhất - không có tradeoff về accuracy, trả lời luôn đầy đủ và chi tiết.
```

### Rủi ro lớn nhất của config này

```text
Cost cao nhất trong 3 configs - có thể không hợp lý cho volume cao (100+ conversations/day) vì chi phí sẽ vượt ngân sách marketing.
```

---

## Config 4 (optional - nếu thời gian dư)

**Tên config**: "Value Leader"

### 3 Knobs

```text
Model: DeepSeek V4 Pro cho tất cả intents → giá $1.74 / $3.48 per 1M tokens
Web: ON selective (Visa + Weather)
History: Last 5 turns
```

### Lý do

```text
DeepSeek V4 Pro nằm ở sweet spot giữa cost và quality - rẻ hơn Claude Sonnet ~4x nhưng vẫn mạnh hơn Gemini Flash-Lite.
Phù hợp cho agencies muốn quality tốt mà không tốn chi phí premium.
```

---

## Bảng kiểm trước khi tính cost

- [x] ≥3 configs đã đặt tên (Budget Bot, Smart Router, Premium Concierge, Value Leader)
- [x] Mỗi config đã chốt rõ 3 knobs (không còn ô trống)
- [x] Mỗi config có ≥2 câu lý do
- [x] 3 configs đủ khác biệt - không phải chỉ đổi mỗi 1 knob nhỏ
- [x] Nhóm đồng thuận đây là 3 configs đáng so sánh

**So sánh nhanh 3 configs:**

| Knob | Budget Bot | Smart Router | Premium Concierge |
|------|------------|--------------|------------------|
| Model | Gemini Flash-Lite | Mix (3 models) | Claude Sonnet |
| Web | OFF | Selective (Visa/Weather) | Broad |
| History | Last 3 | Last 5 | Full |

**Nếu 3 configs quá giống nhau** (chỉ đổi model, knobs khác giống hệt) → quay lại tweak. Mục đích là thấy tradeoff - configs giống nhau quá → không thấy tradeoff.

Xong → mở `03-cost-calculation.md` để bắt đầu tính cost.
