from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io

# ── FIELDS ──────────────────────────────────────────────────────────────────
CUSTOMER_NAME   = "CUSTOMER NAME"
PROPERTY        = "Property address / description"
SERVICE_TYPE    = "Land Clearing / Forestry Mulching"
QUOTE_NUM       = "CC-2026-XXX"
DATE            = "June 27, 2026"

ACCOMPLISH      = """What the customer wants to accomplish."""

SCOPE           = """Scope of work narrative."""

CONDITIONS = [
    ["Acreage",   "X acres"],
    ["Density",   "L2 Moderate"],
    ["Terrain",   "Flat"],
    ["Ground",    "No rock"],
    ["Access",    "Description"],
    ["Material",  "Mulched in place"],
]

EXPECT          = """What the customer can expect when the job is done."""

INCLUDED        = [
    "Item 1",
    "Item 2",
    "Item 3",
]
NOT_INCLUDED    = [
    "Hazardous materials of any kind",
    "Items added to scope after quote acceptance",
    "Work beyond marked property boundaries",
]

PRICE_LINE      = "$0,000"
PRICE_DESC      = "Complete as scoped - service description"
PRICE_SUB       = "Mobilization included · 20% deposit required to schedule · Balance due on completion"

NEXT_STEP       = "Reply to confirm or call to lock in your date. A 20% deposit is required to schedule. We will confirm your date within 24 hours."

QUOTE_FOOTER    = f"Quote # {QUOTE_NUM} | Price: {PRICE_LINE} | 20% deposit to schedule · balance due on completion"
# ────────────────────────────────────────────────────────────────────────────

BLACK   = colors.HexColor('#0d0d0d')
DARK    = colors.HexColor('#1a1a1a')
YELLOW  = colors.HexColor('#F5C400')
RED     = colors.HexColor('#CC2222')
WHITE   = colors.white
LGRAY   = colors.HexColor('#f5f5f5')
MGRAY   = colors.HexColor('#dddddd')
DGRAY   = colors.HexColor('#555555')

def build_styles():
    return {
        'hdr_chew': ParagraphStyle('hdr_chew', fontName='Helvetica-Bold', fontSize=28, textColor=RED, spaceAfter=0, leading=30, alignment=TA_LEFT),
        'hdr_sub': ParagraphStyle('hdr_sub', fontName='Helvetica', fontSize=8, textColor=WHITE, spaceAfter=2, leading=11, alignment=TA_LEFT),
        'hdr_contact': ParagraphStyle('hdr_contact', fontName='Helvetica', fontSize=8, textColor=YELLOW, spaceAfter=0, leading=12, alignment=TA_RIGHT),
        'section_label': ParagraphStyle('section_label', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, spaceAfter=0, leading=10, alignment=TA_LEFT),
        'meta_label': ParagraphStyle('meta_label', fontName='Helvetica-Bold', fontSize=7.5, textColor=DGRAY, spaceAfter=1, leading=10),
        'meta_value': ParagraphStyle('meta_value', fontName='Helvetica', fontSize=9, textColor=BLACK, spaceAfter=0, leading=12),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9, textColor=BLACK, spaceAfter=4, leading=13),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9, textColor=BLACK, spaceAfter=2, leading=13, leftIndent=12, firstLineIndent=-8),
        'price_amt': ParagraphStyle('price_amt', fontName='Helvetica-Bold', fontSize=26, textColor=WHITE, spaceAfter=2, leading=28, alignment=TA_CENTER),
        'price_desc': ParagraphStyle('price_desc', fontName='Helvetica', fontSize=9, textColor=WHITE, spaceAfter=2, leading=13, alignment=TA_CENTER),
        'price_sub': ParagraphStyle('price_sub', fontName='Helvetica', fontSize=8, textColor=YELLOW, spaceAfter=0, leading=11, alignment=TA_CENTER),
        'next_step': ParagraphStyle('next_step', fontName='Helvetica', fontSize=9, textColor=BLACK, spaceAfter=4, leading=13),
        'sig_label': ParagraphStyle('sig_label', fontName='Helvetica-Bold', fontSize=7.5, textColor=DGRAY, spaceAfter=2, leading=10),
        'sig_line': ParagraphStyle('sig_line', fontName='Helvetica', fontSize=9, textColor=BLACK, spaceAfter=0, leading=12),
        'footer': ParagraphStyle('footer', fontName='Helvetica', fontSize=7, textColor=DGRAY, spaceAfter=0, leading=10, alignment=TA_CENTER),
        'tc_item_label': ParagraphStyle('tc_item_label', fontName='Helvetica-Bold', fontSize=7.5, textColor=RED, spaceAfter=1, leading=10),
        'tc_item': ParagraphStyle('tc_item', fontName='Helvetica', fontSize=7.5, textColor=BLACK, spaceAfter=3, leading=11),
    }

def section_bar(label, S):
    tbl = Table([[Paragraph(label, S['section_label'])]], colWidths=[7.5*inch])
    tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RED),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8)]))
    return tbl

def tc_section(S):
    items = []
    items.append(Spacer(1, 10))
    items.append(section_bar("TERMS & CONDITIONS", S))
    items.append(Spacer(1, 4))
    items.append(Paragraph("By accepting this proposal, customer acknowledges and agrees to all terms below. These terms are incorporated into and govern the scope of work described above.", S['tc_item']))
    items.append(Spacer(1, 6))
    terms = [
        ("1. PROPERTY OWNERSHIP & AUTHORIZATION", "Before we begin, we just need to confirm you are the legal owner of the property or have written permission from the owner to authorize this work. This protects everyone. CHEW cannot take responsibility for work on property the customer was not authorized to approve."),
        ("2. PROPERTY BOUNDARY MARKING", "So we clear exactly what you want and nothing you do not, please identify and point out all property boundaries before we start. We do not survey or verify property lines, so we will work within the area you show us. We cannot be responsible for work outside the boundaries you have communicated to us."),
        ("3. SAFETY ZONE - 300-FOOT CLEARANCE", "For everyone's safety, no person, animal, or unattended vehicle should be within 300 feet of active machine operation - including parked vehicles, pets, livestock, children, and bystanders. We ask that you help keep the area clear. CHEW will always pause work to keep people and animals safe whenever the zone is breached. Repeated or excessive stoppages may result in a delay charge at the applicable hourly rate."),
        ("4. SLOPE & TERRAIN LIMITATIONS", "Your safety and ours comes first. For that reason, CHEW does not operate equipment on inclines exceeding 15 degrees. We will review slope and terrain together during the on-site visit so there are no surprises. If any area cannot be worked safely, we will talk it through and adjust the scope or pricing for that section before we begin."),
        ("5. UTILITY LOCATE - 811 REQUIRED", "To protect what is beneath your property, please contact 811 (Call Before You Dig) and make sure all underground utilities are located and marked before we start - electrical, gas, water, sewer, irrigation, invisible pet fencing, and fiber. We will not break ground until you have given us the green light that the 811 locate is complete. CHEW cannot be responsible for damage to utilities that were not marked."),
        ("6. SITE READINESS & HAZARD DISCLOSURE", "We protect your property best when we know what is on it. Please tell us about all known site hazards before we arrive - buried wire or fence, septic components, irrigation heads, drainage pipes, cisterns, wells, buried structures, stumps, and anything not visible from the surface - and mark septic lids and sprinkler heads ahead of time. CHEW cannot be responsible for damage to hazards that were not disclosed or marked."),
        ("7. FENCE LINES & BURIED WIRE", "Hidden fence wire is one of the most common causes of equipment damage in clearing work, so please mark all fence lines, buried wire, t-posts, and boundary fencing before we begin. CHEW cannot be responsible for damage to fence lines or buried wire that were not marked."),
        ("8. TURF, LAWN & GROUND DISTURBANCE", "Track equipment naturally causes some turf disturbance, ruts, compaction, and surface scarring - it comes with this kind of site work. We will do our best to minimize it, but we cannot guarantee the ground surface will be restored to its original condition. By moving forward, the customer accepts ground disturbance as a normal part of the work."),
        ("9. NO REGROWTH GUARANTEE", "Mulching and clearing remove what is above ground, but they do not remove root systems - so some regrowth is natural and expected. We cannot guarantee against it. Ongoing maintenance to manage regrowth is up to the customer after our work is done."),
        ("10. STUMPS & ROOT SYSTEMS", "Forestry mulching grinds surface and near-surface material. Deeper root systems, stumps, and buried root balls may not be fully eliminated and can resurface over time. That is the nature of mulching, not a defect in our work."),
        ("11. TREE DIAMETER LIMITATIONS", "Our SP-900 forestry mulcher handles trees up to 6 inches in diameter as standard scope. Trees 7 to 8 inches we will look at together during the site visit - they may need a scope adjustment or additional charge. Trees over 8 inches are outside what the mulcher is built to process and are not included. Please point out any large-diameter trees before the estimate so we can plan for them. CHEW cannot be responsible for equipment damage from undisclosed oversized trees."),
        ("12. WEATHER & SCHEDULING", "This is weather-dependent work, so we may need to reschedule for rain, standing water, extreme heat, or unsafe conditions - always with your safety and a quality result in mind, and never a penalty to you. Rescheduled jobs go to the next available opening. Deposits are non-refundable for cancellations made within 48 hours of the scheduled date."),
        ("13. ACCESS & GATE AVAILABILITY", "We will review site access together during the on-site visit. On your scheduled work date, please have access ready - unlocked gates, cleared entry paths, and room to stage the truck, trailer, and machine. If we arrive and cannot access the site, the mobilization fee is due in full whether or not work is performed, since the trip and equipment haul still happened."),
        ("14. PETS & LIVESTOCK", "For their safety, please secure and remove all pets, livestock, and animals from the work area and the 300-foot safety zone before we begin, and keep them secured while we work. CHEW cannot be responsible for injury to animals that enter the work area."),
        ("15. DOWNTIME BILLING", "We are happy to keep you informed as we work. If the job gets significantly delayed or interrupted by the customer - extended direction of the operator, scope disputes mid-job, or access issues - that time is billable at the applicable hourly rate. On project-priced jobs, significant customer-caused delays may need a written change order before we continue."),
        ("16. SCOPE CHANGES - WRITTEN ONLY", "To keep everyone on the same page, any change to the agreed scope - adding, reducing, or modifying - needs a written change order signed by both of us before that work begins. We do not honor verbal scope changes, simply to protect you from misunderstandings. Additional scope is priced separately at current rates."),
        ("17. DEBRIS OWNERSHIP & DISPOSAL", "Once material is mulched, cleared, or loaded for haul-off, it is considered disposed and cannot be reclaimed after work has begun. By moving forward, the customer confirms they have the right to authorize disposal of all material on the property."),
        ("18. PHOTOGRAPHY & MARKETING", "We like to document our work with before, during, and after photos and video - for our records and to show what we do, including on social media and advertising. We will never publish identifying personal information without your consent."),
        ("19. FLUID & FUEL CONTACT", "Minor hydraulic fluid and fuel drips are a normal part of operating heavy equipment. CHEW cannot be responsible for incidental fluid contact with soil during normal machine operation."),
        ("20. ACTS OF NATURE", "Clearing dense vegetation can sometimes cause natural movement of trees and material. CHEW cannot be responsible for falling trees, widow-makers, natural debris movement, or other acts of nature that occur during or as a result of the work."),
        ("21. THIRD-PARTY PROPERTY & STRUCTURES", "So we can protect everything on your property, please disclose all improvements on or under it before we start - buried irrigation, invisible fencing, drainage pipes, or septic components. CHEW cannot be responsible for damage to structures or objects that were not disclosed or marked."),
        ("22. PAYMENT TERMS & FEES", "A deposit may be required to secure your place on the schedule; the amount will be specified at the time of booking. The remaining balance is due in full upon job completion, before equipment leaves the property. Accepted payment methods are cash, credit card, and check. Cash payments may qualify for a discount — ask at time of booking. Credit card payments may be subject to a processing fee. Any check returned for insufficient funds is subject to a $35 returned-check fee, and the outstanding balance plus that fee must be paid immediately by cash or credit card. Customer-initiated cancellations within 48 hours of the scheduled start date will result in forfeiture of the deposit. If collection action is required, customer is responsible for all collection costs and reasonable attorney fees."),
        ("23. PRICE VALIDITY", "This quote is good for 30 days from the issue date. After that, we will just need to reconfirm pricing in writing before scheduling."),
        ("24. DISPUTE RESOLUTION & GOVERNING LAW", "In the unlikely event of a dispute, this agreement is governed by the laws of the State of Texas, with venue in Coryell County, Texas."),
    ]
    for label, text in terms:
        items.append(KeepTogether([Paragraph(label, S['tc_item_label']), Paragraph(text, S['tc_item']), Spacer(1, 5)]))
    return items

def build_proposal(output_path):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.4*inch, bottomMargin=0.5*inch)
    S = build_styles()
    story = []

    hdr_data = [[Table([[[Paragraph("CHEW", S['hdr_chew'])],[Paragraph("Central Texas Site Services", S['hdr_sub'])],[Paragraph("Clearing · Hauling · Earthwork · Waste Removal", S['hdr_sub'])]]], colWidths=[4*inch]), Table([[[Paragraph("737-235-1335", S['hdr_contact'])],[Paragraph("chew.earthworks@gmail.com", S['hdr_contact'])],[Paragraph("callchew.com", S['hdr_contact'])],[Paragraph("Copperas Cove, TX", S['hdr_contact'])]]], colWidths=[3.5*inch])]]
    hdr_tbl = Table(hdr_data, colWidths=[4*inch, 3.5*inch])
    hdr_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(0,-1),12),('RIGHTPADDING',(-1,0),(-1,-1),12)]))
    story.append(hdr_tbl); story.append(Spacer(1, 6))

    story.append(section_bar("PROPOSAL", S)); story.append(Spacer(1, 4))
    meta_data = [[Paragraph("PREPARED FOR",S['meta_label']),Paragraph(CUSTOMER_NAME,S['meta_value']),Paragraph("QUOTE #",S['meta_label']),Paragraph(QUOTE_NUM,S['meta_value'])],[Paragraph("PROPERTY",S['meta_label']),Paragraph(PROPERTY,S['meta_value']),Paragraph("DATE",S['meta_label']),Paragraph(DATE,S['meta_value'])],[Paragraph("SERVICE",S['meta_label']),Paragraph(SERVICE_TYPE,S['meta_value']),Paragraph("VALID",S['meta_label']),Paragraph("30 days from issue",S['meta_value'])]]
    meta_tbl = Table(meta_data, colWidths=[1.1*inch, 3.3*inch, 0.8*inch, 2.3*inch])
    meta_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRAY),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-2),0.5,MGRAY)]))
    story.append(meta_tbl); story.append(Spacer(1, 8))

    story.append(KeepTogether([section_bar("WHAT YOU WANT TO ACCOMPLISH",S),Spacer(1,4),Paragraph(ACCOMPLISH,S['body']),Spacer(1,6)]))
    story.append(KeepTogether([section_bar(f"SCOPE OF WORK - {SERVICE_TYPE.upper()}",S),Spacer(1,4),Paragraph(SCOPE,S['body']),Spacer(1,6)]))

    story.append(section_bar("SITE CONDITIONS", S)); story.append(Spacer(1, 4))
    cond_data = [[Paragraph("DETAIL",S['meta_label']),Paragraph("INFO",S['meta_label'])]] + [[Paragraph(l,S['meta_label']),Paragraph(v,S['meta_value'])] for l,v in CONDITIONS]
    cond_tbl = Table(cond_data, colWidths=[1.5*inch, 6*inch])
    cond_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),WHITE),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LGRAY]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-2),0.5,MGRAY)]))
    story.append(cond_tbl); story.append(Spacer(1, 8))

    story.append(KeepTogether([section_bar("WHAT YOU CAN EXPECT",S),Spacer(1,4),Paragraph(EXPECT,S['body']),Spacer(1,6)]))

    story.append(section_bar("WHAT'S INCLUDED / WHAT'S NOT INCLUDED", S)); story.append(Spacer(1, 4))
    inc_items = [Paragraph(f"- {i}",S['bullet']) for i in INCLUDED]
    not_items = [Paragraph(f"- {i}",S['bullet']) for i in NOT_INCLUDED]
    mx = max(len(inc_items),len(not_items))
    while len(inc_items)<mx: inc_items.append(Paragraph("",S['bullet']))
    while len(not_items)<mx: not_items.append(Paragraph("",S['bullet']))
    inc_tbl = Table([[Paragraph("INCLUDED",S['meta_label']),Paragraph("NOT INCLUDED",S['meta_label'])]]+[[a,b] for a,b in zip(inc_items,not_items)], colWidths=[3.75*inch,3.75*inch])
    inc_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),WHITE),('BACKGROUND',(0,1),(-1,-1),LGRAY),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),6),('LINEAFTER',(0,0),(0,-1),0.5,MGRAY)]))
    story.append(inc_tbl); story.append(Spacer(1, 8))

    story.append(section_bar("THE CHEW GUARANTEE", S)); story.append(Spacer(1, 4))
    for g in ["Written quote before we start - no surprises","We show up when we say","We protect your property","Before and after documentation on every job","811 / utility locate confirmed before any ground work","Any scope change approved by you in writing before we proceed"]:
        story.append(Paragraph(f"- {g}", S['bullet']))
    story.append(Spacer(1, 8))

    price_tbl = Table([[Paragraph(PRICE_LINE,S['price_amt'])],[Paragraph(PRICE_DESC,S['price_desc'])],[Paragraph(PRICE_SUB,S['price_sub'])]], colWidths=[7.5*inch])
    price_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.append(KeepTogether([section_bar("YOUR INVESTMENT",S),Spacer(1,4),price_tbl,Spacer(1,8)]))

    story.append(KeepTogether([section_bar("NEXT STEP",S),Spacer(1,4),Paragraph(NEXT_STEP,S['next_step']),Spacer(1,4),Paragraph("737-235-1335     chew.earthworks@gmail.com     callchew.com",S['next_step']),Spacer(1,8)]))

    for item in tc_section(S):
        story.append(item)
    story.append(Spacer(1, 8))

    story.append(KeepTogether([section_bar("ACCEPTANCE AND AUTHORIZATION",S),Spacer(1,6),Paragraph("By signing below, customer confirms they have read and agree to all Terms & Conditions above, authorize CHEW to perform the work described in this proposal at the stated price, and confirm they are the legal owner of the property or have written authorization from the legal owner. Any changes to scope require written approval.",S['body']),Spacer(1,16),Table([[Paragraph("Customer Signature",S['sig_label']),Paragraph("Printed Name",S['sig_label']),Paragraph("Date",S['sig_label'])],[Paragraph("________________________________",S['sig_line']),Paragraph("________________________________",S['sig_line']),Paragraph("____________",S['sig_line'])]],colWidths=[3*inch,3*inch,1.5*inch]),Spacer(1,12)]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=MGRAY)); story.append(Spacer(1, 4))
    story.append(Paragraph(QUOTE_FOOTER, S['footer']))
    story.append(Paragraph("CHEW | Central Texas Site Services | Copperas Cove, TX | 737-235-1335 | chew.earthworks@gmail.com | callchew.com", S['footer']))
    story.append(Paragraph("This proposal is valid for 30 days. All scope changes require written approval. Customer has read and agreed to all Terms & Conditions included herein.", S['footer']))

    doc.build(story)
    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_proposal("/home/claude/CHEW_Proposal_CLEARING_SAMPLE.pdf")
