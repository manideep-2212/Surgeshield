#!/usr/bin/env python3
"""
Generate the SurgeShield Architecture PowerPoint Presentation (20 Slides).
Story-driven, visually consistent, architectural narrative with strict color semantics:
  RED    -> Problem / Risk / Failure / Bottleneck
  BLUE   -> System / Technology / Normal Flow
  GREEN  -> Solution / Success / Protected State
  PURPLE -> SurgeShield Unique Capabilities / Scaling / Intelligence
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# CONSTANT SEMANTIC PALETTE
# ---------------------------------------------------------
# Neutral Backgrounds
LIGHT_BG = RGBColor(248, 250, 252)     # Slate 50
CARD_WHITE = RGBColor(255, 255, 255)   # Pure White
CARD_BORDER = RGBColor(226, 232, 240)  # Slate 200

DARK_BG = RGBColor(15, 23, 42)         # Slate 900
DARK_CARD = RGBColor(30, 41, 59)       # Slate 800
DARK_BORDER = RGBColor(51, 65, 85)     # Slate 700

# Typography
TEXT_DARK = RGBColor(15, 23, 42)       # Slate 900
TEXT_BODY = RGBColor(51, 65, 85)       # Slate 700
TEXT_MUTED = RGBColor(100, 116, 139)   # Slate 500
TEXT_LIGHT = RGBColor(255, 255, 255)   # White
TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # Slate 400

# Semantic Colors
# RED: Problem / Failure / Vulnerability / Bottleneck
RED_COLOR = RGBColor(220, 38, 38)      # #DC2626 Red 600
RED_BG = RGBColor(254, 242, 242)       # #FEF2F2 Red 50
RED_BORDER = RGBColor(254, 202, 202)   # #FECACA Red 200

# BLUE: System / Technology / Architecture / Normal Flow
BLUE_COLOR = RGBColor(37, 99, 235)     # #2563EB Blue 600
BLUE_BG = RGBColor(239, 246, 255)      # #EFF6FF Blue 50
BLUE_BORDER = RGBColor(191, 219, 254)  # #BFDBFE Blue 200

# GREEN: Solution / Success / Protected State / Zero Overbooking
GREEN_COLOR = RGBColor(22, 163, 74)    # #16A34A Green 600
GREEN_BG = RGBColor(240, 253, 244)     # #F0FDF4 Green 50
GREEN_BORDER = RGBColor(187, 247, 208) # #BBF7D0 Green 200

# PURPLE: SurgeShield Unique / Intelligence / Scaling / Core Accents
PURPLE_COLOR = RGBColor(99, 91, 255)   # #635BFF Indigo
PURPLE_BG = RGBColor(245, 243, 255)    # #F5F3FF Purple 50
PURPLE_BORDER = RGBColor(221, 214, 254)# #DDD6FE Purple 200

FONT_NAME = "Segoe UI"

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title, category, slide_num, total_slides=20, is_dark=False):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = FONT_NAME
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = PURPLE_COLOR if not is_dark else RGBColor(165, 180, 252)

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.5), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_NAME
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK

    # Slide Counter
    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.55), Inches(1.0), Inches(0.4))
    tf_num = num_box.text_frame
    tf_num.word_wrap = True
    tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{slide_num:02d} / {total_slides:02d}"
    p_num.font.name = FONT_NAME
    p_num.font.size = Pt(12)
    p_num.font.bold = True
    p_num.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_badge(slide, left, top, width, height, text, bg_color, text_color, font_size=9):
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_NAME
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return badge

def style_para(para, text, font_size=12, bold=False, color=TEXT_BODY, space_after=4, align=PP_ALIGN.LEFT):
    para.text = text
    para.alignment = align
    para.font.name = FONT_NAME
    para.font.size = Pt(font_size)
    para.font.bold = bold
    para.font.color.rgb = color
    para.space_after = Pt(space_after)

# ---------------------------------------------------------
# SLIDES 1 TO 20 IMPLEMENTATION
# ---------------------------------------------------------

def build_slide_1(prs):
    # Slide 1: Title Slide (Dark Theme with Semantic Legend)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, DARK_BG)

    add_badge(slide, Inches(0.8), Inches(0.8), Inches(3.8), Inches(0.36),
              "OFFICIAL P1 HACKATHON SOLUTION", PURPLE_COLOR, TEXT_LIGHT, 11)

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    style_para(p, "SurgeShield: Resilient, Self-Scaling Web Platform", 32, True, TEXT_LIGHT, 8)
    p2 = tf.add_paragraph()
    style_para(p2, "Architecting Zero-Downtime, High-Concurrency Event Registration Under Flash-Crowd Surges", 17, False, RGBColor(203, 213, 225), 0)

    # Consistent Color Legend Box (The audience knows the code immediately)
    add_card(slide, Inches(0.8), Inches(3.1), Inches(11.73), Inches(0.85), DARK_CARD, DARK_BORDER)
    tb_leg = slide.shapes.add_textbox(Inches(1.0), Inches(3.15), Inches(11.33), Inches(0.75))
    tf_leg = tb_leg.text_frame
    tf_leg.word_wrap = True
    p_leg_title = tf_leg.paragraphs[0]
    style_para(p_leg_title, "PRESENTATION VISUAL ENCODING & ARCHITECTURAL SEMANTICS:", 10, True, TEXT_LIGHT_MUTED, 4)

    # 4 Colored Pill Legend Items
    add_badge(slide, Inches(1.0), Inches(3.5), Inches(2.6), Inches(0.32), "RED = Failure / Risk / Bottleneck", RED_COLOR, TEXT_LIGHT, 9)
    add_badge(slide, Inches(3.8), Inches(3.5), Inches(2.6), Inches(0.32), "BLUE = System / Technology Flow", BLUE_COLOR, TEXT_LIGHT, 9)
    add_badge(slide, Inches(6.6), Inches(3.5), Inches(2.6), Inches(0.32), "GREEN = Protected State / Solution", GREEN_COLOR, TEXT_LIGHT, 9)
    add_badge(slide, Inches(9.4), Inches(3.5), Inches(2.6), Inches(0.32), "PURPLE = SurgeShield Capabilities", PURPLE_COLOR, TEXT_LIGHT, 9)

    # 4 Core Architectural Pillar Cards
    pillars = [
        ("CONCURRENCY CONTROL", "PostgreSQL SELECT FOR UPDATE pessimistic row-locking eliminates double-booking across distributed nodes.", GREEN_COLOR),
        ("DUAL RATE LIMITING", "Edge Nginx burst control (20 r/s) + Express application limiter (300 req/m) prevent server collapse.", RED_COLOR),
        ("ASYNC DECOUPLING", "BullMQ + Redis 7 + Outbox pattern offloads slow notifications (<15ms API response latency).", BLUE_COLOR),
        ("SELF-HEALING CLUSTER", "Multi-node Nginx round-robin, automated worker crash recovery, and real-time health detection.", PURPLE_COLOR)
    ]
    card_w = Inches(2.72)
    card_h = Inches(2.0)
    card_y = Inches(4.2)
    for i, (p_title, p_desc, accent) in enumerate(pillars):
        x = Inches(0.8 + i * 2.98)
        add_card(slide, x, card_y, card_w, card_h, DARK_CARD, DARK_BORDER)
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), card_y + Inches(0.18), Inches(0.6), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb_p = slide.shapes.add_textbox(x + Inches(0.2), card_y + Inches(0.35), card_w - Inches(0.4), card_h - Inches(0.45))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        p_t = tf_p.paragraphs[0]
        style_para(p_t, p_title, 12, True, TEXT_LIGHT, 5)
        p_d = tf_p.add_paragraph()
        style_para(p_d, p_desc, 10, False, TEXT_LIGHT_MUTED, 0)

    # Footer
    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.4))
    tf_foot = tb_foot.text_frame
    p_f = tf_foot.paragraphs[0]
    style_para(p_f, "SurgeShield Engineering Team  |  Target Audience: Mentors, Evaluators & System Architects", 11, False, TEXT_LIGHT_MUTED, 0)

def build_slide_2(prs):
    # Slide 2: Real-World Story / Relatable Scenario
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "The Booking Dilemma: Resource + Time + Multiple Users", "Relatable Real-World Scenario", 2)

    # Top Context Card
    add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(1.0), BLUE_BG, BLUE_BORDER)
    tb_top = slide.shapes.add_textbox(Inches(1.0), Inches(1.48), Inches(11.33), Inches(0.85))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    p_t = tf_top.paragraphs[0]
    style_para(p_t, "Imagine Booking a Popular Train, Bus, or Movie Ticket Online:", 13, True, BLUE_COLOR, 3)
    p_t2 = tf_top.add_paragraph()
    style_para(p_t2, "You find the perfect journey. Only a few seats remain. You select a seat and proceed toward payment. The system temporarily reserves the seat for you. But what happens if you don't complete the payment? After the hold period expires, the seat must safely release so another passenger can book it.", 11, False, TEXT_DARK, 0)

    # 4 Visual Story Steps (Horizontal Cards)
    steps = [
        ("1. SELECT SEAT", "User discovers the last remaining seat and clicks 'Book'.", BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("2. TEMPORARY HOLD", "System locks the seat for 10 minutes to allow payment entry.", PURPLE_BG, PURPLE_COLOR, PURPLE_BORDER),
        ("3. PAYMENT DROPS", "User abandons session or mobile connection stutters.", RED_BG, RED_COLOR, RED_BORDER),
        ("4. SEAT RELEASED", "Hold timer expires; seat returns to pool for other buyers.", GREEN_BG, GREEN_COLOR, GREEN_BORDER)
    ]
    card_w = Inches(2.75)
    card_h = Inches(2.5)
    for i, (stitle, sdesc, bg, accent, border) in enumerate(steps):
        x = Inches(0.8 + i * 2.99)
        add_card(slide, x, Inches(2.65), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.15), Inches(2.8), card_w - Inches(0.3), Inches(0.35), stitle, accent, TEXT_LIGHT, 11)

        tb_s = slide.shapes.add_textbox(x + Inches(0.2), Inches(3.3), card_w - Inches(0.4), card_h - Inches(0.8))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_sd = tf_s.paragraphs[0]
        style_para(p_sd, sdesc, 11, False, TEXT_BODY, 0)

    # Bottom Transition Banner (The Bridge to P1)
    banner = add_card(slide, Inches(0.8), Inches(5.4), Inches(11.73), Inches(1.3), PURPLE_BG, PURPLE_COLOR)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.33), Inches(1.1))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    style_para(p_b, "The Core Distributed Systems Principle:", 13, True, PURPLE_COLOR, 3)
    p_b2 = tf_b.add_paragraph()
    style_para(p_b2, "Managing RESOURCE + TIME + MULTIPLE USERS is challenging for a single ticket. Now transition to our problem: Imagine thousands of users trying to register for a high-demand event at the exact same millisecond. That is where systems break, and that is why we built SurgeShield.", 12, False, TEXT_DARK, 0)

def build_slide_3(prs):
    # Slide 3: P1 Problem Statement: The Traffic Surge Challenge
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "From Normal Traffic to Sudden Avalanche: The Surge Problem", "Official P1 Problem Statement", 3)

    # Left Card: Normal Baseline Traffic (BLUE)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(5.65), Inches(3.7), BLUE_BG, BLUE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.6), Inches(5.15), Inches(3.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "NORMAL TRAFFIC BASELINE", 15, True, BLUE_COLOR, 8)

    normal_items = [
        ("Predictable Traffic Load", "Approximately 100 concurrent users browsing events at leisurely intervals."),
        ("Normal Server Utilization", "Single application node comfortably runs at 10-15% CPU and memory."),
        ("Fast Response Latency", "API responds in < 25ms; database connection pool operates well below limits."),
        ("The Illusion of Stability", "\"Everything works fine during normal traffic, but the real challenge begins when traffic suddenly spikes.\"" )
    ]
    for title, desc in normal_items:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"• {title}:", 11, True, BLUE_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, f"   {desc}", 10, False, TEXT_BODY, 5)

    # Right Card: Traffic Surge Avalanche (RED)
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.65), Inches(3.7), RED_BG, RED_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(1.6), Inches(5.15), Inches(3.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "TICKETING OPENS: FLASH-CROWD SURGE", 15, True, RED_COLOR, 8)

    surge_items = [
        ("Instantaneous 100x Explosion", "Traffic spikes from 100 to 10,000 requests in under 3 seconds."),
        ("Extreme Contention for Final Seats", "Hundreds of users hit 'Submit' at the exact same millisecond for the last 5 seats."),
        ("Server & Database Choke", "Database connection pool exhausts instantly; CPU spikes to 100% capacity."),
        ("Cascading Service Meltdown", "HTTP 504 gateway timeouts, dropped network packets, and complete service freeze.")
    ]
    for title, desc in surge_items:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"• {title}:", 11, True, RED_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, f"   {desc}", 10, False, TEXT_BODY, 5)

    # Bottom Visual Cascade Flow
    add_card(slide, Inches(0.8), Inches(5.3), Inches(11.73), Inches(1.5), CARD_WHITE, CARD_BORDER)
    tb_c = slide.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.33), Inches(0.4))
    tf_c = tb_c.text_frame
    p_ct = tf_c.paragraphs[0]
    style_para(p_ct, "THE UNPROTECTED MELTDOWN CASCADE:", 11, True, RED_COLOR, 0)

    # 5 Horizontal Flow Badges
    stages = [
        ("Traffic Surge", RED_BG, RED_COLOR),
        ("Server Pressure", RED_BG, RED_COLOR),
        ("High Latency", RED_BG, RED_COLOR),
        ("Failed Requests", RED_BG, RED_COLOR),
        ("Total Outage ❌", RED_COLOR, TEXT_LIGHT)
    ]
    step_w = Inches(2.0)
    for i, (name, bg, fg) in enumerate(stages):
        x = Inches(1.0 + i * 2.3)
        add_badge(slide, x, Inches(5.95), step_w, Inches(0.5), name, bg, fg, 11)
        if i < 4:
            arrow_tb = slide.shapes.add_textbox(x + step_w, Inches(6.0), Inches(0.3), Inches(0.4))
            tf_arr = arrow_tb.text_frame
            p_a = tf_arr.paragraphs[0]
            style_para(p_a, "→", 16, True, TEXT_MUTED, 0, PP_ALIGN.CENTER)

def build_slide_4(prs):
    # Slide 4: What Happens During a Traffic Surge? (Failure Mode Analysis)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "The Failure Chain: Why Naive Architectures Break", "Technical Risk & Failure Analysis", 4)

    failures = [
        ("1. DB Connection Exhaustion", "PostgreSQL pool limit reached (e.g. 20 conns). Hundreds of concurrent requests queue up, stall, and drop with HTTP 500.", RED_COLOR, RED_BG, RED_BORDER),
        ("2. Node.js Event Loop Congestion", "Synchronous I/O or heavy operations block the single-threaded event loop, preventing healthy health probes from responding.", RED_COLOR, RED_BG, RED_BORDER),
        ("3. Memory Spikes & V8 OOM Crashes", "Unbuffered incoming requests pile up in memory buffers faster than they can be served, triggering Node Out-Of-Memory termination.", RED_COLOR, RED_BG, RED_BORDER),
        ("4. Cascading 3rd-Party Timeouts", "Calling external email/SMS confirmation services synchronously (taking 1-2s) holds HTTP worker threads hostage.", RED_COLOR, RED_BG, RED_BORDER)
    ]

    card_w = Inches(5.65)
    card_h = Inches(2.2)
    for i, (title, desc, accent, bg, border) in enumerate(failures):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.08)
        y = Inches(1.5 + row * 2.45)
        add_card(slide, x, y, card_w, card_h, bg, border)

        tb = slide.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), card_w - Inches(0.5), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        style_para(p_t, title, 14, True, accent, 8)
        p_d = tf.add_paragraph()
        style_para(p_d, desc, 11, False, TEXT_BODY, 0)

    # Bottom Summary Callout
    banner = add_card(slide, Inches(0.8), Inches(6.2), Inches(11.73), Inches(0.7), CARD_WHITE, CARD_BORDER)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.33), Inches(0.6))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    style_para(p_b, "Key Architectural Insight: Web platforms do not fail because of bad code; they fail because unbuffered traffic hits unprotected state.", 11, True, RED_COLOR, 0, PP_ALIGN.CENTER)

def build_slide_5(prs):
    # Slide 5: High-Level SurgeShield Architecture (EARLY SYSTEM DESIGN!)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "SurgeShield End-to-End Architecture: Built for Resilience", "Early System Design (Explainable in 2 Minutes)", 5)

    # Main Architecture Canvas
    add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(4.5), CARD_WHITE, CARD_BORDER)

    # 1. Users Block
    add_card(slide, Inches(1.1), Inches(1.6), Inches(2.2), Inches(4.1), PURPLE_BG, PURPLE_BORDER)
    tb_u = slide.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(2.0), Inches(3.8))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True
    p_u = tf_u.paragraphs[0]
    style_para(p_u, "USERS & CLIENTS", 13, True, PURPLE_COLOR, 8, PP_ALIGN.CENTER)
    p_u1 = tf_u.add_paragraph()
    style_para(p_u1, "• Web Attendees\n• Event Organizers\n• Stress Test Generator\n  (25-50 burst requests)\n\nFeatures:\n• Idempotency UUIDs\n• JWT Token Auth\n• Seat Visualizer", 10, False, TEXT_BODY, 0)

    # Arrow 1 -> NGINX
    add_badge(slide, Inches(3.45), Inches(3.4), Inches(0.6), Inches(0.3), "HTTP", PURPLE_COLOR, TEXT_LIGHT, 9)

    # 2. NGINX Reverse Proxy
    add_card(slide, Inches(4.2), Inches(1.6), Inches(2.3), Inches(4.1), BLUE_BG, BLUE_BORDER)
    tb_ng = slide.shapes.add_textbox(Inches(4.3), Inches(1.75), Inches(2.1), Inches(3.8))
    tf_ng = tb_ng.text_frame
    tf_ng.word_wrap = True
    p_ng = tf_ng.paragraphs[0]
    style_para(p_ng, "NGINX GATEWAY", 13, True, BLUE_COLOR, 8, PP_ALIGN.CENTER)
    p_ng1 = tf_ng.add_paragraph()
    style_para(p_ng1, "Port: 8080\n\n• L7 Round-Robin LB\n• Edge Rate Limiting:\n  limit_req (20 r/s)\n• Burst buffer: 40\n• Upstream Failover:\n  max_fails=2, 5s\n• Static Asset Host", 10, False, TEXT_BODY, 0)

    # Arrow 2 -> API Cluster
    add_badge(slide, Inches(6.65), Inches(3.4), Inches(0.6), Inches(0.3), "PROXY", BLUE_COLOR, TEXT_LIGHT, 9)

    # 3. 3x API Cluster
    add_card(slide, Inches(7.4), Inches(1.6), Inches(2.3), Inches(4.1), PURPLE_BG, PURPLE_BORDER)
    tb_api = slide.shapes.add_textbox(Inches(7.5), Inches(1.75), Inches(2.1), Inches(3.8))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True
    p_api = tf_api.paragraphs[0]
    style_para(p_api, "API CLUSTER (3x)", 13, True, PURPLE_COLOR, 8, PP_ALIGN.CENTER)
    p_api1 = tf_api.add_paragraph()
    style_para(p_api1, "App 1 | App 2 | App 3\n(Port 3000 Stateless)\n\n• JWT Verification\n• App Rate Limiting\n• Concurrency Gating\n• Outbox Enqueue\n• servedBy Header", 10, False, TEXT_BODY, 0)

    # Arrow 3 -> Data Tier
    add_badge(slide, Inches(9.85), Inches(3.4), Inches(0.6), Inches(0.3), "DATA", GREEN_COLOR, TEXT_LIGHT, 9)

    # 4. Data & Worker Tier
    add_card(slide, Inches(10.6), Inches(1.6), Inches(1.75), Inches(4.1), GREEN_BG, GREEN_BORDER)
    tb_db = slide.shapes.add_textbox(Inches(10.65), Inches(1.75), Inches(1.65), Inches(3.8))
    tf_db = tb_db.text_frame
    tf_db.word_wrap = True
    p_db = tf_db.paragraphs[0]
    style_para(p_db, "DATA & QUEUE", 12, True, GREEN_COLOR, 6, PP_ALIGN.CENTER)
    p_db1 = tf_db.add_paragraph()
    style_para(p_db1, "PostgreSQL 16:\n• FOR UPDATE Lock\n• Check Invariants\n• Outbox Records\n\nRedis 7 & BullMQ:\n• 5s Catalog Cache\n• Job Queue (AOF)\n\nWorker Service:\n• Async Consumer", 9.5, False, TEXT_BODY, 0)

    # Bottom Quick-Map Legend (Where everything lives)
    legend_bar = add_card(slide, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.85), DARK_BG, DARK_BORDER)
    tb_leg = slide.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.33), Inches(0.75))
    tf_leg = tb_leg.text_frame
    tf_leg.word_wrap = True
    p_l1 = tf_leg.paragraphs[0]
    style_para(p_l1, "WHERE KEY SURGESHIELD CAPABILITIES LIVE IN THE ARCHITECTURE:", 10, True, RGBColor(165, 180, 252), 2)
    p_l2 = tf_leg.add_paragraph()
    style_para(p_l2, "• Load Balancing: Nginx (:8080)   • Concurrency Control: PostgreSQL Row Lock   • Idempotency: API Pre-check + DB Unique\n• Async Processing: BullMQ + Redis + Worker   • Health Probes: /health (Composite)   • Scaling: Queue-Depth Virtual Pool", 10, False, TEXT_LIGHT, 0)

def build_slide_6(prs):
    # Slide 6: Problem -> Solution Engineering Framework
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Systematic Engineering: How SurgeShield Solves Challenges", "Our Engineering Methodology", 6)

    # Introduction Card
    add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(0.85), BLUE_BG, BLUE_BORDER)
    tb_top = slide.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.33), Inches(0.75))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    p_t = tf_top.paragraphs[0]
    style_para(p_t, "The Repeatable 5-Step Discipline Applied to Every Failure Mode:", 13, True, BLUE_COLOR, 2)
    p_t2 = tf_top.add_paragraph()
    style_para(p_t2, "Rather than deploying ad-hoc fixes, SurgeShield isolates each high-traffic vulnerability through this systematic engineering framework. The next slides walk through each problem using this exact flow.", 11, False, TEXT_DARK, 0)

    # 5 Sequential Cards
    steps = [
        ("1. PROBLEM", "The real-world failure mode or bottleneck that causes customer complaints.", RED_BG, RED_COLOR, RED_BORDER),
        ("2. WHY IT HAPPENS", "The root-cause flaw in naive architectures (e.g. read-modify-write races).", RED_BG, RED_COLOR, RED_BORDER),
        ("3. SURGESHIELD SOLUTION", "The conceptual engineering pattern that guarantees resilience.", GREEN_BG, GREEN_COLOR, GREEN_BORDER),
        ("4. TECHNOLOGY USED", "The enterprise tool selected to enforce this solution (e.g. PostgreSQL).", BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("5. WHAT WE IMPLEMENTED", "The verified code, SQL migration, or config in our project.", PURPLE_BG, PURPLE_COLOR, PURPLE_BORDER)
    ]
    card_w = Inches(2.2)
    card_h = Inches(3.2)
    for i, (stitle, sdesc, bg, accent, border) in enumerate(steps):
        x = Inches(0.8 + i * 2.38)
        add_card(slide, x, Inches(2.45), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.1), Inches(2.6), card_w - Inches(0.2), Inches(0.35), stitle, accent, TEXT_LIGHT, 10)

        tb_s = slide.shapes.add_textbox(x + Inches(0.15), Inches(3.1), card_w - Inches(0.3), card_h - Inches(0.8))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_sd = tf_s.paragraphs[0]
        style_para(p_sd, sdesc, 11, False, TEXT_BODY, 0)

    # Bottom Footer
    banner = add_card(slide, Inches(0.8), Inches(5.9), Inches(11.73), Inches(0.85), CARD_WHITE, CARD_BORDER)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.33), Inches(0.75))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    style_para(p_b, "Now, let us examine the 6 critical problems SurgeShield overcomes, starting with the most dangerous: Concurrency & Overbooking.", 12, True, PURPLE_COLOR, 0, PP_ALIGN.CENTER)

def build_slide_7(prs):
    # Slide 7: Problem 1 — Concurrency / Overbooking
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 1: Concurrency & Overbooking (The Race Condition)", "P1 Core Challenge: Zero Overbooking", 7)

    # Left Column: THE PROBLEM (RED)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(5.65), Inches(5.2), RED_BG, RED_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "THE CONCURRENCY HAZARD (NAIVE SYSTEM)", 14, True, RED_COLOR, 6)

    prob_desc = [
        ("The Scenario", "Only 2 seats remain. User A requests 2 seats. User B requests 2 seats. Both click 'Register' at the exact same millisecond."),
        ("Why It Happens", "Without database-level synchronization, both transactions execute:\n`SELECT available_seats FROM events WHERE id=1;`\nBoth read available = 2. Both checks (2 >= 2) evaluate to TRUE!"),
        ("The Result: Overbooking ❌", "User A executes: `UPDATE events SET available_seats = 0;`\nUser B executes: `UPDATE events SET available_seats = -2;`\n4 seats booked for 2 physical seats! Overbooking occurs, database constraint is violated, and customer trust is destroyed.")
    ]
    for title, desc in prob_desc:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"• {title}:", 11, True, RED_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 6)

    # Right Column: SURGESHIELD SOLUTION (GREEN)
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.65), Inches(5.2), GREEN_BG, GREEN_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "SURGESHIELD SOLUTION: SELECT ... FOR UPDATE", 14, True, GREEN_COLOR, 6)

    # Visual Lock Diagram inside right card
    lock_box = add_card(slide, Inches(7.13), Inches(2.1), Inches(5.15), Inches(1.2), CARD_WHITE, GREEN_BORDER)
    tb_lock = slide.shapes.add_textbox(Inches(7.2), Inches(2.15), Inches(5.0), Inches(1.1))
    tf_lock = tb_lock.text_frame
    tf_lock.word_wrap = True
    p_lk = tf_lock.paragraphs[0]
    style_para(p_lk, "VISUAL ROW-LOCKING PIPELINE:", 10, True, GREEN_COLOR, 2)
    p_lk1 = tf_lock.add_paragraph()
    style_para(p_lk1, "USER A ──────┐\n             ↓  Acquires Exclusive Row Lock\n        EVENT ROW 🔒 (PostgreSQL SELECT ... FOR UPDATE)\n             ↑  Blocked & Queued until User A Commits\nUSER B ──────┘", 10, True, TEXT_DARK, 0)

    sol_desc = [
        ("Strict Serialization", "User A enters transaction and locks the event row. User B is paused at the DB layer."),
        ("Clean Rejection (HTTP 409)", "User A books 2 seats (Remaining = 0). User B wakes up, reads updated seats = 0, and is cleanly rejected with HTTP 409!"),
        ("What We Implemented", "In `src/server.js`: Atomic `SELECT ... FOR UPDATE`, multi-ticket support (`quantity >= 1`), and `CHECK(available_seats >= 0)` constraint.")
    ]
    for title, desc in sol_desc:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"✓ {title}:", 11, True, GREEN_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 5)

def build_slide_8(prs):
    # Slide 8: Problem 2 — Duplicate Requests
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 2: Duplicate Requests & Network Retries", "Network Reliability & Idempotency", 8)

    # Left Column: THE PROBLEM (RED)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(5.65), Inches(5.2), RED_BG, RED_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "THE DUPLICATE SUBMISSION HAZARD", 14, True, RED_COLOR, 6)

    prob_desc = [
        ("The Story", "A user clicks 'Register'. The mobile network connection stutters or lags. Anxious, the user clicks 'Register' again. Or the browser/mobile network silently auto-retries the exact same HTTP request."),
        ("Why It Happens", "Without idempotency protection, the backend treats both network packets as two completely separate registration requests."),
        ("The Result ❌", "Two registrations are created for the same person, double-charging them or deducting two seats instead of one. Available seats are incorrectly consumed by ghost bookings.")
    ]
    for title, desc in prob_desc:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"• {title}:", 11, True, RED_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 6)

    # Right Column: SURGESHIELD SOLUTION (GREEN)
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.65), Inches(5.2), GREEN_BG, GREEN_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "SURGESHIELD SOLUTION: IDEMPOTENCY KEY", 14, True, GREEN_COLOR, 6)

    # Visual Flow Box inside right card
    flow_box = add_card(slide, Inches(7.13), Inches(2.1), Inches(5.15), Inches(1.2), CARD_WHITE, GREEN_BORDER)
    tb_fl = slide.shapes.add_textbox(Inches(7.2), Inches(2.15), Inches(5.0), Inches(1.1))
    tf_fl = tb_fl.text_frame
    tf_fl.word_wrap = True
    p_fl = tf_fl.paragraphs[0]
    style_para(p_fl, "VISUAL IDEMPOTENCY PIPELINE:", 10, True, GREEN_COLOR, 2)
    p_fl1 = tf_fl.add_paragraph()
    style_para(p_fl1, "Request A (Key: UUID-1) ────────┐\n                                 ↓\nRetry Request A (Key: UUID-1) ──→ IDEMPOTENCY ENGINE ──→ Single Booking Created\n                                                         (2nd Request: Safe Replay)", 10, True, TEXT_DARK, 0)

    sol_desc = [
        ("Client-Side UUID Header", "Client UI generates unique `Idempotency-Key` header with each submission."),
        ("Fast Pre-Flight Replay", "Server checks `registrations` table first. If key already exists, immediately returns `{ replayed: true }`. Zero seats deducted!"),
        ("What We Implemented", "Database constraint `UNIQUE(event_id, idempotency_key)` guarantees that even parallel retries are caught safely with zero seat loss.")
    ]
    for title, desc in sol_desc:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"✓ {title}:", 11, True, GREEN_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 5)

def build_slide_9(prs):
    # Slide 9: Problem 3 — Slow Synchronous Processing
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 3: Slow Synchronous Processing & Bottlenecks", "Asynchronous Processing & Decoupling", 9)

    # Top Half: NAIVE BLOCKING SYSTEM (RED)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(2.2), RED_BG, RED_BORDER)
    tb_top = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(2.0))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    p_t = tf_top.paragraphs[0]
    style_para(p_t, "NAIVE SYNCHRONOUS FLOW: THE BLOCKING EMAIL TRAP (2-3s DELAY)", 13, True, RED_COLOR, 4)

    # Visual Flow of Naive
    p_nf = tf_top.add_paragraph()
    style_para(p_nf, "Registration Request  →  Save to DB  →  Send Email/SMS (External API: 2000ms delay)  →  Wait...  →  HTTP Response to User", 11, True, TEXT_DARK, 4)
    p_nd = tf_top.add_paragraph()
    style_para(p_nd, "The Flaw: The user is forced to wait for work that does not need to happen inside the main request. During surges, web threads choke waiting for slow 3rd-party email APIs, causing cascading timeouts for all users.", 10, False, TEXT_BODY, 0)

    # Bottom Half: SURGESHIELD DECOUPLED PIPELINE (GREEN)
    add_card(slide, Inches(0.8), Inches(3.8), Inches(11.73), Inches(2.8), GREEN_BG, GREEN_BORDER)
    tb_bot = slide.shapes.add_textbox(Inches(1.0), Inches(3.9), Inches(11.33), Inches(2.6))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_b = tf_bot.paragraphs[0]
    style_para(p_b, "SURGESHIELD SOLUTION: DECOUPLED ASYNC PIPELINE (<15ms RESPONSE)", 13, True, GREEN_COLOR, 4)

    # Visual Flow of SurgeShield
    p_bf = tf_bot.add_paragraph()
    style_para(p_bf, "1. Fast Critical Path (<15ms):  Registration  →  PostgreSQL Row Lock  →  Insert Outbox (PENDING)  →  BullMQ Enqueue  →  Immediate HTTP 201!", 11, True, TEXT_DARK, 3)
    p_bf2 = tf_bot.add_paragraph()
    style_para(p_bf2, "2. Decoupled Background Path:   BullMQ / Redis Broker  →  Background Worker (800ms)  →  Outbox Updated to 'SENT'", 11, True, BLUE_COLOR, 5)

    p_bd = tf_bot.add_paragraph()
    style_para(p_bd, "Core Principle: \"Registration is the critical path. Notification processing is moved to the background.\"\nWhat We Implemented: BullMQ 5 queue backed by Redis 7 AOF persistence + PostgreSQL transactional outbox pattern + dedicated worker container.", 10, False, TEXT_BODY, 0)

def build_slide_10(prs):
    # Slide 10: Problem 4 — Traffic Overload & Load Balancing
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 4: Traffic Overload & Single-Server Saturation", "Horizontal Load Balancing & Failover", 10)

    # Left: THE PROBLEM - Single Server (RED)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(5.65), Inches(5.2), RED_BG, RED_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "THE SINGLE-SERVER SATURATION HAZARD", 14, True, RED_COLOR, 8)

    # Visual Single Server Flow
    p_sf = tf_l.add_paragraph()
    style_para(p_sf, "MANY CONCURRENT USERS\n        ↓\nSingle Web Server ❌\n        ↓\n100% CPU Saturation & Memory OOM\n        ↓\nSERVER CRASH & TOTAL SERVICE OUTAGE", 11, True, RED_COLOR, 8)

    prob_pts = [
        ("Single Point of Failure (SPOF)", "When one server handles routing, auth, business logic, and database access, its crash terminates 100% of user traffic."),
        ("Zero Burst Cushioning", "Incoming surges directly saturate the server's network socket queue.")
    ]
    for title, desc in prob_pts:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"• {title}:", 11, True, RED_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 6)

    # Right: SURGESHIELD SOLUTION - Nginx + 3x APIs (GREEN)
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.65), Inches(5.2), GREEN_BG, GREEN_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(1.55), Inches(5.15), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "SURGESHIELD SOLUTION: NGINX CLUSTER", 14, True, GREEN_COLOR, 8)

    # Visual Cluster Flow
    p_cf = tf_r.add_paragraph()
    style_para(p_cf, "MANY CONCURRENT USERS\n        ↓\nNGINX Reverse Proxy (:8080)\n  /         |         \\\nAPI 1     API 2     API 3\n(Served by: app1, app2, app3)", 11, True, BLUE_COLOR, 8)

    sol_pts = [
        ("Nginx L7 Round-Robin", "Distributes requests evenly across 3 stateless Node.js containers."),
        ("Edge Rate Limiting", "Nginx token-bucket drops malicious DDoS (20 r/s burst 40) before reaching Node.js."),
        ("Demonstrable Verification", "Every response exposes `servedBy` and `X-Served-By` headers to prove load distribution.")
    ]
    for title, desc in sol_pts:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"✓ {title}:", 11, True, GREEN_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, desc, 10, False, TEXT_BODY, 6)

def build_slide_11(prs):
    # Slide 11: Problem 5 — Worker Failure & Self-Healing
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 5: Component Failure & Queue Self-Healing", "Fault Tolerance & Crash Recovery", 11)

    # 3 Stage Horizontal Flow
    stages = [
        ("STAGE 1: WORKER DIES",
         "Background worker process crashes or is stopped (`docker compose stop worker`).\n\nAPI continues running normally! PostgreSQL commits bookings. Redis safely buffers queued jobs in memory & disk (`appendonly yes`).",
         RED_BG, RED_COLOR, RED_BORDER),
        ("STAGE 2: HEALTH DETECTION",
         "The health probe (`/health`) queries Redis for `worker:heartbeat`.\n\nBecause the worker is down, the 4-second TTL key expires. `/health` flags `worker: 'offline'` gracefully without killing the API.",
         BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("STAGE 3: RESTART & RECOVERY",
         "Worker process is restarted (`docker compose start worker`).\n\nWorker connects to Redis, picks up all buffered jobs, updates outbox to `SENT`, and restores heartbeat. ZERO DATA LOSS!",
         GREEN_BG, GREEN_COLOR, GREEN_BORDER)
    ]
    card_w = Inches(3.68)
    card_h = Inches(4.3)
    for i, (stitle, sdesc, bg, accent, border) in enumerate(stages):
        x = Inches(0.8 + i * 4.02)
        add_card(slide, x, Inches(1.5), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.2), Inches(1.7), card_w - Inches(0.4), Inches(0.38), stitle, accent, TEXT_LIGHT, 11)

        tb = slide.shapes.add_textbox(x + Inches(0.2), Inches(2.3), card_w - Inches(0.4), card_h - Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p_d = tf.paragraphs[0]
        style_para(p_d, sdesc, 11, False, TEXT_BODY, 0)

    # Bottom Summary
    banner = add_card(slide, Inches(0.8), Inches(6.0), Inches(11.73), Inches(0.85), PURPLE_BG, PURPLE_COLOR)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.33), Inches(0.75))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    style_para(p_b, "Resilience Guarantee: Even if the worker crashes under heavy surge load, zero notifications are lost and registrations continue without interruption.", 12, True, PURPLE_COLOR, 0, PP_ALIGN.CENTER)

def build_slide_12(prs):
    # Slide 12: Problem 6 — Capacity Mismatch & Self-Scaling
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Problem 6: Capacity Mismatch: Self-Scaling Architecture", "Dynamic Elasticity & Auto-Scaling Simulation", 12)

    # Visual Scaling Cycle (Horizontal Flow at top)
    cycle_box = add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(1.2), PURPLE_BG, PURPLE_BORDER)
    tb_c = slide.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.33), Inches(1.1))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p_ct = tf_c.paragraphs[0]
    style_para(p_ct, "THE DYNAMIC SCALING LIFECYCLE:", 11, True, PURPLE_COLOR, 2)
    p_cf = tf_c.add_paragraph()
    style_para(p_cf, "NORMAL CAPACITY (2 Workers)  ──[Traffic Surge: Queue Depth > 0]──→  SCALE OUT (4 → 6 → 8 → 10 Workers)  ──[Queue Drains]──→  SCALE IN (2 Workers)", 11, True, TEXT_DARK, 0)

    # Left: Prototype Simulation (PURPLE)
    add_card(slide, Inches(0.8), Inches(2.8), Inches(5.65), Inches(3.8), CARD_WHITE, PURPLE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(2.95), Inches(5.15), Inches(3.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "LOCAL PROTOTYPE: AUTO-SCALING SIMULATION", 13, True, PURPLE_COLOR, 6)

    sim_pts = [
        ("Honest Engineering Label", "Clearly labeled as Simulated for local demonstrability on a single machine without requiring a cloud Kubernetes cluster."),
        ("Backlog-Driven Sizing Formula", "`queueDepth = waiting + active;`\n`simulatedWorkers = Math.min(10, Math.max(2, 2 + Math.ceil(queueDepth / 3)));`"),
        ("Dynamic Status States", "• IDLE_BASELINE (2 workers)\n• SCALING_UP (up to 10 workers reacting to surge backlog)\n• DRAINING_QUEUE (workers active, backlog clearing)"),
        ("Live Simulation Endpoint", "POST `/api/demo/simulate-surge` enqueues 25-50 jobs into BullMQ to visually show dynamic scaling on the Admin UI.")
    ]
    for title, desc in sim_pts:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"• {title}:", 10.5, True, PURPLE_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, desc, 9.5, False, TEXT_BODY, 4)

    # Right: Production Kubernetes Blueprint (BLUE)
    add_card(slide, Inches(6.88), Inches(2.8), Inches(5.65), Inches(3.8), BLUE_BG, BLUE_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(2.95), Inches(5.15), Inches(3.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "PRODUCTION BLUEPRINT: KUBERNETES HPA (k8s/)", 13, True, BLUE_COLOR, 6)

    k8s_pts = [
        ("HorizontalPodAutoscaler (HPA v2)", "Kubernetes HPA manifest provided in `k8s/README.md` targeting the stateless API Deployment."),
        ("Scaling Policies", "• minReplicas: 3, maxReplicas: 20\n• Target metric: CPU averageUtilization 60%"),
        ("KEDA Worker Scaling", "KEDA (Kubernetes Event-driven Autoscaling) monitors Redis BullMQ backlog queue depth to scale worker pods dynamically."),
        ("High Availability Best Practices", "• PodDisruptionBudget ensures minimum healthy pod quorum\n• Readiness/Liveness probes gate traffic to healthy pods.")
    ]
    for title, desc in k8s_pts:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"✓ {title}:", 10.5, True, BLUE_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, desc, 9.5, False, TEXT_BODY, 4)

    # Bottom
    banner = add_card(slide, Inches(0.8), Inches(6.7), Inches(11.73), Inches(0.4), CARD_WHITE, CARD_BORDER)
    tb_bt = slide.shapes.add_textbox(Inches(1.0), Inches(6.72), Inches(11.33), Inches(0.35))
    tf_bt = tb_bt.text_frame
    p_btt = tf_bt.paragraphs[0]
    style_para(p_btt, "Key Distinction: Local prototype uses queue-depth virtual scaling for live demo; production uses Kubernetes HPA & KEDA.", 10, True, TEXT_MUTED, 0, PP_ALIGN.CENTER)

def build_slide_13(prs):
    # Slide 13: Monitoring & Health Dashboard
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Operational Visibility: Health Probes & Live Telemetry", "Observability, Health Checks & Monitoring", 13)

    pillars = [
        ("1. Multi-Tier Health Check (/health)",
         "Composite Dependency Verification",
         [
             "PostgreSQL Probe: Executes `SELECT 1`.",
             "Redis Probe: Executes `redis.ping()`.",
             "Worker Heartbeat: Checks `worker:heartbeat` key in Redis (4s TTL).",
             "Returns HTTP 200 with service breakdown:",
             "`{ status: 'ok', database: 'ok', redis: 'ok', worker: 'active' }`",
             "Graceful Degradation: If worker dies, reports `worker: 'offline'` while keeping HTTP API status functional."
         ],
         BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("2. Kubernetes Readiness (/ready)",
         "Ingress Traffic Routing Probe",
         [
             "Lightweight probe verifying DB connectivity.",
             "Returns `{ ready: true, instance: 'app1' }`.",
             "Prevents sending user traffic to cold-starting pods.",
             "Nginx Upstream Failover:",
             "`server app1:3000 max_fails=2 fail_timeout=5s;`",
             "`proxy_next_upstream error timeout http_502 http_503 http_504;`",
             "If App 1 crashes, Nginx retries App 2 in <1ms!"
         ],
         GREEN_BG, GREEN_COLOR, GREEN_BORDER),
        ("3. Prometheus & Live Admin UI",
         "Real-Time Telemetry & Monitoring",
         [
             "Prometheus Metrics (`/metrics`):",
             "• `http_requests_total`: by route, status, instance",
             "• `registrations_total`: by result outcome",
             "Live Admin Dashboard (`/api/admin/dashboard`):",
             "• Service health badges (Nginx, API, Postgres, Redis, BullMQ, Worker)",
             "• Real-time BullMQ queue depth counters",
             "• Outbox delivery tracker & scaling status"
         ],
         PURPLE_BG, PURPLE_COLOR, PURPLE_BORDER)
    ]

    card_w = Inches(3.68)
    card_h = Inches(5.1)
    for i, (title, subtitle, bullets, bg, accent, border) in enumerate(pillars):
        x = Inches(0.8 + i * 4.02)
        add_card(slide, x, Inches(1.5), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.15), Inches(1.65), card_w - Inches(0.3), Inches(0.4), title, accent, TEXT_LIGHT, 10.5)

        tb = slide.shapes.add_textbox(x + Inches(0.15), Inches(2.15), card_w - Inches(0.3), card_h - Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p_sub = tf.paragraphs[0]
        style_para(p_sub, subtitle, 10, True, TEXT_MUTED, 6)

        for bullet in bullets:
            p_b = tf.add_paragraph()
            style_para(p_b, f"• {bullet}", 9.5, False, TEXT_BODY, 4)

def build_slide_14(prs):
    # Slide 14: What Makes SurgeShield Unique?
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "What Makes SurgeShield Unique? The Integrated Platform", "Architectural Differentiation", 14)

    # Core Banner Statement
    banner = add_card(slide, Inches(0.8), Inches(1.4), Inches(11.73), Inches(1.0), PURPLE_BG, PURPLE_COLOR)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(1.48), Inches(11.33), Inches(0.85))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_bt = tf_b.paragraphs[0]
    style_para(p_bt, "SURGESHIELD IS NOT JUST AN EVENT-REGISTRATION APP.", 13, True, PURPLE_COLOR, 2)
    p_b2 = tf_b.add_paragraph()
    style_para(p_b2, "It is an integrated, demonstrable resilient-systems platform. Its uniqueness lies in the deliberate combination of 8 distributed resilience mechanisms working together seamlessly under load.", 11, False, TEXT_DARK, 0)

    # 8 Resilience Mechanisms in a 4x2 Grid
    mechanisms = [
        ("1. Strict Concurrency Control", "Pessimistic row locking (`SELECT ... FOR UPDATE`) guarantees zero overbooking even across multiple distributed nodes.", GREEN_COLOR),
        ("2. Guaranteed Idempotency", "Unique UUID keys and database constraints ensure network retries and double-clicks never deduct seats twice.", GREEN_COLOR),
        ("3. Decoupled Asynchronous Processing", "BullMQ + Redis offloads slow notification I/O, maintaining sub-15ms registration response times.", BLUE_COLOR),
        ("4. Horizontal Load Balancing", "Nginx round-robin distributes traffic across 3 stateless API nodes with serving instance verification (`servedBy`).", BLUE_COLOR),
        ("5. Persistent Queue-Based Recovery", "Redis AOF persistence buffers jobs during worker crashes; workers catch up automatically upon restart.", GREEN_COLOR),
        ("6. Dual-Layer Rate Limiting", "Edge token-bucket (20 r/s burst 40) + Express limiter protect the cluster from sudden traffic collapse.", RED_COLOR),
        ("7. Dynamic Scaling Simulation", "Simulated worker pool dynamically expands from 2 to 10 workers based on real-time BullMQ backlog depth.", PURPLE_COLOR),
        ("8. 1-Click Reproducibility & Reset", "Complete administrative reset endpoints and scripts restore system state instantly for clean demo reruns.", PURPLE_COLOR)
    ]

    card_w = Inches(2.75)
    card_h = Inches(1.9)
    for idx, (m_title, m_desc, accent) in enumerate(mechanisms):
        col = idx % 4
        row = idx // 4
        x = Inches(0.8 + col * 2.99)
        y = Inches(2.6 + row * 2.1)
        add_card(slide, x, y, card_w, card_h, CARD_WHITE, CARD_BORDER)

        tb = slide.shapes.add_textbox(x + Inches(0.12), y + Inches(0.12), card_w - Inches(0.24), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        style_para(p_t, m_title, 11, True, accent, 4)
        p_d = tf.add_paragraph()
        style_para(p_d, m_desc, 9.5, False, TEXT_BODY, 0)

    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.73), Inches(0.3))
    tf_foot = tb_foot.text_frame
    p_f = tf_foot.paragraphs[0]
    style_para(p_f, "The Value: Not just individual tools, but how they interlock to create an uncrashable, zero-overbooking platform.", 10.5, True, TEXT_MUTED, 0, PP_ALIGN.CENTER)

def build_slide_15(prs):
    # Slide 15: Technologies Used & Architectural Justification
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Technology Stack Selection: Architectural Justification", "Component Rationale & Fit", 15)

    techs = [
        ("Nginx 1.27 Alpine", "Gateway & Load Balancer", "High-performance C-based reverse proxy, L7 round-robin load distribution, edge rate-limiting token bucket, and instant upstream failover.", BLUE_COLOR),
        ("Node.js 20 & Express", "Stateless API Cluster", "Lightweight, non-blocking asynchronous event loop ideal for high-concurrency I/O multiplexing and rapid REST API response times.", BLUE_COLOR),
        ("PostgreSQL 16", "ACID Data Storage", "Enterprise relational database providing row-level locking (SELECT FOR UPDATE), transaction isolation, and strict check constraints.", GREEN_COLOR),
        ("Redis 7 Alpine", "In-Memory Cache & Broker", "Sub-millisecond latency in-memory data store for event catalog caching (5s TTL) and durable queue backing with AOF persistence.", GREEN_COLOR),
        ("BullMQ 5", "Distributed Async Queue", "Robust Redis-based background job engine with exponential backoff retries, concurrency controls, and failure quarantine.", PURPLE_COLOR),
        ("Docker & Docker Compose", "Container Orchestration", "Isolated multi-container local stack mimicking production network topologies with deterministic healthchecks and dependencies.", BLUE_COLOR),
        ("Prometheus (prom-client)", "Metrics & Telemetry", "Industry-standard metrics instrumentation exposing HTTP request counters, registration results, and Node.js process metrics.", PURPLE_COLOR),
        ("Bcrypt & JSON Web Tokens", "Authentication & Security", "Salted password hashing with bcrypt (12 rounds) and stateless signed JWTs enforcing role-based permissions (ATTENDEE vs ORGANIZER).", BLUE_COLOR)
    ]

    card_w = Inches(2.75)
    card_h = Inches(2.35)
    for idx, (name, role, desc, accent) in enumerate(techs):
        col = idx % 4
        row = idx // 4
        x = Inches(0.8 + col * 2.99)
        y = Inches(1.5 + row * 2.6)
        add_card(slide, x, y, card_w, card_h, CARD_WHITE, CARD_BORDER)

        tb = slide.shapes.add_textbox(x + Inches(0.12), y + Inches(0.12), card_w - Inches(0.24), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p_n = tf.paragraphs[0]
        style_para(p_n, name, 12, True, accent, 2)
        p_r = tf.add_paragraph()
        style_para(p_r, role, 10, True, TEXT_MUTED, 6)
        p_d = tf.add_paragraph()
        style_para(p_d, desc, 9.5, False, TEXT_BODY, 0)

    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.73), Inches(0.3))
    tf_foot = tb_foot.text_frame
    p_f = tf_foot.paragraphs[0]
    style_para(p_f, "Every technology was deliberately selected for maximum resilience, low latency, and zero vendor lock-in.", 11, True, GREEN_COLOR, 0, PP_ALIGN.CENTER)

def build_slide_16(prs):
    # Slide 16: Requirement -> Implementation Matrix
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Official P1 Requirement Traceability & Implementation Matrix", "Requirements Traceability", 16)

    rows = 8
    cols = 5
    table_shape = slide.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.4))
    table = table_shape.table

    col_widths = [Inches(2.2), Inches(2.3), Inches(3.7), Inches(2.0), Inches(1.53)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    headers = ["P1 Requirement", "Failure Condition", "SurgeShield Engineering Solution", "Technology", "Status"]
    data = [
        ["Prevent overbooking", "Concurrency contention on finite seats", "Pessimistic row-locking (SELECT ... FOR UPDATE) + ACID rollback", "PostgreSQL 16", "IMPLEMENTED"],
        ["Prevent duplicate orders", "Network retries & client double-clicks", "Client Idempotency-Key header + UNIQUE(event_id, idempotency_key)", "PostgreSQL / Express", "IMPLEMENTED"],
        ["Absorb peak traffic surges", "Slow synchronous notification delays", "Decoupled async job queue + Transactional Outbox pattern", "BullMQ + Redis 7", "IMPLEMENTED"],
        ["Distribute traffic across nodes", "Single-server CPU/memory saturation", "L7 Reverse Proxy with round-robin load distribution & failover", "Nginx 1.27 Alpine", "IMPLEMENTED"],
        ["Rate limit surge bursts", "Abnormal burst traffic / DDoS collapse", "Dual-layer token-bucket (20 r/s) + Express cluster limiter", "Nginx + Express", "IMPLEMENTED"],
        ["Add/remove worker capacity", "Capacity mismatch during surges", "Queue-depth reactive virtual worker pool (2 to 10) + K8s HPA manifest", "BullMQ / K8s HPA", "SIMULATED + K8S"],
        ["Detect unhealthy services", "Silent worker or node crashes", "Composite /health probe (DB + Redis + Heartbeat) & auto-failover", "Redis TTL + Nginx", "IMPLEMENTED"]
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BG
        p = cell.text_frame.paragraphs[0]
        style_para(p, h, 11, True, TEXT_LIGHT, 0)

    for row_idx, row_data in enumerate(data):
        bg = CARD_WHITE if row_idx % 2 == 0 else RGBColor(241, 245, 249)
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            if col_idx == 4:
                status_color = GREEN_COLOR if text == "IMPLEMENTED" else PURPLE_COLOR
                style_para(p, text, 10, True, status_color, 0)
            elif col_idx == 0:
                style_para(p, text, 10, True, TEXT_DARK, 0)
            else:
                style_para(p, text, 10, False, TEXT_BODY, 0)

def build_slide_17(prs):
    # Slide 17: Before vs After Comparison
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Transformation Benchmark: Naive Baseline vs. SurgeShield", "Architectural Transformation", 17)

    # Left: NAIVE BASELINE (RED)
    add_card(slide, Inches(0.8), Inches(1.4), Inches(5.65), Inches(5.3), RED_BG, RED_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.55), Inches(5.15), Inches(5.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    style_para(p_l, "NORMAL / NAIVE SYSTEM ❌", 16, True, RED_COLOR, 10)

    naive_pts = [
        ("Single Server SPOF", "One Node.js process handles traffic; crash terminates 100% of user sessions."),
        ("Direct Unlocked DB Updates", "Executes `SELECT` then `UPDATE` without locks. Results in massive overbooking and negative seats."),
        ("Synchronous Blocking Notifications", "Calls email/SMS in request loop. Client hangs for 2-3 seconds; connections exhaust."),
        ("Duplicate Request Vulnerability", "Retries create duplicate bookings and double charges on client reconnects."),
        ("Limited Failure Handling", "Worker or process crash permanently drops pending jobs with zero recovery."),
        ("Zero Operational Visibility", "Raw terminal console logs; blind during live production outages.")
    ]
    for title, desc in naive_pts:
        p_t = tf_l.add_paragraph()
        style_para(p_t, f"- {title}:", 11.5, True, RED_COLOR, 1)
        p_d = tf_l.add_paragraph()
        style_para(p_d, f"   {desc}", 10, False, TEXT_BODY, 6)

    # Right: SURGESHIELD RESILIENT PLATFORM (GREEN)
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.65), Inches(5.3), GREEN_BG, GREEN_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.13), Inches(1.55), Inches(5.15), Inches(5.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_r = tf_r.paragraphs[0]
    style_para(p_r, "SURGESHIELD PLATFORM ✓", 16, True, GREEN_COLOR, 10)

    shield_pts = [
        ("Multi-Node L7 Load Balancing", "Nginx round-robin balances traffic across 3 stateless API nodes with instant failover."),
        ("PostgreSQL Row-Level Locking", "`SELECT ... FOR UPDATE` strictly serializes seat decrements. 100% ZERO OVERBOOKING."),
        ("Decoupled BullMQ Async Pipeline", "Fast DB commit + outbox pattern. API responds in <15ms; workers process in background."),
        ("Idempotency-Key Protection", "Unique UUID checks replay cached response safely without extra seat deductions."),
        ("Persistent Queue Recovery", "Redis AOF buffers backlog; workers catch up automatically upon restart."),
        ("Full Operational Telemetry", "Prometheus metrics (`/metrics`), live health probes, and real-time Admin UI.")
    ]
    for title, desc in shield_pts:
        p_t = tf_r.add_paragraph()
        style_para(p_t, f"✓ {title}:", 11.5, True, GREEN_COLOR, 1)
        p_d = tf_r.add_paragraph()
        style_para(p_d, f"   {desc}", 10, False, TEXT_BODY, 6)

def build_slide_18(prs):
    # Slide 18: Live Mentor Demonstration Playbook (17-Step Script)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Demonstration Playbook: 17-Step Mentor Live Demo", "Mentor Evaluation & Demonstration Script", 18)

    phases = [
        ("Phase 1: Baseline Architecture",
         "Load Balancing & Health",
         [
             "1. Run `docker compose ps` -> 6 healthy containers.",
             "2. Open `http://localhost:8080` -> Log in as Attendee.",
             "3. Inspect Network tab -> `X-Served-By` rotates.",
             "4. Check catalog cache -> Show `cache: HIT`.",
             "5. Open Admin UI -> Show service health badges."
         ],
         BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("Phase 2: Concurrency & Idempotency",
         "Stress Testing & Guarantees",
         [
             "6. Reset 'Concurrency Test' event to 5 seats.",
             "7. Trigger Live Stress Test: Fire 25 requests.",
             "8. Verify: Exactly 5 confirmed, 20 rejected (409).",
             "9. Verify remaining seats: Exactly 0 (No Overbooking!).",
             "10. Resubmit identical request -> Show `replayed: true`."
         ],
         GREEN_BG, GREEN_COLOR, GREEN_BORDER),
        ("Phase 3: Failure & Self-Healing",
         "Fault Tolerance & Rate Limit",
         [
             "11. Run `docker compose stop worker`.",
             "12. Place booking -> Confirms in DB (<15ms).",
             "13. Show worker badge turns 'Offline' in `/health`.",
             "14. Run `docker compose start worker` -> Auto-recovers.",
             "15. Test `/api/demo/rate-limit-test` -> HTTP 429."
         ],
         RED_BG, RED_COLOR, RED_BORDER),
        ("Phase 4: Scaling & Reset",
         "Elasticity & Reproducibility",
         [
             "16. Click 'Simulate 50-Job Surge' -> Watch virtual worker pool scale from 2 to 10 workers.",
             "17. Click '1-Click Full System Reset' -> Restore all event seats and clear test records instantly."
         ],
         PURPLE_BG, PURPLE_COLOR, PURPLE_BORDER)
    ]

    card_w = Inches(2.75)
    card_h = Inches(5.1)
    for i, (title, subtitle, bullets, bg, accent, border) in enumerate(phases):
        x = Inches(0.8 + i * 2.99)
        add_card(slide, x, Inches(1.5), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.12), Inches(1.65), card_w - Inches(0.24), Inches(0.4), title, accent, TEXT_LIGHT, 10)

        tb = slide.shapes.add_textbox(x + Inches(0.15), Inches(2.15), card_w - Inches(0.3), card_h - Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p_sub = tf.paragraphs[0]
        style_para(p_sub, subtitle, 10, True, TEXT_MUTED, 8)

        for bullet in bullets:
            p_b = tf.add_paragraph()
            style_para(p_b, bullet, 9.5, False, TEXT_BODY, 6)

def build_slide_19(prs):
    # Slide 19: Production Cloud Deployment Roadmap
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BG)
    add_header(slide, "Production Cloud Blueprint: From Prototype to Enterprise", "Enterprise Production Architecture", 19)

    cloud_pillars = [
        ("1. Kubernetes Cluster (EKS/GKE)",
         "Stateless API Autoscaling",
         [
             "Deploy stateless API image to Kubernetes Deployment.",
             "HorizontalPodAutoscaler (HPA v2) scales API pods from 3 to 20 based on 60% CPU utilization.",
             "KEDA (Kubernetes Event-driven Autoscaling) scales worker pods from 1 to 50 based on Redis BullMQ queue length.",
             "PodDisruptionBudget guarantees high availability during node maintenance."
         ],
         BLUE_BG, BLUE_COLOR, BLUE_BORDER),
        ("2. Managed Multi-AZ Database",
         "AWS Aurora PostgreSQL",
         [
             "Multi-AZ deployment with automatic sub-minute failover.",
             "Dedicated Read Replicas serve high-frequency event catalog queries, completely offloading the primary writer.",
             "Pessimistic row locking (`SELECT FOR UPDATE`) executes exclusively on the writer instance with zero cross-region latency."
         ],
         GREEN_BG, GREEN_COLOR, GREEN_BORDER),
        ("3. In-Memory Distributed Cache",
         "AWS ElastiCache Redis Cluster",
         [
             "Multi-AZ replication with automatic failover and Redis Sentinel.",
             "Durable append-only file (AOF) persistence across shards.",
             "Isolates catalog caching (volatile LRU) from BullMQ queue streams (persistent)."
         ],
         PURPLE_BG, PURPLE_COLOR, PURPLE_BORDER),
        ("4. Edge Security & Global CDN",
         "Cloudflare / AWS WAF",
         [
             "Global Anycast CDN caches static assets at edge locations.",
             "Edge WAF blocks volumetric DDoS attacks before hitting Kubernetes.",
             "Geo-distributed TLS termination ensures low latency worldwide."
         ],
         RED_BG, RED_COLOR, RED_BORDER)
    ]

    card_w = Inches(2.75)
    card_h = Inches(5.1)
    for i, (title, subtitle, bullets, bg, accent, border) in enumerate(cloud_pillars):
        x = Inches(0.8 + i * 2.99)
        add_card(slide, x, Inches(1.5), card_w, card_h, bg, border)

        badge = add_badge(slide, x + Inches(0.12), Inches(1.65), card_w - Inches(0.24), Inches(0.4), title, accent, TEXT_LIGHT, 10)

        tb = slide.shapes.add_textbox(x + Inches(0.15), Inches(2.15), card_w - Inches(0.3), card_h - Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p_sub = tf.paragraphs[0]
        style_para(p_sub, subtitle, 10, True, TEXT_MUTED, 8)

        for bullet in bullets:
            p_b = tf.add_paragraph()
            style_para(p_b, f"• {bullet}", 9.5, False, TEXT_BODY, 6)

def build_slide_20(prs):
    # Slide 20: Conclusion & Core Takeaways (Dark Theme)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, DARK_BG)
    add_header(slide, "SurgeShield: Enterprise Resilience Realized", "Summary & Core Takeaways", 20, is_dark=True)

    pillars = [
        ("1. Concurrency Safety Requires Isolation",
         DARK_CARD,
         GREEN_COLOR,
         [
             "Application-level checks (`if available >= qty`) fail catastrophically under multi-node concurrency.",
             "Database row-level locking (`SELECT ... FOR UPDATE`) is non-negotiable for finite inventory.",
             "SurgeShield guarantees mathematically zero overbooking regardless of traffic volume."
         ]),
        ("2. Decoupling Is Key to Scalability",
         DARK_CARD,
         BLUE_COLOR,
         [
             "Synchronous 3rd-party dependencies will destroy web server throughput during flash crowds.",
             "Separating the fast critical path (<15ms) from background notification processing preserves availability.",
             "Queues act as shock absorbers, smoothing out extreme traffic spikes."
         ]),
        ("3. Fault Tolerance Must Be Designed In",
         DARK_CARD,
         PURPLE_COLOR,
         [
             "Components will fail during high traffic: workers crash, connections drop, and users retry.",
             "Persistent queues, idempotent APIs, multi-node load balancing, and active health checks turn potential crashes into self-healing events."
         ])
    ]

    card_w = Inches(3.68)
    card_h = Inches(4.2)
    for i, (title, bg, accent, bullets) in enumerate(pillars):
        x = Inches(0.8 + i * 4.02)
        add_card(slide, x, Inches(1.5), card_w, card_h, bg, DARK_BORDER)

        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), Inches(1.7), Inches(0.8), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(x + Inches(0.2), Inches(1.9), card_w - Inches(0.4), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        style_para(p_t, title, 13, True, TEXT_LIGHT, 10)

        for bullet in bullets:
            p_b = tf.add_paragraph()
            style_para(p_b, f"• {bullet}", 10, False, TEXT_LIGHT_MUTED, 6)

    # Bottom Callout Banner
    banner = add_card(slide, Inches(0.8), Inches(5.95), Inches(11.73), Inches(0.9), DARK_CARD, PURPLE_COLOR)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.33), Inches(0.8))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    style_para(p_b, "SurgeShield: Demonstrable Resilience Under Extreme Concurrency", 14, True, TEXT_LIGHT, 2, PP_ALIGN.CENTER)
    p_b2 = tf_b.add_paragraph()
    style_para(p_b2, "Thank You  |  Ready for Mentor Evaluation & Architecture Q&A", 11, False, RGBColor(165, 180, 252), 0, PP_ALIGN.CENTER)

# ---------------------------------------------------------
# MAIN GENERATION
# ---------------------------------------------------------
def main():
    print("Initializing PowerPoint presentation...")
    prs = create_deck()

    print("Generating slides...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)
    build_slide_9(prs)
    build_slide_10(prs)
    build_slide_11(prs)
    build_slide_12(prs)
    build_slide_13(prs)
    build_slide_14(prs)
    build_slide_15(prs)
    build_slide_16(prs)
    build_slide_17(prs)
    build_slide_18(prs)
    build_slide_19(prs)
    build_slide_20(prs)

    output_local = "SurgeShield_Architecture_Presentation.pptx"
    output_downloads = r"C:\Users\nsree\Downloads\SurgeShield_Architecture_Presentation.pptx"

    print(f"Saving presentation to {output_local}...")
    prs.save(output_local)
    print("Saved local copy successfully.")

    print(f"Copying presentation to {output_downloads}...")
    try:
        shutil.copyfile(output_local, output_downloads)
        print("Copied to Downloads directory successfully.")
    except Exception as e:
        print(f"Warning copying to Downloads: {e}")

    print("All 20 slides generated successfully!")

if __name__ == "__main__":
    main()
