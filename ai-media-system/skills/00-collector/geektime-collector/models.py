from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class VideoInfo:
    url: str
    transcript: Optional[str] = None
    duration: Optional[int] = None  # in seconds


@dataclass
class Article:
    id: str
    type: str = "geektime"
    url: str = ""
    title: str = ""
    author: str = ""
    published_at: Optional[datetime] = None
    collected_at: datetime = field(default_factory=datetime.now)
    content: str = ""
    images: List[str] = field(default_factory=list)
    video: Optional[VideoInfo] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "images": self.images,
            "collected_at": self.collected_at.isoformat()
        }
        if self.published_at:
            result["published_at"] = self.published_at.isoformat()
        if self.video:
            result["video"] = {
                "url": self.video.url,
                "transcript": self.video.transcript,
                "duration": self.video.duration
            }
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class CollectionResult:
    success: bool
    article: Optional[Article] = None
    error: Optional[str] = None
