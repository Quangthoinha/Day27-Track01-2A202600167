# 01 · Base Flow + Chốt 3 Knobs

> **Mục tiêu**: Hiểu chatbot hoạt động ra sao ở mức base (không chọn config gì) - và xác định 3 knobs nhóm sẽ tweak ở các bước sau.
>
> **Thời gian**: 7 phút (trong 15 phút phần Setup)

---

## Bước 1 - Đọc base flow trong cost reference card

- Khi tourist gửi tin nhắn, AI làm gì đầu tiên? → **Intent Classification** (phân loại ý định)
- 5 intent dẫn đến 5 hành động khác nhau - hành động nào tốn LLM, hành động nào không? → **Booking & Complaint** = $0 LLM (chuyển người), **Visa/Guide/Weather** = tốn LLM
- Sau khi route, AI ráp gì lại để generate response? → **Context Assembly**: system prompt + history + RAG chunks + web search (nếu bật) + user message
---

## Bước 2 - Vẽ lại flow theo cách hiểu của nhóm

```
```text
┌────────────────────────────────────────────────────────────┐
│                 TOURIST GỬI TIN NHẮN                       │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼

┌────────────────────────────────────────────────────────────┐
│           1. INTENT CLASSIFICATION (LLM call)              │
│                                                            │
│  Phân loại intent:                                         │
│  - Visa                                                    │
│  - Guide                                                   │
│  - Weather                                                 │
│  - Booking                                                 │
│  - Complaint                                               │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼

┌────────────┬────────────┬────────────┬────────────┬────────────┐
│   Visa     │   Guide    │  Weather   │  Booking   │ Complaint  │
└─────┬──────┴─────┬──────┴─────┬──────┴─────┬──────┴─────┬──────┘
      │            │            │            │            │
      ▼            ▼            ▼            ▼            ▼

┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ RAG + Web  │ │    RAG     │ │  Web only  │ │  HANDOFF   │ │ ESCALATE   │
│  (policy)  │ │  (KB info) │ │ (real-time)│ │   Sales    │ │  Manager   │
│    $LLM    │ │    $LLM    │ │    $LLM    │ │     $0     │ │     $0     │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └────────────┘ └────────────┘
      │              │              │
      └──────────────┴──────┬───────┘
                             │
                             ▼

┌────────────────────────────────────────────────────────────┐
│                  3. CONTEXT ASSEMBLY                       │
│                                                            │
│  - System prompt: 500 tokens                               │
│  - Chat history: 260 tokens / turn                         │
│  - RAG chunks: 1,250 tokens                                │
│  - Web search results: 800 tokens (nếu bật)                │
│  - User message: 80 tokens                                 │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼

┌────────────────────────────────────────────────────────────┐
│           4. RESPONSE GENERATION (LLM call)                │
│                                                            │
│      Model tạo câu trả lời (~180 output tokens)            │
└────────────────────────────────────────────────────────────┘
```

**4 điểm bắt buộc trong flow:**
1. ✅ Intent Classification - phân loại ý định
2. ✅ Route theo intent - 5 nhánh (RAG / Web / Handoff / Escalate)
3. ✅ Context Assembly - ráp system prompt + history + RAG + web + user msg
4. ✅ Response Generation - model tạo câu trả lời

---

## Bước 3 - Xác định 3 Knobs

3 knobs là 3 quyết định thiết kế nhóm có thể tweak. Mỗi config nhóm thiết kế = 1 bộ chọn tại 3 knobs này.

Trước khi điền vào ô bên dưới, đọc nhanh mục **3. Decision Points** của `cost-reference-card.md`. Sau đó tự hỏi:

- **Knob 1 - Model tier**: model rẻ và model mạnh chênh bao nhiêu lần? Có thể mix theo intent không? → **Có thể chênh 20-50× (cheap vs premium)**
- **Knob 2 - Web search**: intent nào *cần* real-time? intent nào không cần? → **Visa & Weather cần real-time, Guide thì RAG đủ**
- **Knob 3 - History**: 7 lượt chat cuối đắt hay rẻ? Cắt history có rủi ro gì? → **Mỗi turn thêm 260 tokens, quên context có thể làm khách khó chịu**

### Knob 1 - Model tier

**Câu hỏi:** Chất lượng câu trả lời ở mức nào?

Options:

```text
☑ Cheap        (Gemini Flash-Lite / DeepSeek V4 Flash / GPT-4o-mini)
□ Mid          (Gemini Flash / Claude Haiku 4.5)
□ Strong       (DeepSeek V4 Pro / Claude Sonnet 4.6)
□ Premium      (Claude Opus 4.7 / GPT-5.5)
□ Mix          (model khác nhau cho intent khác nhau - viết rõ)
```

**Câu hỏi gợi mở cho nhóm** (trả lời trước khi chọn):

- Mục tiêu chính là chi phí thấp hay chất lượng cao? → **Cần cân bằng: Guide chiếm 59%, dùng cheap cho Guide, strong cho Visa/Complaint**
- Tourist hỏi câu phức tạp hay đơn giản hơn? → **Hỏi điểm đến phổ biến, câu hỏi không quá phức tạp**
- Có nên dùng cheap cho phân loại + strong cho trả lời không? → **Có - classifier có thể dùng keyword matching = $0**

```text
Nhóm hướng đến mix-model approach:
- Classifier: keyword matching ($0)
- Guide intents (59%): Gemini Flash-Lite (cheap)
- Visa/Weather intents: DeepSeek V4 Pro (strong nhưng giá hợp lý)
- Complaint: Claude Sonnet (cần respond cẩn thận)
```

### Knob 2 - Web search

**Câu hỏi:** Có cần thông tin real-time không?

Options:

```text
□ OFF              (chỉ dùng RAG - knowledge base có sẵn)
☑ ON selective     (bật cho 1–2 intent cần real-time: visa, weather)
□ ON broad         (bật cho hầu hết intent)
```

**Câu hỏi gợi mở:**

- Visa policy đổi mỗi tháng - RAG có đủ không? → **Không đủ - visa policy thay đổi thường xuyên, cần web search**
- Weather là thông tin real-time tự nhiên - không có lựa chọn khác đúng không? → **Đúng - weather cần real-time**
- Web search tốn $0.008/call + 800 tokens - bật bừa có lợi không? → **Không - chỉ bật cho Visa + Weather**

```text
Nhóm quyết định ON selective cho:
- Visa/Policy (1/22 = 5%) - policy thay đổi thường xuyên
- Weather/Event (2/22 = 9%) - tự nhiên là real-time
→ Chỉ 14% conversations cần web search
```

### Knob 3 - History management

**Câu hỏi:** Chatbot cần nhớ bao nhiêu context của conversation?

Options:

```text
□ Last 3 turns        (nhẹ nhất, dễ quên)
☑ Last 5 turns        (cân bằng)
□ Full history        (nhớ tất cả, đắt nhất ở conv dài)
□ Summarize every 5   (nâng cao - cần 1 LLM call phụ để tóm tắt)
```

**Câu hỏi gợi mở:**

- Tourist hay nói "tôi đã nói budget là $500 ở turn 1" rồi turn 7 hỏi gợi ý - nếu quên thì sao? → **Quên budget = suggest sai → khách không hài lòng**
- Scenario A trung bình 4 lượt → full history có tốn nhiều không? → **Không cần full, Last 5 đủ cho 4 turns**
- Scenario B trung bình 7 lượt → mỗi turn thêm 260 tokens - tổng thêm bao nhiêu? → **7 turns × 260 = 1,820 tokens thêm → tốn thêm ~$0.001-0.003/conversation**

```text
Nhóm chọn Last 5 turns:
- Scenario A (4 turns): đủ nhớ toàn bộ
- Scenario B (7 turns): vẫn nhớ 5 turns gần nhất, có thể miss turn 1-2
- Risk: nếu tourist nói budget ở turn 1, turn 6 có thể quên → cần tự khắc phục bằng cách nhắc khách
```

---

## Bước 4 - Sơ bộ nhóm muốn thử những combo nào?

Chưa cần quyết định cuối cùng. Chỉ cần phác thảo: nhóm dự định thử ít nhất 3 combo khác nhau. Càng khác nhau, càng dễ thấy tradeoff.

**Combo 1 (định hướng cheap)**:

```text
Model: Gemini Flash-Lite (response) + keyword (classifier)
Web: OFF (chỉ RAG)
History: Last 3 turns
→ Tên dự kiến: "Budget Bot"
```

**Combo 2 (định hướng premium)**:

```text
Model: Claude Sonnet 4.6 (response) + Claude Haiku (classifier)
Web: ON selective (Visa + Weather)
History: Full history
→ Tên dự kiến: "Premium Concierge"
```

**Combo 3 (định hướng balanced / smart mix)**:

```text
Model: Mix - Gemini Flash-Lite cho Guide, DeepSeek V4 Pro cho Visa, Claude Sonnet cho Complaint
Web: ON selective (Visa + Weather)
History: Last 5 turns
→ Tên dự kiến: "Smart Router"
```

**Combo 4** (optional - nếu nhóm có ý tưởng khác):

```text
Model: DeepSeek V4 Pro cho tất cả
Web: ON selective (Visa + Weather + Safety)
History: Last 5 turns
→ Tên dự kiến: "Value Leader"
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Đã vẽ flow base có đủ 4 bước (Intent → Route → Context → Response)
- [x] Hiểu Booking + Khiếu nại = $0 LLM cost (chuyển con người)
- [x] Đã phác thảo ≥3 combo khác nhau (chưa cần chi tiết)
- [x] Nhóm đồng thuận về hướng đi mỗi combo

Xong → chuyển sang **Main phase**. Mở `02-config-design.md`.
