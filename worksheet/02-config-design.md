# 02 · Configuration Design — Đặt tên + Chốt knobs cho ≥3 Configs

> **Mục tiêu**: Biến phác thảo ở `01-base-flow.md` thành ≥3 configurations chi tiết, mỗi config có tên + 3 knobs đã chốt + lý do chọn.
>
> **Thời gian**: 15 phút (đầu phần Main, trước khi tính cost)

---

## Tại sao đặt tên + viết lý do?

Khi present, nhóm sẽ nói "Config 1, Config 2, Config 3" → người nghe sẽ chán ngay. Đặt tên gợi mở (Budget Bot, Premium Concierge, Smart Mix...) giúp memorable + cho thấy nhóm hiểu rõ tradeoff. Viết lý do giúp nhóm tự kiểm tra: "Mình chọn config này vì lý do gì? Có justify được không?"

---

## Cách điền

Với mỗi config: đặt tên + chốt 3 knobs + viết 2–3 câu lý do chọn. Mỗi câu lý do phải gắn với 1 tình huống thực tế (volume thấp / khách hỏi visa nhiều / budget bị siết...).

Tham khảo bảng pricing chi tiết tại `cost-reference-card.md` mục **3. Decision Points**.

---

## Config 1

**Tên config** (gợi mở: "Budget Bot", "Bare Minimum", "Lean Mode", "Night Mode" — đặt tên có cá tính):

```text
Budget Bot
```

### 3 Knobs

**① Model tier**:

```text
Response model: GPT-5 nano → giá $0.05 / $0.40 per 1M tokens (input/output)
Classifier model: GPT-5 nano → giá $0.05 / $0.40 per 1M tokens (hoặc keyword = $0)
```

**② Web search**:

```text
☑ OFF
□ ON selective — bật cho intent: __________________
□ ON broad
```

**③ History management**:

```text
☑ Last 3
□ Last 5
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

Trước khi viết, tự hỏi:

- Config này phục vụ tình huống nào tốt nhất? (mùa thấp điểm? night-time? volume cao đột biến?)
- Trade-off chính là gì? (Rẻ nhưng kém chất lượng? Đắt nhưng chính xác?)
- Khách hàng nào sẽ hài lòng nhất với config này? Khách nào sẽ thất vọng?

```text
1. Phục vụ tốt nhất cho mùa thấp điểm (300 conv/ngày) hoặc night-time khi không có nhân viên —
   GPT-5 nano rẻ nhất thị trường ($0.05/$0.40), giảm cost tối đa.
2. 59% câu hỏi là Guide/Destination (FAQ đơn giản) — không cần model mạnh, GPT-5 nano đủ xử lý.
3. Khách hỏi đơn giản ("đi Đà Nẵng mùa nào đẹp") sẽ hài lòng vì trả lời nhanh.
   Khách hỏi phức tạp về visa policy mới nhất sẽ thất vọng vì không có web search + model yếu.
```

### Rủi ro lớn nhất của config này

```text
Visa info có thể outdated nếu web OFF và model không đủ mạnh để phát hiện contradiction trong KB.
Khách quên context khi history Last 3 — nếu tourist nhắc budget ở turn 1 rồi turn 5 hỏi lại, bot sẽ không nhớ.
```

---

## Config 2

**Tên config**:

```text
Premium Concierge
```

### 3 Knobs

**① Model tier**:

```text
Response model: GPT-5.5 → giá $5.00 / $30.00 per 1M tokens (input/output)
Classifier model: GPT-5.5 → giá $5.00 / $30.00 per 1M tokens (hoặc keyword = $0)
```

**② Web search**:

```text
□ OFF
□ ON selective — bật cho intent: __________________
☑ ON broad
```

**③ History management**:

```text
□ Last 3
□ Last 5
☑ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
1. Phục vụ khách VIP, honeymoon, hoặc khách có câu hỏi phức tạp (itinerary 7 ngày, so sánh điểm đến) —
   GPT-5.5 là flagship mới nhất, chất lượng cao nhất, đáp ứng kỳ vọng cao.
2. Web search ON broad đảm bảo mọi thông tin đều real-time — visa policy vừa đổi, weather forecast chính xác,
   khách không bao giờ nhận câu trả lời "có thể đã lỗi thời".
3. Full history giữ toàn bộ context conversation — khách không cần nhắc lại budget, số người, ngày đi.
   Trade-off: cost cao gấp ~100× so với Budget Bot, nhưng vẫn rẻ hơn nhân viên ($0.50/conv) nếu tính đúng.
```

### Rủi ro lớn nhất của config này

```text
Cost spike nếu volume tăng đột biến — Scenario B (1,200 conv/ngày, 7 turns) với full history + GPT-5.5
+ web search broad có thể đắt hơn nhân viên. Cần giám sát monthly cost chặt chẽ.
```

---

## Config 3

**Tên config**:

```text
Smart Mix
```

### 3 Knobs

**① Model tier**:

```text
Response model: Mix — GPT-5 nano ($0.05/$0.40) cho Guide/Destination (59% volume),
                     Gemini 3.1 Flash-Lite ($0.25/$1.50) cho Visa/Policy + Weather/Event
Classifier model: GPT-5 nano → giá $0.05 / $0.40 per 1M tokens (hoặc keyword = $0)
```

**② Web search**:

```text
□ OFF
☑ ON selective — bật cho intent: Visa/Policy + Weather/Event
□ ON broad
```

**③ History management**:

```text
□ Last 3
☑ Last 5
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
1. Đây là "sweet spot" giữa cost và quality — dùng đúng mức "trí thông minh" cho đúng loại câu hỏi.
   GPT-5 nano xử lý 59% FAQ đơn giản ở giá rẻ nhất; Gemini 3.1 Flash-Lite xử lý 14% Visa/Weather
   với chất lượng mid-tier ở giá vẫn rẻ (rẻ hơn Sonnet 4.6 ~12×).
2. Web search ON selective tiết kiệm — chỉ bật khi cần real-time (visa đổi, weather),
   không bật cho Guide (KB đủ) → tránh lãng phí $0.008/query + 800 tokens không cần thiết.
3. Last 5 turns đủ nhớ context cho hầu hết conversation (Scenario A avg 4 turns; Scenario B 7 turns
   thì vẫn nhớ được 5/7 lượt) mà không đắt như Full history.
```

### Rủi ro lớn nhất của config này

```text
Complexity tăng — cần routing logic để chọn model đúng theo intent. Nếu classifier sai (phân loại Visa thành Guide),
sẽ dùng GPT-5 nano yếu cho câu hỏi phức tạp → trả lời sai hoặc không đủ chính xác.
```

---

## Config 4 (optional — nếu thời gian dư)

Nhóm có thể thiết kế thêm config thứ 4 để có thêm điểm so sánh. Không bắt buộc.

**Tên config**:

```text
Deep Value
```

### 3 Knobs

```text
Response model: DeepSeek V4 Pro (promo) → giá $0.435 / $0.87 per 1M tokens
Classifier model: DeepSeek V4 Flash → giá $0.14 / $0.28 per 1M tokens (hoặc keyword = $0)
Web: ON selective — bật cho intent: Visa/Policy + Weather/Event
History: Summarize every 5 turns
```

### Lý do

```text
1. DeepSeek V4 Pro (promo) là model strong nhưng rẻ hơn GPT-5.5 ~34× và rẻ hơn Sonnet 4.6 ~17× —
   "best bang for buck" nếu cần chất lượng cao mà không muốn trả premium.
2. Summarize every 5 turns tiết kiệm tokens hơn Full history — mỗi 5 lượt tóm tắt 1 lần,
   giảm tokens nhưng vẫn giữ được context dài hạn (tốt hơn Last 5 cho conversation 7+ turns).
3. Phù hợp cho doanh nghiệp muốn chất lượng strong nhưng budget bị siết (mùa cao điểm volume lớn).
```

---

## Bảng kiểm trước khi tính cost

- [x] ≥3 configs đã đặt tên (không chỉ "Config 1/2/3")
- [x] Mỗi config đã chốt rõ 3 knobs (không còn ô trống)
- [x] Mỗi config có ≥2 câu lý do
- [x] 3 configs đủ khác biệt — không phải chỉ đổi mỗi 1 knob nhỏ
- [x] Nhóm đồng thuận đây là 3 configs đáng so sánh

**Nếu 3 configs quá giống nhau** (chỉ đổi model, knobs khác giống hệt) → quay lại tweak. Mục đích là thấy tradeoff — configs giống nhau quá → không thấy tradeoff.

Xong → mở `03-cost-calculation.md` để bắt đầu tính cost.
