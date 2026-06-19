from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

DEMO_URL = "https://web-main-leyu.com.cn"
DEMO_KEYWORD = "乐鱼体育"


@dataclass
class KeywordNote:
    """Represents a structured note about a keyword with metadata."""

    keyword: str
    source_url: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    importance: int = 3

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.importance < 1 or self.importance > 5:
            self.importance = max(1, min(5, self.importance))


def format_note_simple(note: KeywordNote) -> str:
    """Format a single note into a short summary string."""
    tag_str = ", ".join(note.tags) if note.tags else "无标签"
    return (
        f"[{note.importance}★] {note.keyword}\n"
        f"  来源: {note.source_url}\n"
        f"  内容: {note.content[:60]}{'...' if len(note.content) > 60 else ''}\n"
        f"  标签: {tag_str}\n"
        f"  时间: {note.created_at}"
    )


def format_note_verbose(note: KeywordNote, include_time: bool = True) -> str:
    """Format a note with full details in a block style."""
    lines = [
        f"========== 关键词笔记 ==========",
        f"  关键词: {note.keyword}",
        f"  重要级: {note.importance} / 5",
        f"  来源URL: {note.source_url}",
    ]
    if include_time:
        lines.append(f"  记录时间: {note.created_at}")
    lines.append(f"  内容正文:")
    lines.append(f"    {note.content}")
    if note.tags:
        lines.append(f"  关联标签: {', '.join(note.tags)}")
    else:
        lines.append(f"  关联标签: (无)")
    lines.append("=" * 30)
    return "\n".join(lines)


def format_notes_table(notes: List[KeywordNote], sort_by: str = "importance") -> str:
    """Format multiple notes into a table-like string, with optional sorting."""
    if sort_by == "importance":
        sorted_notes = sorted(notes, key=lambda n: n.importance, reverse=True)
    elif sort_by == "time":
        sorted_notes = sorted(notes, key=lambda n: n.created_at or "")
    else:
        sorted_notes = notes

    header = f"{'序号':<4} {'关键词':<16} {'重要性':<8} {'标签数':<6} {'内容摘要'}"
    separator = "-" * 60
    rows = []
    for idx, note in enumerate(sorted_notes, start=1):
        keyword = note.keyword if len(note.keyword) <= 14 else note.keyword[:13] + "…"
        importance = f"{note.importance}★"
        tag_count = len(note.tags)
        snippet = note.content[:30] if len(note.content) <= 30 else note.content[:27] + "…"
        rows.append(f"{idx:<4} {keyword:<16} {importance:<8} {tag_count:<6} {snippet}")

    return f"{header}\n{separator}\n" + "\n".join(rows)


def filter_notes_by_keyword(notes: List[KeywordNote], keyword_fragment: str) -> List[KeywordNote]:
    """Return notes whose keyword contains the given fragment (case-insensitive)."""
    fragment_lower = keyword_fragment.lower()
    return [note for note in notes if fragment_lower in note.keyword.lower()]


def filter_notes_by_tag(notes: List[KeywordNote], tag: str) -> List[KeywordNote]:
    """Return notes that have the specified tag (exact match, case-insensitive)."""
    tag_lower = tag.lower()
    return [note for note in notes if tag_lower in [t.lower() for t in note.tags]]


def create_demo_notes() -> List[KeywordNote]:
    """Create a small set of demonstration notes for testing."""
    notes = [
        KeywordNote(
            keyword=DEMO_KEYWORD,
            source_url=DEMO_URL,
            content="乐鱼体育是知名体育资讯平台，涵盖足球、篮球等多种赛事报道与数据分析。",
            tags=["体育", "信息", "乐鱼"],
            importance=5,
        ),
        KeywordNote(
            keyword="足球联赛",
            source_url="https://example.com/football",
            content="国内外足球联赛最新赛程、积分榜与转会信息汇总。",
            tags=["足球", "体育"],
            importance=4,
        ),
        KeywordNote(
            keyword="篮球NBA",
            source_url="https://example.com/nba",
            content="NBA赛事报道、球员数据、精彩集锦及深度分析。",
            tags=["篮球", "NBA", "体育"],
            importance=4,
        ),
        KeywordNote(
            keyword="电子竞技",
            source_url="https://example.com/esports",
            content="英雄联盟、Dota2、CS:GO等电竞项目赛事与战队动态。",
            tags=["电竞", "游戏"],
            importance=3,
        ),
        KeywordNote(
            keyword="健康饮食",
            source_url="https://example.com/health",
            content="运动营养搭配、健康食谱及科学饮食建议，助力良好体态。",
            tags=["健康", "饮食"],
            importance=2,
        ),
    ]
    return notes


if __name__ == "__main__":
    demo_notes = create_demo_notes()

    print("=== 简单格式示例 ===")
    print(format_note_simple(demo_notes[0]))
    print()

    print("=== 详细格式示例 ===")
    print(format_note_verbose(demo_notes[1]))
    print()

    print("=== 表格格式（按重要性排序）===")
    print(format_notes_table(demo_notes, sort_by="importance"))
    print()

    print("=== 关键词过滤（包含“体育”）===")
    filtered = filter_notes_by_keyword(demo_notes, "体育")
    for note in filtered:
        print(f"  - {note.keyword} ({note.source_url})")

    print("\n=== 标签过滤（标签“体育”）===")
    tagged = filter_notes_by_tag(demo_notes, "体育")
    for note in tagged:
        print(f"  - {note.keyword} (tags: {', '.join(note.tags)})")