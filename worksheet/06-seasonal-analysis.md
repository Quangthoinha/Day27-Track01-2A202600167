# 06 · Seasonal Analysis — Chi phí AI theo 12 tháng (Dữ liệu thực tế)

> **Mục tiêu**: Tính số users thực tế và chi phí AI cho từng tháng trong năm, dựa trên dữ liệu du lịch Việt Nam 2024-2025 + benchmark chatbot toàn cầu.
>
> **Nguồn dữ liệu**:
> - Vietnam National Authority of Tourism (VNAT) — lượt khách quốc tế theo tháng
> - vietnambooking.com traffic (Semrush) — ~90K visits/tháng peak
> - YonderHQ chatbot benchmark — 1.5% engagement rate, 3.1 turns/conv (AI-resolved)
> - LoopReply — 10,000 conversations analyzed across industries
>

---

## 1. Dữ liệu thực tế — Tourism Vietnam 2024-2025

### Lượt khách quốc tế đến Việt Nam theo tháng (ước tính 2025)

| Tháng | Khách quốc tế | Mùa | Ghi chú |
|---|---|---|---|
| **T1** | ~1.9M | Cao-Tết | Tết Nguyên Đán, khách TQ/Hàn nhiều |
| **T2** | ~1.8M | Trung bình | Post-Tết dip nhẹ |
| **T3** | ~2.05M | **Cao** | Spring peak, khách Âu đông |
| **T4** | ~1.65M | Trung bình | Sau peak, thời tiết đẹp |
| **T5** | ~1.53M | Trung bình-thấp | Bắt đầu mùa mưa |
| **T6** | ~1.4M | Trung bình | Mùa mưa miền Bắc/Trung |
| **T7** | ~1.55M | Cao (hè) | School holidays, khách gia đình |
| **T8** | ~1.68M | **Cao** (hè) | Peak hè, beach demand |
| **T9** | ~1.45M | Trung bình | Cuối mùa mưa, planning Q4 |
| **T10** | ~1.6M | Trung bình-cao | Mùa thu đẹp, khách tăng |
| **T11** | ~1.75M | Cao | Bắt đầu mùa cao điểm Q4 |
| **T12** | ~2.0M | **Rất cao** | Christmas, NYE, booking Q1/2026 |
| **Tổng** | **~20.4M/năm** | | |

### Website traffic agency theo mùa (benchmark vietnambooking.com scaled)

Theo Semrush, vietnambooking.com (OTA VN top) có:
- Tháng thấp (Jan): ~62K visits
- Tháng cao (Dec): ~90K visits
- Peak/thấp ratio: **~1.5×**

**Scale cho agency theo đề bài** (đạt 300 conv/day = ~20K visitors/day):

| Tháng | Visitors/tháng | Visitors/ngày | Chatbot Users/ngày (1.5% engage) | Mùa |
|---|---|---|---|---|
| T1 | 1.2M | 40,000 | **600** | Cao |
| T2 | 900K | 30,000 | **450** | TB |
| T3 | 1.5M | 50,000 | **750** | **Cao** |
| T4 | 1.0M | 33,000 | **500** | TB |
| T5 | 800K | 27,000 | **400** | TB-Thấp |
| T6 | 700K | 23,000 | **350** | TB |
| T7 | 900K | 30,000 | **450** | Cao (hè) |
| T8 | 1.1M | 37,000 | **550** | Cao |
| T9 | 850K | 28,000 | **420** | TB |
| T10 | 950K | 32,000 | **475** | TB-Cao |
| T11 | 1.1M | 37,000 | **550** | Cao |
| T12 | 1.4M | 47,000 | **700** | **Rất cao** |

→ **Users thực tế**: 350–750 users/ngày tương tác chatbot (không phải 300–1,200 như đề bài).

Nếu agency lớn hơn (đề bài), scale factor ~2×: **700–1,500 users/ngày**.

---

## 2. Tính toán chi phí AI — 3 Scenarios

### Scenario 1: Agency vừa (350–750 users/ngày)

**Giả định**: Avg 3.1 turns/conv, intent mix thay đổi theo mùa.

| Tháng | Users/ngày | Turns/conv | Intent Mix | Budget Bot/Tháng | Smart Mix/Tháng | Premium/Tháng |
|---|---|---|---|---|---|---|
| T1 | 600 | 3.5 | Guide 50%, Visa 20%, Weather 10%, Booking 15%, Complaint 5% | **$3.24** | **$18.90** | **$1,026** |
| T2 | 450 | 3.2 | Guide 55%, Visa 18%, Weather 8%, Booking 12%, Complaint 7% | **$2.18** | **$12.15** | **$720** |
| T3 | 750 | 3.8 | Guide 45%, Visa 22%, Weather 12%, Booking 16%, Complaint 5% | **$4.86** | **$30.38** | **$1,539** |
| T4 | 500 | 3.3 | Guide 52%, Visa 20%, Weather 10%, Booking 13%, Complaint 5% | **$2.70** | **$15.75** | **$855** |
| T5 | 400 | 3.0 | Guide 58%, Visa 15%, Weather 12%, Booking 10%, Complaint 5% | **$1.80** | **$10.20** | **$600** |
| T6 | 350 | 2.8 | Guide 60%, Visa 15%, Weather 10%, Booking 10%, Complaint 5% | **$1.47** | **$8.23** | **$504** |
| T7 | 450 | 3.2 | Guide 55%, Visa 18%, Weather 8%, Booking 12%, Complaint 7% | **$2.18** | **$12.15** | **$720** |
| T8 | 550 | 3.4 | Guide 50%, Visa 20%, Weather 10%, Booking 15%, Complaint 5% | **$2.97** | **$17.33** | **$943** |
| T9 | 420 | 3.0 | Guide 58%, Visa 15%, Weather 12%, Booking 10%, Complaint 5% | **$1.89** | **$10.71** | **$630** |
| T10 | 475 | 3.1 | Guide 55%, Visa 18%, Weather 10%, Booking 12%, Complaint 5% | **$2.21** | **$12.83** | **$743** |
| T11 | 550 | 3.3 | Guide 52%, Visa 20%, Weather 10%, Booking 13%, Complaint 5% | **$2.70** | **$15.75** | **$855** |
| T12 | 700 | 3.6 | Guide 48%, Visa 20%, Weather 10%, Booking 17%, Complaint 5% | **$3.78** | **$22.68** | **$1,176** |
| **TỔNG NĂM** | | | | **$31.98** | **$197.04** | **$10,311** |

### Scenario 2: Agency lớn (theo đề bài — 700–1,500 users/ngày)

| Tháng | Users/ngày | Budget Bot/Tháng | Smart Mix/Tháng | Premium/Tháng |
|---|---|---|---|---|
| T1 | 1,200 | **$6.48** | **$37.80** | **$2,052** |
| T2 | 900 | **$4.37** | **$24.30** | **$1,440** |
| T3 | 1,500 | **$9.72** | **$60.75** | **$3,078** |
| T4 | 1,000 | **$5.40** | **$31.50** | **$1,710** |
| T5 | 800 | **$3.60** | **$20.40** | **$1,200** |
| T6 | 700 | **$2.97** | **$16.43** | **$1,008** |
| T7 | 900 | **$4.37** | **$24.30** | **$1,440** |
| T8 | 1,100 | **$5.94** | **$34.65** | **$1,886** |
| T9 | 840 | **$3.78** | **$21.42** | **$1,260** |
| T10 | 950 | **$4.43** | **$25.65** | **$1,486** |
| T11 | 1,100 | **$5.40** | **$31.50** | **$1,710** |
| T12 | 1,400 | **$7.56** | **$45.36** | **$2,352** |
| **TỔNG NĂM** | | **$64.02** | **$394.06** | **$20,622** |

---

## 3. So sánh chi phí AI vs Human theo tháng

### Human baseline (1 nhân viên)
- 30 conversations/ngày × 30 ngày = 900 conv/tháng
- Lương: $15/ngày × 30 = **$450/tháng**
- **Chi phí/conversation = $0.50**

### Agency vừa (550 users/ngày trung bình)

| Tháng | Users | Human Cost | Smart Mix Cost | Rẻ hơn |
|---|---|---|---|---|
| T12 (cao) | 700/day = 21K/mo | $10,500 | **$22.68** | **463×** |
| T6 (thấp) | 350/day = 10.5K/mo | $5,250 | **$8.23** | **638×** |
| **TB năm** | 16.5K/mo | $8,250 | **$16.42** | **502×** |

→ **Smart Mix tiết kiệm ~$8,200–$10,500/tháng** so với thuê nhân viên.

### Agency lớn (1,100 users/ngày TB)

| Tháng | Users | Human Cost | Smart Mix Cost | Rẻ hơn |
|---|---|---|---|---|
| T12 (cao) | 1,400/day = 42K/mo | $21,000 | **$45.36** | **463×** |
| T6 (thấp) | 700/day = 21K/mo | $10,500 | **$16.43** | **639×** |
| **TB năm** | 33K/mo | $16,500 | **$32.84** | **502×** |

→ **Smart Mix tiết kiệm ~$16,400–$21,000/tháng**.

---

## 4. Kết luận

### Số users thực tế

| Loại agency | Users/ngày (TB) | Users/tháng (TB) | Users/năm |
|---|---|---|---|
| **Nhỏ** (village/local) | 50–150 | 1,500–4,500 | ~20K–60K |
| **Vừa** (city/regional) | 350–750 | 10K–22K | ~150K–270K |
| **Lớn** (national/OTA) | 700–1,500 | 21K–45K | ~300K–540K |

→ Theo đề bài (300–1,200 conv/day), đây là **agency lớn** cấp quốc gia hoặc OTA.

### Chi phí AI thực tế (Smart Mix)

| Agency Size | Chi phí/năm | So với human |
|---|---|---|
| Vừa | **$197/năm** | Rẻ hơn ~$99,000 |
| Lớn | **$394/năm** | Rẻ hơn ~$198,000 |

→ **Ngay cả agency lớn nhất, chi phí AI 1 năm chỉ bằng 1 bữa ăn nhà hàng.**

---

## 5. Chi phí triển khai (Implementation Cost)

Đây là chi phí **1 lần**, không phải recurring:

| Hạng mục | Chi phí | Ghi chú |
|---|---|---|
| **Development** (chatbot UI, API integration) | $2,000–$5,000 | 2-4 tuần, 1-2 devs |
| **Knowledge base setup** (40 articles, indexing) | $200–$500 | One-time |
| **Vector DB** (Pinecone/Weaviate) | $0–$200/tháng | Free tier đủ cho startup |
| **Tavily web search API** | $0–$50/tháng | 1,500 free requests/ngày |
| **Testing & QA** | $500–$1,000 | 1 tuần |
| **Monitoring** (Langfuse/Datadog) | $0–$100/tháng | Free tier có sẵn |
| **TỔNG TRIỂN KHAI** | **$2,700–$6,800** | |
| **TỔNG VẬN HÀNH/năm** (Smart Mix, agency lớn) | **$394 + $2,400 (infra)** = **$2,800** | |
| **TỔNG CHI PHÍ NĂM ĐẦU** | **$5,500–$9,600** | |
| **TỔNG CHI PHÍ NĂM 2+** | **~$2,800/năm** | Chỉ vận hành |

→ **ROI**: Tiết kiệm $16,500/tháng = **$198,000/năm** — trừ chi phí AI $2,800 = **lãi $195,000/năm**.
**Break-even sau 1 tháng.**
