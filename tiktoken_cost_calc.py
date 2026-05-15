import tiktoken

# ============================================================
# TIKTOKEN COST CALCULATOR — AI Product Economics Lab (D27)
# Tính token thực tế cho từng thành phần prompt và cost/conv
# ============================================================

# --- 1. Khởi tạo encoder ---
# GPT-5 và GPT-4.1 dùng tokenizer mới (o200k_base giống GPT-4o)
# Claude/DeepSeek/Gemini tokenizer khác, nhưng để so sánh công bằng
# ta dùng o200k_base cho tất cả (đây là estimate thực tế nhất)
enc = tiktoken.get_encoding("o200k_base")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

def count_tokens_chat(messages: list) -> int:
    """Đếm tokens cho format chat messages (OpenAI style)"""
    total = 0
    for msg in messages:
        # Mỗi message thêm ~4 tokens (role + delimiters)
        total += 4
        total += count_tokens(msg.get("content", ""))
    # Thêm ~3 tokens cho assistant priming
    total += 3
    return total

# --- 2. Định nghĩa các thành phần prompt ---

SYSTEM_PROMPT = """You are a helpful travel assistant for a Vietnam-based travel agency.
Your role is to answer questions about destinations, visa policies, weather, food,
transportation, and culture. You have access to a knowledge base of travel articles.
If the user asks about booking tours or making a reservation, politely hand them off
to a human sales representative. If they have a complaint, escalate to a manager.
Always be friendly, concise, and accurate."""

# Các câu hỏi thực tế từ user-journey.md ( Tourist #1 — Nguyễn Hữu Quang )
USER_MESSAGES = [
    "Hi! I'm planning a trip to Vietnam for 4 people in July. Is it a good time to visit or will it rain all day?",
    "We really want to see Ha Long Bay. Do you have any overnight cruise packages that are kid-friendly?",
    "How does the e-visa process work for US citizens? Can your agency help me with that?",
    "I've heard a lot about street food in Hanoi, but I'm worried about stomach issues. Are there any 'safe' food tours?",
    "What is the best way to travel from Da Nang to Hoi An? Is it easy to catch a taxi?",
    "Can you recommend a 5-star hotel near the French Quarter in Hanoi?",
    "Is it safe to use Grab at night in Vietnam?"
]

# Các câu trả lời mẫu (assistant responses)
ASSISTANT_RESPONSES = [
    "July is actually a great time to visit northern Vietnam like Hanoi and Ha Long Bay! It's summer with warm temperatures around 30-35°C. However, central Vietnam (Da Nang, Hoi An) can be quite hot. The rainy season in the south (Ho Chi Minh City) typically starts around May-June, but July showers are usually short afternoon bursts rather than all-day rain. I'd recommend packing light rain gear just in case!",
    "Absolutely! Ha Long Bay is fantastic for families. Several cruise operators offer family-friendly overnight packages with connecting rooms, kids' activities, and early dinner options. Popular choices include Paradise Elegance and Genesis Regal. Would you like me to connect you with our sales team for specific pricing and availability?",
    "US citizens can apply for a 90-day e-visa through Vietnam's official immigration portal. The fee is $25 and processing typically takes 3 business days. You'll need a passport valid for at least 6 months and a digital photo. While I can guide you through the process, we don't handle visa applications directly — but I can recommend trusted visa agents if you'd like!",
    "Great question! Hanoi street food is amazing, and yes, there are guided food tours designed with hygiene in mind. Companies like Hanoi Foodie Tours and Backstreet Academy take you to vetted vendors with clean food handling practices. I'd also recommend starting with cooked dishes like bun cha or banh mi before trying raw items like goi cuon.",
    "The best way is by private car or Grab! The distance is only about 30km (45 minutes). A taxi from Da Nang airport costs around 300,000-400,000 VND ($12-16). Grab is reliable and usually cheaper. You can also take the local bus for about 20,000 VND but it's less comfortable with luggage.",
    "The French Quarter (Hoan Kiem area) has excellent 5-star options! Top picks: Hotel Metropole Hanoi (historic luxury, ~$250/night), Peridot Grand Hotel (boutique, ~$120/night), and Lotte Hotel Hanoi (modern, ~$150/night with city views). All are within 5 minutes walk of Hoan Kiem Lake. Shall I connect you with sales for booking?",
    "Yes, Grab is generally very safe in Vietnam, even at night! It's the most trusted ride-hailing app here. Drivers are registered and tracked. Just make sure to verify the license plate before getting in. In major cities like Hanoi and Ho Chi Minh City, Grab bike and car operate 24/7. I'd still recommend staying alert as you would anywhere, but most tourists find it very convenient and safe."
]

# RAG chunks mẫu (top-5 chunks)
RAG_CHUNKS = [
    "Vietnam has a tropical monsoon climate. The north experiences four seasons with cool winters (Dec-Feb) and hot summers (May-Aug). Central Vietnam has a dry season (Feb-Aug) and wet season (Sep-Jan). The south has two seasons: wet (May-Nov) and dry (Dec-Apr).",
    "Ha Long Bay, a UNESCO World Heritage site, features thousands of limestone karsts rising from emerald waters. Overnight cruises range from budget ($80/person) to luxury ($300+/person). Family-friendly options include Paradise Elegance, Genesis Regal, and Stella Maris with connecting cabins.",
    "Vietnam offers e-visas for citizens of 80+ countries including the US, UK, Australia, and EU. The standard e-visa costs $25, valid for 90 days single entry. Processing takes 3 working days. Requirements: passport valid 6+ months, digital photo (4x6cm), and application via the official Vietnam Immigration portal.",
    "Hanoi is Vietnam's street food capital. Must-try dishes: pho (beef noodle soup), bun cha (grilled pork with noodles), banh mi (baguette sandwich), and ca phe trung (egg coffee). Popular food tour areas: Old Quarter, French Quarter, and West Lake. Hygiene-conscious travelers should choose vendors with high turnover.",
    "Transportation in Vietnam: Domestic flights (Vietnam Airlines, VietJet, Bamboo Airways) connect major cities. Open Bus Tour and The Sinh Tourist offer reliable sleeper buses. Trains run from Hanoi to Ho Chi Minh City (SE1/SE3, ~30 hours). For short distances, Grab and local taxis are widely available."
]

# Web search results mẫu (khi bật)
WEB_SEARCH_RESULT = """Current weather forecast (May 2026):
Hanoi: 28-35°C, partly cloudy, 60% humidity. No rain expected this week.
Da Nang: 30-38°C, sunny, high UV index. Beach conditions excellent.
Ho Chi Minh City: 26-33°C, afternoon showers possible (30% chance).

Visa update (May 2026): Vietnam has extended e-visa validity to 90 days for all eligible countries.
Tourists can now apply for multiple-entry e-visas starting June 1, 2026.

Hotel rates (May 2026): Hanoi Old Quarter 4-star $60-120/night, 5-star $150-300/night.
Da Nang beachfront resorts $80-250/night depending on season."""

# --- 3. Tính token cho từng thành phần ---

print("=" * 70)
print("TIKTOKEN TOKEN COUNT — ACTUAL PROMPT COMPONENTS")
print("Tokenizer: o200k_base (GPT-4o / GPT-4.1 / GPT-5 family)")
print("=" * 70)

# System prompt
sys_tok = count_tokens(SYSTEM_PROMPT)
print(f"\nSystem Prompt: {sys_tok} tokens")
print(f"  (Reference card estimate: 500 tokens)")

# User messages
print(f"\nUser Messages (7 turns):")
user_toks = []
for i, msg in enumerate(USER_MESSAGES, 1):
    t = count_tokens(msg)
    user_toks.append(t)
    print(f"  Turn {i}: {t:3d} tokens — '{msg[:50]}...'")
print(f"  Average: {sum(user_toks)/len(user_toks):.1f} tokens")
print(f"  (Reference card estimate: 80 tokens)")

# Assistant responses
print(f"\nAssistant Responses (7 turns):")
resp_toks = []
for i, resp in enumerate(ASSISTANT_RESPONSES, 1):
    t = count_tokens(resp)
    resp_toks.append(t)
    print(f"  Turn {i}: {t:4d} tokens — '{resp[:50]}...'")
print(f"  Average: {sum(resp_toks)/len(resp_toks):.1f} tokens")
print(f"  (Reference card estimate: 180 tokens)")

# RAG chunks
print(f"\nRAG Top-5 Chunks:")
rag_total = 0
for i, chunk in enumerate(RAG_CHUNKS, 1):
    t = count_tokens(chunk)
    rag_total += t
    print(f"  Chunk {i}: {t:4d} tokens — '{chunk[:50]}...'")
print(f"  Total RAG: {rag_total} tokens")
print(f"  (Reference card estimate: 1,250 tokens)")

# Web search
web_tok = count_tokens(WEB_SEARCH_RESULT)
print(f"\nWeb Search Results: {web_tok} tokens")
print(f"  (Reference card estimate: 800 tokens)")

# --- 4. Tính history tokens ---
print(f"\nHistory Tokens (per prior turn = user + assistant):")
avg_user = sum(user_toks) / len(user_toks)
avg_resp = sum(resp_toks) / len(resp_toks)
avg_turn = avg_user + avg_resp
print(f"  Avg user msg: {avg_user:.0f} tokens")
print(f"  Avg assistant: {avg_resp:.0f} tokens")
print(f"  1 prior turn: {avg_turn:.0f} tokens")
print(f"  (Reference card estimate: 260 tokens)")

# --- 5. Tính cost cho từng config ---

print("\n" + "=" * 70)
print("COST CALCULATION BY CONFIG (using ACTUAL token counts)")
print("=" * 70)

# Pricing (per 1M tokens)
PRICING = {
    "gpt5_nano":      {"in": 0.05,  "out": 0.40},
    "gpt4_1_nano":    {"in": 0.10,  "out": 0.40},
    "gemini_31_fl":   {"in": 0.25,  "out": 1.50},  # Gemini 3.1 Flash-Lite
    "gemini_25_fl":   {"in": 0.10,  "out": 0.40},
    "deepseek_v4p":   {"in": 0.435, "out": 0.87},  # Promo pricing
    "gpt5_5":         {"in": 5.00,  "out": 30.00},
}

WEB_API_COST = 0.008  # Tavily per query

def calc_config_cost(name, model_key, web_mode, history_mode, turns=4):
    """
    web_mode: "off", "selective", "broad"
    history_mode: "last3", "last5", "full", "summarize5"
    """
    p = PRICING[model_key]

    # Classifier cost (1 LLM call per conv, ~170 tokens)
    # Dùng cùng model hoặc keyword. Với nano thì ~170 tokens
    classifier_input = 170
    classifier_cost = (classifier_input * p["in"]) / 1_000_000

    total_cost = classifier_cost

    for turn in range(1, turns + 1):
        # History
        if history_mode == "last3":
            hist_tok = min(turn - 1, 3) * avg_turn
        elif history_mode == "last5":
            hist_tok = min(turn - 1, 5) * avg_turn
        elif history_mode == "full":
            hist_tok = (turn - 1) * avg_turn
        elif history_mode == "summarize5":
            # Mỗi 5 turns tóm tắt 1 lần (~150 tokens cố định)
            if turn <= 5:
                hist_tok = (turn - 1) * avg_turn
            else:
                hist_tok = 150  # summary
        else:
            hist_tok = 0

        # Input components
        input_tok = sys_tok + hist_tok + rag_total + avg_user

        # Web search (selective = Visa/Weather only; broad = all AI-served turns)
        web_on = False
        if web_mode == "broad":
            web_on = True
        elif web_mode == "selective":
            # Giả định 35% turns là Visa/Weather
            web_on = (turn % 3 == 0)  # approx

        if web_on:
            input_tok += web_tok
            total_cost += WEB_API_COST

        # Model cost
        output_tok = avg_resp
        turn_cost = (input_tok * p["in"] + output_tok * p["out"]) / 1_000_000
        total_cost += turn_cost

    return total_cost

# Tính cho 4 configs
configs = [
    ("Budget Bot", "gpt5_nano", "off", "last3", 4),
    ("Budget Bot", "gpt5_nano", "off", "last3", 7),
    ("Premium Concierge", "gpt5_5", "broad", "full", 4),
    ("Premium Concierge", "gpt5_5", "broad", "full", 7),
    ("Smart Mix (Guide)", "gpt5_nano", "off", "last5", 4),
    ("Smart Mix (Guide)", "gpt5_nano", "off", "last5", 7),
    ("Smart Mix (Visa/Weather)", "gemini_31_fl", "selective", "last5", 4),
    ("Smart Mix (Visa/Weather)", "gemini_31_fl", "selective", "last5", 7),
    ("Deep Value", "deepseek_v4p", "selective", "summarize5", 4),
    ("Deep Value", "deepseek_v4p", "selective", "summarize5", 7),
]

print(f"\n{'Config':<30s} {'Turns':<6s} {'Cost/Conv':<12s} {'Monthly (300d)':<15s} {'Monthly (1200d)':<15s}")
print("-" * 90)

# Tính weighted avg cho Smart Mix
for name, model, web, hist, t in configs:
    cost = calc_config_cost(name, model, web, hist, t)

    # Monthly
    if "Smart Mix" in name and "Guide" in name:
        # Guide 59% volume
        continue
    elif "Smart Mix" in name and "Visa" in name:
        continue

    monthly_300 = cost * 300 * 30
    monthly_1200 = cost * 1200 * 30

    marker = ""
    if t == 7:
        marker = " (Scenario B)"
    else:
        marker = " (Scenario A)"

    print(f"{name:<30s} {t:<6d} ${cost:<10.6f} ${monthly_300:<13.2f} ${monthly_1200:<13.2f}{marker}")

# --- 6. Weighted Smart Mix ---
print("\n" + "-" * 90)
print("SMART MIX — Weighted Average (Guide 59%, Visa 25%, Weather 10%, Handoff 6%)")
print("-" * 90)

for turns in [4, 7]:
    guide_cost = calc_config_cost("", "gpt5_nano", "off", "last5", turns)
    visa_cost = calc_config_cost("", "gemini_31_fl", "selective", "last5", turns)
    weather_cost = calc_config_cost("", "gemini_31_fl", "selective", "last5", turns)
    # Booking/Complaint handoff: only classifier cost (using nano)
    handoff_cost = (170 * PRICING["gpt5_nano"]["in"]) / 1_000_000

    weighted = 0.59 * guide_cost + 0.25 * visa_cost + 0.10 * weather_cost + 0.06 * handoff_cost

    monthly_300 = weighted * 300 * 30
    monthly_1200 = weighted * 1200 * 30

    print(f"  Turns {turns}: Cost/Conv = ${weighted:.6f}")
    print(f"           Monthly @300/day  = ${monthly_300:.2f}")
    print(f"           Monthly @1200/day = ${monthly_1200:.2f}")
    print(f"           Re hon human: {0.50/weighted:.1f}x")
    print()

# --- 7. Deep Value weighted ---
print("-" * 90)
print("DEEP VALUE — Weighted (Guide 59%, Visa 25%, Weather 10%, Handoff 6%)")
print("-" * 90)

for turns in [4, 7]:
    guide_cost = calc_config_cost("", "deepseek_v4p", "selective", "summarize5", turns)
    visa_cost = calc_config_cost("", "deepseek_v4p", "selective", "summarize5", turns)
    weather_cost = calc_config_cost("", "deepseek_v4p", "selective", "summarize5", turns)
    handoff_cost = (170 * PRICING["deepseek_v4p"]["in"]) / 1_000_000

    weighted = 0.59 * guide_cost + 0.25 * visa_cost + 0.10 * weather_cost + 0.06 * handoff_cost

    monthly_300 = weighted * 300 * 30
    monthly_1200 = weighted * 1200 * 30

    print(f"  Turns {turns}: Cost/Conv = ${weighted:.6f}")
    print(f"           Monthly @300/day  = ${monthly_300:.2f}")
    print(f"           Monthly @1200/day = ${monthly_1200:.2f}")
    print(f"           Re hon human: {0.50/weighted:.1f}x")
    print()

print("=" * 70)
print("NOTE: Compare with Reference card estimates in comments")
print("=" * 70)
