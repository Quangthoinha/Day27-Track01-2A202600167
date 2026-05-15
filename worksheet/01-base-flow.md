# 01 · Base Flow + Chốt 3 Knobs

> **Mục tiêu**: Hiểu chatbot hoạt động ra sao ở mức base (không chọn config gì) — và xác định 3 knobs nhóm sẽ tweak ở các bước sau.
>
> **Thời gian**: 7 phút (trong 15 phút phần Setup)

---

## Bước 1 — Đọc base flow trong cost reference card

Mở file `cost-reference-card.md` ở phần **2. Base Flow** — xem flow chatbot mặc định. Đây là cấu trúc mọi config sẽ build dựa trên.

Đọc xong, tự kiểm tra hiểu:

- Khi tourist gửi tin nhắn, AI làm gì đầu tiên?
- 5 intent dẫn đến 5 hành động khác nhau — hành động nào tốn LLM, hành động nào không?
- Sau khi route, AI ráp gì lại để generate response?

Nếu chưa hiểu → quay lại đọc lại 1 lần nữa. Đừng đi tiếp khi còn mơ hồ.

---

## Bước 2 — Vẽ lại flow theo cách hiểu của nhóm

Vẽ flow ra giấy hoặc trên bảng (1 thành viên vẽ, cả nhóm góp ý). Có thể dùng ASCII đơn giản:

```text
TOURIST GỬI TIN NHẮN
         │
         ▼
┌─ Intent Classification ───────────────────────────┐
│  Phân loại ý định khách hàng bằng LLM Classifier   │
│  → Visa/Policy | Guide/Destination | Weather/Event │
│  → Tour/Booking | Complaint                        │
└────────┬──────────────────────────────────────────┘
         │
    ┌────┼────┬──────────┬───────────┐
    ▼    ▼    ▼          ▼           ▼
  Visa  Guide Weather  Booking   Complaint
    │    │      │         │          │
    ▼    ▼      ▼         ▼          ▼
┌──────────────┐ ┌────┐  ┌────┐  ┌──────────┐
│ Knowledge    │ │RAG │  │    │  │          │
│ Lookup:      │ │Only│  │Hand│  │ Escalate │
│ RAG top-5 +  │ │    │  │off │  │ Manager  │
│ Web search?  │ │    │  │$0  │  │ $0       │
└──────┬───────┘ └────┘  └────┘  └──────────┘
       │
       ▼
┌─ Context Assembly ──────────────────────────────┐
│  System prompt (500 tok) +                        │
│  Chat history (N turns × 260 tok) +               │
│  RAG chunks (1,250 tok) +                         │
│  Web search results (800 tok, nếu bật) +          │
│  User message (80 tok)                            │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌─ Response Generation ─────────────────────────────┐
│  Model tạo câu trả lời (180 tok output)           │
└───────────────────────────────────────────────────┘
```

**Giải thích 4 bước:**

1. **Intent Classification**: LLM classifier phân loại câu hỏi (150 input + 20 output tokens). Booking và Complaint không cần qua bước 2-3-4 — chuyển ngay cho người.
2. **Route theo intent**: 5 nhánh. Visa/Guide/Weather cần RAG lookup. Booking/Complaint handoff → $0 LLM cost cho phần còn lại.
3. **Context Assembly**: Ráp system prompt + history + RAG (cố định 1,250 tok) + web search (nếu bật) + user message thành 1 prompt duy nhất.
4. **Response Generation**: Model tạo câu trả lời (180 tokens output). Đây là bước tốn tiền nhất vì output giá cao hơn input 3-5×.

Khi vẽ, đảm bảo flow có 4 điểm:

1. **Intent classification** — phân loại ý định
2. **Route theo intent** — 5 nhánh đi đâu (RAG / Web search / Handoff / Escalate)
3. **Context assembly** — ráp system prompt + history + RAG + web (nếu bật) + user msg
4. **Response generation** — model tạo câu trả lời

Nếu nhóm vẽ thiếu 1 trong 4 bước → bổ sung trước khi đi tiếp.

---

## Bước 3 — Xác định 3 Knobs

3 knobs là 3 quyết định thiết kế nhóm có thể tweak. Mỗi config nhóm thiết kế = 1 bộ chọn tại 3 knobs này.

Trước khi điền vào ô bên dưới, đọc nhanh mục **3. Decision Points** của `cost-reference-card.md`. Sau đó tự hỏi:

- Knob 1 — Model tier: model rẻ và model mạnh chênh bao nhiêu lần? Có thể mix theo intent không?
- Knob 2 — Web search: intent nào *cần* real-time? intent nào không cần?
- Knob 3 — History: 7 lượt chat cuối đắt hay rẻ? Cắt history có rủi ro gì?

### Knob 1 — Model tier

**Câu hỏi:** Chất lượng câu trả lời ở mức nào?

Options:

```text
□ Cheap        (GPT-5 nano $0.05/$0.40 / GPT-4.1 nano $0.10/$0.40 / Gemini 2.5 Flash-Lite $0.10/$0.40 / DeepSeek V4 Flash $0.14/$0.28)
□ Mid          (GPT-5 mini $0.25/$2.00 / Gemini 3.1 Flash-Lite $0.25/$1.50 / Gemini 2.5 Flash $0.30/$2.50 / GPT-4.1 mini $0.40/$1.60 / Claude Haiku 4.5 $1.00/$5.00)
□ Strong       (DeepSeek V4 Pro $0.435/$0.87 promo / Gemini 2.5 Pro $1.25/$10.00 / GPT-4.1 $2.00/$8.00 / Claude Sonnet 4.6 $3.00/$15.00)
□ Premium      (Claude Opus 4.7 $5.00/$25.00 / GPT-5.5 $5.00/$30.00)
□ Mix          (model khác nhau cho intent khác nhau — viết rõ)
```

**Câu hỏi gợi mở cho nhóm** (trả lời trước khi chọn):

- Mục tiêu chính là chi phí thấp hay chất lượng cao?
- Tourist hỏi câu phức tạp hay đơn giản hơn?
- Có nên dùng cheap cho phân loại + strong cho trả lời không?

```text
Nhóm nhận thấy 59% câu hỏi là Guide/Destination (FAQ đơn giản) — không cần model mạnh.
Còn Visa/Policy (5%) và Weather (9%) cần chính xác hơn.
→ Nên dùng cheap model (GPT-5 nano $0.05/$0.40 — rẻ nhất thị trường) cho Guide,
  và mid (Gemini 3.1 Flash-Lite $0.25/$1.50 hoặc GPT-4.1 mini $0.40/$1.60) cho Visa/Weather.
Classifier có thể dùng keyword matching ($0) hoặc GPT-5 nano (~170 tokens, ~$0.00001).
```

### Knob 2 — Web search

**Câu hỏi:** Có cần thông tin real-time không?

Options:

```text
□ OFF              (chỉ dùng RAG — knowledge base có sẵn)
□ ON selective    (bật cho 1–2 intent cần real-time: visa, weather)
□ ON broad         (bật cho hầu hết intent)
```

**Câu hỏi gợi mở:**

- Visa policy đổi mỗi tháng — RAG có đủ không?
- Weather là thông tin real-time tự nhiên — không có lựa chọn khác đúng không?
- Web search tốn $0.005/call + 800 tokens — bật bừa có lợi không?

```text
Visa policy đổi mỗi tháng — RAG có thể outdated nếu không cập nhật liên tục.
Weather là real-time tự nhiên — không web search thì không thể trả lời đúng.
Nhưng Guide (59% volume) như "điểm đến", "ẩm thực" — KB đủ, không cần web.
→ Chọn ON selective: chỉ bật cho Visa và Weather.
Cost thêm: $0.008/query + 800 tokens input (~$0.0001-$0.001 tùy model).
```

### Knob 3 — History management

**Câu hỏi:** Chatbot cần nhớ bao nhiêu context của conversation?

Options:

```text
□ Last 3 turns        (nhẹ nhất, dễ quên)
□ Last 5 turns        (cân bằng)
□ Full history        (nhớ tất cả, đắt nhất ở conv dài)
□ Summarize every 5   (nâng cao — cần 1 LLM call phụ để tóm tắt)
```

**Câu hỏi gợi mở:**

- Tourist hay nói "tôi đã nói budget là $500 ở turn 1" rồi turn 7 hỏi gợi ý — nếu quên thì sao?
- Scenario A trung bình 4 lượt → full history có tốn nhiều không?
- Scenario B trung bình 7 lượt → mỗi turn thêm 260 tokens — tổng thêm bao nhiêu?

```text
Tourist hay hỏi nhiều chủ đề liên tiếp trong 1 conversation (T1 hỏi 7 câu khác nhau).
Nếu chỉ nhớ Last 3 turns → dễ quên budget/điểm đến đã nhắc ở turn 1.
Nhưng Full history ở Scenario B (7 turns) = 6×260 = 1,560 tokens — đắt gấp đôi.
→ Chọn Last 5 turns là sweet spot: đủ nhớ context ngắn hạn, không quá đắt.
```

---

## Bước 4 — Sơ bộ nhóm muốn thử những combo nào?

Chưa cần quyết định cuối cùng. Chỉ cần phác thảo: nhóm dự định thử ít nhất 3 combo khác nhau. Càng khác nhau, càng dễ thấy tradeoff.

**Combo 1 (định hướng cheap)**:

```text
Model: GPT-5 nano ($0.05/$0.40) — rẻ nhất, 1 model cho tất cả intent
Web: OFF (chỉ RAG)
History: Last 3 turns
Tên dự kiến: "Budget Bot"
```

**Combo 2 (định hướng premium)**:

```text
Model: GPT-5.5 ($5.00/$30.00) — flagship mới nhất, 1 model cho tất cả intent
Web: ON broad (bật cho hầu hết intent)
History: Full history
Tên dự kiến: "Premium Concierge"
```

**Combo 3 (định hướng balanced / smart mix)**:

```text
Model: Mix — GPT-5 nano ($0.05/$0.40) cho Guide (59% volume),
            Gemini 3.1 Flash-Lite ($0.25/$1.50) cho Visa/Weather
Web: ON selective — bật cho Visa + Weather
History: Last 5 turns
Tên dự kiến: "Smart Mix"
```

**Combo 4** (optional — nếu nhóm có ý tưởng khác):

```text
Model: DeepSeek V4 Pro promo ($0.435/$0.87) — strong nhưng rẻ hơn GPT-5.5 ~34×
Web: ON selective — Visa + Weather
History: Summarize every 5 turns
Tên dự kiến: "Deep Value"
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Đã vẽ flow base có đủ 4 bước (Intent → Route → Context → Response)
- [x] Hiểu Booking + Khiếu nại = $0 LLM cost (chuyển con người)
- [x] Đã phác thảo ≥3 combo khác nhau (Budget Bot, Premium Concierge, Smart Mix, Deep Value)
- [x] Nhóm đồng thuận về hướng đi mỗi combo

**Note về volume thực tế:** Theo dữ liệu Vietnam tourism 2025 (VNAT) + Semrush (vietnambooking.com), agency vừa có **350–750 users/ngày** theo mùa, không phải 300–1,200 như đề bài. Avg turns thực tế: **3.1 turns** (không phải 4–7). Chi tiết: `06-seasonal-analysis.md`.

Xong → 10:25 chuyển sang **Main phase**. Mở `02-config-design.md`.
