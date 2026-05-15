# 00 · User Journey Simulation — Đóng vai Tourist

> **Mục tiêu**: Trước khi tính chi phí, nhóm phải hình dung được khách hàng thật sự hỏi gì, hỏi như thế nào, và 1 conversation thực tế trông ra sao.
>
> **Thời gian**: 8 phút (trong 15 phút phần Setup)

---

## Bước 1 — Mỗi người đóng vai 1 tourist (4 phút)

### Tourist #1 (Tên thành viên: Nguyễn Hữu Quang)

**Persona**: Một du khách Mỹ, thích trải nghiệm văn hóa, đi cùng gia đình, ngân sách khá nhưng rất quan tâm đến vấn đề an toàn và visa.

```text
1. Hi! I'm planning a trip to Vietnam for 4 people in July. Is it a good time to visit or will it rain all day?
2. We really want to see Ha Long Bay. Do you have any overnight cruise packages that are kid-friendly?
3. How does the e-visa process work for US citizens? Can your agency help me with that?
4. I've heard a lot about street food in Hanoi, but I'm worried about stomach issues. Are there any "safe" food tours?
5. What is the best way to travel from Da Nang to Hoi An? Is it easy to catch a taxi?
6. Can you recommend a 5-star hotel near the French Quarter in Hanoi?
7. Is it safe to use Grab at night in Vietnam?
```

---

### Tourist #2 (Tên thành viên: Trần Vọng Triển)

**Persona:** Couple từ Hàn Quốc, honeymoon trip, budget cao, quan tâm luxury + trải nghiệm đẹp + đồ ăn

```text
1. We're planning our honeymoon in Vietnam. Which destination is more romantic: Da Nang, Phu Quoc, or Ha Long Bay?
2. Can you recommend a luxury beach resort with a private pool?
3. What's the weather like in central Vietnam in July?
4. Are there any fine dining Vietnamese restaurants we should try? I'm vegetarian. Will it be hard for me to find local food that I can eat?
5. Is it easy to travel between Da Nang and Hoi An?
6. Can your company arrange airport pickup and a private tour guide?
7. How much should we expect to spend for a comfortable 7-day trip?
8. I saw some bad reviews online about tour cancellations and hidden fees. What happens if our booking gets changed or canceled at the last minute?
```

---

### Tourist #3 (Tên thành viên: Nguyễn Thị Ngọc Thư)

**Persona:** Gia đình từ Úc, đi cùng 2 trẻ em, muốn an toàn + tiện lợi, lo về food safety + lịch trình cho trẻ nhỏ

```text
1. We're traveling to Vietnam with two young kids. Which city is the most family-friendly?
2. Is Vietnamese street food safe for children?
3. Can you suggest a 5-day itinerary that isn't too exhausting for kids?
4. Are baby seats available in taxis or private cars?
5. Which attractions are fun for both adults and children?
6. Do hospitals in major cities have English-speaking staff?
7. What apps should we install before arriving in Vietnam?
```

## Bước 2 — Gom lại và phân loại (4 phút)

| # | Câu hỏi (1 dòng) | Intent | Lượt chat ước tính | Bot / Người |
|---|---|---|---|---|
| 1 | July weather in Vietnam - good time to visit? | Thời tiết/Sự kiện | 1 | ☑ Bot |
| 2 | Kid-friendly Ha Long Bay overnight cruise | Điểm đến/Guide + Tour/Booking | 2 | ☑ Bot |
| 3 | E-visa process for US citizens | Visa/Policy | 2 | ☑ Bot |
| 4 | Safe street food tours in Hanoi | Điểm đến/Guide | 1 | ☑ Bot |
| 5 | Da Nang to Hoi An transport options | Điểm đến/Guide | 1 | ☑ Bot |
| 6 | 5-star hotel near French Quarter Hanoi | Tour/Booking | 2 | ☑ Bot → Sales |
| 7 | Safety of Grab at night in Vietnam | Điểm đến/Guide | 1 | ☑ Bot |
| 8 | Romantic destination for honeymoon | Điểm đến/Guide | 2 | ☑ Bot |
| 9 | Luxury beach resort with private pool | Tour/Booking | 2 | ☑ Bot → Sales |
| 10 | Weather in central Vietnam July | Thời tiết/Sự kiện | 1 | ☑ Bot |
| 11 | Vegetarian fine dining Vietnamese restaurants | Điểm đến/Guide | 2 | ☑ Bot |
| 12 | Da Nang to Hoi An travel (repeat) | Điểm đến/Guide | 1 | ☑ Bot |
| 13 | Airport pickup + private tour guide | Tour/Booking | 2 | ☑ Bot → Sales |
| 14 | Budget estimate for 7-day trip | Điểm đến/Guide | 2 | ☑ Bot |
| 15 | Tour cancellation & hidden fees policy | Khiếu nại/Policy | 2 | ☑ Bot → Manager |
| 16 | Most family-friendly city in Vietnam | Điểm đến/Guide | 2 | ☑ Bot |
| 17 | Street food safety for children | Điểm đến/Guide | 1 | ☑ Bot |
| 18 | 5-day kid-friendly itinerary | Điểm đến/Guide | 3 | ☑ Bot |
| 19 | Baby seats in taxis/private cars | Điểm đến/Guide | 1 | ☑ Bot |
| 20 | Family-friendly attractions | Điểm đến/Guide | 2 | ☑ Bot |
| 21 | Hospitals with English-speaking staff | Điểm đến/Guide | 1 | ☑ Bot |
| 22 | Must-have apps before arriving Vietnam | Điểm đến/Guide | 1 | ☑ Bot |

---

## Bước 3 — Rút insight cho nhóm (cuối phần Setup)

**Tổng số câu hỏi nhóm gom được**: 22

**Phân bố intent thực tế của nhóm** (% mỗi intent):

```text
Guide (Điểm đến): 59% (13/22) — chiếm đa số
Tour/Booking: 23% (5/22)
Visa/Policy: 5% (1/22)
Weather/Sự kiện: 9% (2/22)
Khiếu nại: 5% (1/22)
```

**Số lượt chat trung bình để xong 1 chủ đề**:

```text
- Info/Guide thông thường: 1-2 lượt
- Địa điểm phức tạp (itinerary): 3 lượt
- Booking cần tư vấn: 2 lượt
- Khiếu nại chính sách: 2 lượt
→ Trung bình: ~2 lượt/ câu hỏi
```

**Đối chiếu với đề bài** (Scenario A = 4 lượt, Scenario B = 7 lượt):

```text
Khác vì đề bài tính theo 1 conversation đầy đủ với nhiều intent,
còn bảng trên tính cho từng câu hỏi riêng lẻ. Khi tourist hỏi
liên tiếp nhiều chủ đề trong 1 conversation (như T1 hỏi 7 câu),
tổng lượt chat sẽ cao hơn (khoảng 4-6 lượt cho 1 conversation nhỏ).
```

**Insight bất ngờ — điều gì nhóm chỉ hiểu sau khi đóng vai?**

```text
- Tourist thường hỏi nhiều intent trong 1 conversation (info + booking + safety)
- Câu hỏi về điểm đến chiếm ~60% — đây là core use case chính
- Booking thường cần chuyển sang sales, không bot nào tự đặt được
- Câu hỏi về safety (Grab, food, hospitals) rất quan trọng nhưng dễ trả lời
- Khiếu nại hiếm nhưng cần xử lý cẩn thận với manager
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Mỗi người trong nhóm đã viết ≥5 câu hỏi tourist
- [x] Đã gom + phân loại intent cho ≥10 câu (bảng trên: 22 câu)
- [x] Đã có phân bố intent % của nhóm (Guide 59%, Booking 23%, Visa 5%, Weather 9%, Khiếu nại 5%)
- [x] Có ít nhất 1 insight về cách tourist thật sự dùng chatbot

Xong → mở `01-base-flow.md`.
