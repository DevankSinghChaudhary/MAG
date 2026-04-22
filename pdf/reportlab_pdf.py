import re
import unicodedata
from html import unescape
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Flowable, HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


UNICODE_REPLACEMENTS = str.maketrans(
    {
        "\u00A0": " ",
        "\u00AD": "-",
        "\u2007": " ",
        "\u2009": " ",
        "\u200A": " ",
        "\u202F": " ",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201C": '"',
        "\u201D": '"',
    }
)


MOCK_PDF_DATA = [
    {
        "Gap_name": "Membership Gap",
        "Observation": (
            "Your current monetization structure depends on one-time offers and sporadic launches, "
            "which means your most engaged followers do not have a recurring way to stay close to "
            "your work. There is interest and trust, but no consistent container that keeps people "
            "connected after the first purchase."
        ),
        "Impact": (
            "This limits revenue predictability and makes retention harder because each campaign has "
            "to restart momentum from scratch. Over time, that creates higher pressure on content "
            "performance and leaves loyal audience members without a clear next step."
        ),
        "Recommendation": (
            "Introduce a recurring membership with monthly value such as exclusive trainings, "
            "templates, Q&A sessions, or guided implementation support. This gives your audience a "
            "clear continuity path while creating a steadier revenue base."
        ),
    },
    {
        "Gap_name": "Digital Product Ladder Gap",
        "Observation": (
            "The current offer structure does not create an easy entry point for warm followers who "
            "are interested but not yet ready for a premium purchase. The jump from free content to "
            "your main paid solution feels too large."
        ),
        "Impact": (
            "Without a lower-friction product, you lose conversions from people who are willing to "
            "buy but need a smaller first commitment. That reduces total customer volume and weakens "
            "the path toward higher-ticket conversion later."
        ),
        "Recommendation": (
            "Add a compact starter product such as a workbook, mini-course, checklist bundle, or "
            "guided template pack that solves one focused problem. Position it as the first step into "
            "your ecosystem and connect it clearly to your larger offer."
        ),
    },
    {
        "Gap_name": "Community Retention Gap",
        "Observation": (
            "Your audience receives strong educational value, but there is no built-in peer "
            "interaction, accountability loop, or ongoing implementation support after consumption. "
            "That makes the experience feel transactional instead of relational."
        ),
        "Impact": (
            "This reduces repeat engagement and lowers lifetime value because people may benefit from "
            "the content once without developing a stronger long-term connection to your brand. It can "
            "also make referrals less likely because users are not participating in a shared "
            "experience."
        ),
        "Recommendation": (
            "Create a structured follow-through layer with cohort check-ins, discussion prompts, "
            "implementation challenges, or member-only office hours. A community-based retention "
            "mechanism will strengthen transformation, loyalty, and repeat monetization opportunities."
        ),
    },
]


def _format_text(value):
    text = _clean_text(value)
    return escape(text).replace("\n", "<br/>")


def _clean_text(value):
    text = "" if value is None else str(value)
    text = unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(UNICODE_REPLACEMENTS)
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", " ")
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"<[^>\n]+>", "", text)
    text = re.sub(r"`{1,3}", "", text)
    text = re.sub(r"(\*\*|__|\*|_|~~)", "", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"(?<=\w)\n(?=\w)", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _estimate_revenue(followers):
    try:
        total_followers = int(followers)
    except (TypeError, ValueError):
        return None

    if total_followers <= 0:
        return None

    low_estimate = total_followers * 0.01 * 79
    high_estimate = total_followers * 0.02 * 99

    return {
        "followers": total_followers,
        "low": low_estimate,
        "high": high_estimate,
    }


def _format_currency(value):
    return f"${value:,.0f}"


class GapCard(Flowable):
    def __init__(self, gap, gap_name_style, body_style, impact_style, recommendation_style):
        super().__init__()
        self.gap = gap or {}
        self.gap_name_style = gap_name_style
        self.body_style = body_style
        self.impact_style = impact_style
        self.recommendation_style = recommendation_style
        self.card_padding = 14
        self.corner_radius = 12
        self.card_background = colors.HexColor("#FFFFFF")
        self.card_border = colors.HexColor("#D1D5DB")
        self.impact_accent = colors.HexColor("#C94B4B")
        self.recommendation_accent = colors.HexColor("#2b9dfb")
        self.impact_background = colors.HexColor("#FCEEEE")
        self.recommendation_background = colors.HexColor("#D9F0FF")
        self.corner_radius_line = 0
        self._table = None
        self._inner_width = None

    def _build_table(self, inner_width):
        if self._table is not None and self._inner_width == inner_width:
            return

        rows = [
            [Paragraph(_format_text(self.gap.get("Gap_name", "")), self.gap_name_style)],
            [Paragraph(f"<b>Observation:</b> {_format_text(self.gap.get('Observation', ''))}", self.body_style)],
            [Paragraph(f"<b>Impact:</b> {_format_text(self.gap.get('Impact', ''))}", self.impact_style)],
            [Spacer(1, 6)],
            [Paragraph(f"<b>Recommendation:</b> {_format_text(self.gap.get('Recommendation', ''))}", self.recommendation_style)],
        ]

        table = Table(
            rows,
            colWidths=[inner_width],
            hAlign="LEFT",
            splitByRow=0,
        )
        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, 0), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                    ("BACKGROUND", (0, 2), (-1, 2), self.impact_background),
                    ("BACKGROUND", (0, 4), (-1, 4), self.recommendation_background),
                    ("LEFTPADDING", (0, 2), (-1, 2), 14),
                    ("LEFTPADDING", (0, 4), (-1, 4), 14),
                    ("LEFTPADDING", (0, 3), (-1, 3), 0),
                    ("RIGHTPADDING", (0, 3), (-1, 3), 0),
                    ("TOPPADDING", (0, 3), (-1, 3), 0),
                    ("BOTTOMPADDING", (0, 3), (-1, 3), 0),
                    ("LINEBEFORE", (0, 2), (0, 2), 4, self.impact_accent, self.corner_radius_line),
                    ("LINEBEFORE", (0, 4), (0, 4), 4, self.recommendation_accent, self.corner_radius_line),
                ]
            )
        )

        self._table = table
        self._inner_width = inner_width

    def wrap(self, availWidth, availHeight):
        inner_width = max(availWidth - (self.card_padding * 2), 100)
        self._build_table(inner_width)
        table_width, table_height = self._table.wrap(inner_width, availHeight)
        self.width = table_width + (self.card_padding * 2)
        self.height = table_height + (self.card_padding * 2)
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.card_background)
        self.canv.setStrokeColor(self.card_border)
        self.canv.roundRect(0, 0, self.width, self.height, self.corner_radius, fill=1, stroke=1)
        self._table.drawOn(self.canv, self.card_padding, self.card_padding)
        self.canv.restoreState()


def create_pdf(data, name, followers=None, output_file=None, carousel_data=None):
    if not data:
        raise ValueError("No data available for PDF generation!")

    if not name or not str(name).strip():
        raise ValueError("Name is required for PDF generation!")

    if isinstance(data, dict):
        data = [data]

    output_file = output_file or f"{name}_audit.pdf"
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "AuditTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "AuditSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "AuditSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#111827"),
        spaceAfter=14,
    )
    gap_name_style = ParagraphStyle(
        "GapName",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#111827"),
    )
    body_style = ParagraphStyle(
        "GapBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#374151"),
    )
    impact_style = ParagraphStyle(
        "ImpactBody",
        parent=body_style,
        textColor=colors.HexColor("#A63D3D"),
    )
    recommendation_style = ParagraphStyle(
        "RecommendationBody",
        parent=body_style,
        textColor=colors.HexColor("#404040"),
    )
    revenue_title_style = ParagraphStyle(
        "RevenueTitle",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#14532D"),
    )
    revenue_body_style = ParagraphStyle(
        "RevenueBody",
        parent=body_style,
        textColor=colors.HexColor("#166534"),
    )
    carousel_style = ParagraphStyle(
        "CarouselDay",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#3B82F6"),
    )
    revenue_estimate = _estimate_revenue(followers)

    story = [
        HRFlowable(
            width="75%",
            thickness=0.5,
            color=colors.HexColor("#000000"),
            lineCap="round",
            spaceBefore=0,
            spaceAfter=10,
        ),
        Paragraph("Monetization Audit Report", title_style),
        Paragraph(f"Prepared for: {_format_text(name)}", subtitle_style),
    ]

    if revenue_estimate:
        followers_text = _format_text(f"{revenue_estimate['followers']:,}")
        revenue_range_text = f"{_format_currency(revenue_estimate['low'])} - {_format_currency(revenue_estimate['high'])}"
        revenue_rows = [
            [Paragraph("Estimated Revenue Potential", revenue_title_style)],
            [
                Paragraph(
                    (
                        f"Based on {followers_text} followers, a 1-2% conversion on a $79-$99 offer "
                        f"suggests an estimated revenue range of <b>{revenue_range_text}</b>. "
                        f"See below for how I can help you achieve this potential."
                    ),
                    revenue_body_style,
                )
            ],
        ]
        revenue_table = Table(
            revenue_rows,
            colWidths="100%",
            hAlign="LEFT",
        )
        revenue_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ECFDF3")),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ]
            )
        )

        story.append(Spacer(1, 10))
        story.append(
            KeepTogether(
                [
                    Spacer(1, 5),
                    revenue_table,
                    Spacer(1, 15),
                ]
            )
        )

    story.extend([
        Paragraph("Monetization Gaps Identified", section_style),
        Spacer(1, 5),
    ])
    for index, gap in enumerate(data):
        if index:
            story.append(Spacer(1, 10)),
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.HexColor("#6B7280"),
                    lineCap="round",
                    spaceBefore=0,
                    spaceAfter=0,
                )
            )
            story.append(Spacer(1, 14))
        story.append(GapCard(gap, gap_name_style, body_style, impact_style, recommendation_style))

    # Add Instagram Story Sequences section
    if carousel_data:
        story.append(Spacer(1, 18))
        story.append(Paragraph("Instagram Story Sequences: 7-Day Product Testing", section_style))
        story.append(Spacer(1, 8))
        
        carousel_title = carousel_data.get("carousel_title", "7-Day Product Testing")
        selected_product = carousel_data.get("selected_product", "Digital Product")
        
        story.append(Paragraph(f"<b>Campaign:</b> {_format_text(carousel_title)}", body_style))
        story.append(Paragraph(f"<b>Product Focus:</b> {_format_text(selected_product)}", body_style))
        story.append(Spacer(1, 12))
        
        # Add strategy overview
        story.append(Paragraph(
            "<b>Strategy Overview:</b><br/>This 7-day Instagram story sequence tests your product's market demand through authentic storytelling. Days 1-2 build awareness, Days 3-5 deliver value and proof, Days 6-7 drive conversions.",
            body_style
        ))
        story.append(Spacer(1, 12))
        
        for day in range(1, 8):
            day_key = f"day_{day}"
            if day_key in carousel_data:
                day_data = carousel_data[day_key]
                focus = day_data.get("focus", "")
                content_idea = day_data.get("content_idea", "")
                hook = day_data.get("hook", "")
                call_to_action = day_data.get("call_to_action", "")
                
                story.append(Paragraph(f"<b>Day {day}: {_format_text(focus)}</b>", carousel_style))
                story.append(Paragraph(f"<b>Story Idea:</b> {_format_text(content_idea)}", body_style))
                story.append(Paragraph(f"<b>Hook:</b> {_format_text(hook)}", body_style))
                story.append(Paragraph(f"<b>CTA:</b> {_format_text(call_to_action)}", body_style))
                if day < 7:
                    story.append(Spacer(1, 8))

    doc.build(story)
    return output_file


def create_mock_pdf(name="Preview Creator", followers=25000, output_file="mock_preview_audit.pdf"):
    return create_pdf(MOCK_PDF_DATA, name, followers=followers, output_file=output_file)
