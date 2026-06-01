from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TranscriptSegment:
    index: int
    start_seconds: float
    end_seconds: float
    text: str

    @property
    def duration_seconds(self) -> float:
        return max(0.0, self.end_seconds - self.start_seconds)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class TranscriptBlock:
    start_seconds: float
    end_seconds: float
    text: str
    source_indexes: list[int]

    @property
    def duration_seconds(self) -> float:
        return max(0.0, self.end_seconds - self.start_seconds)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class Chapter:
    start_seconds: float
    title: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class HookCandidate:
    id: str
    start_seconds: float
    end_seconds: float
    score: float
    reason: str
    transcript: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class SegmentCandidate:
    id: str
    start_seconds: float
    end_seconds: float
    score: float
    reason: str
    transcript: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class AnalysisResult:
    chapters: list[Chapter]
    hooks: list[HookCandidate]
    broll: list[SegmentCandidate]
    shorts: list[SegmentCandidate]
    youtube_description: str
    transcript_blocks: list[TranscriptBlock]

    def to_dict(self) -> dict[str, object]:
        return {
            "chapters": [chapter.to_dict() for chapter in self.chapters],
            "hooks": [hook.to_dict() for hook in self.hooks],
            "broll": [item.to_dict() for item in self.broll],
            "shorts": [item.to_dict() for item in self.shorts],
            "youtube_description": self.youtube_description,
            "transcript_blocks": [block.to_dict() for block in self.transcript_blocks],
        }
