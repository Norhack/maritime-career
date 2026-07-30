from typing import List, Dict, Any
from sqlalchemy.orm import Session
from scrapers.common.base import BaseScraper
from scrapers.common.parser import JobParser
from scrapers.common.deduplicator import Deduplicator
from backend.models.job import Job
from backend.models.company import Company
from backend.database.connection import SessionLocal
from datetime import datetime
import hashlib


class LinkedInScraper(BaseScraper):
    """Stub scraper for LinkedIn jobs."""

    def __init__(self):
        super().__init__(source_name="linkedin", rate_limit_per_hour=30)

    def fetch(self) -> List[Dict[str, Any]]:
        # Placeholder implementation: return a deterministic sample payload
        return [
            {
                "title": "Technical Superintendent",
                "company": "Maersk",
                "location": "Oslo, Norway",
                "description": "Lead vessel maintenance and technical operations for a maritime fleet.",
                "url": "https://example.com/jobs/linkedin-1",
                "salary": "Competitive",
                "employment_type": "Full-time",
                "published_date": "2026-07-30T00:00:00",
            }
        ]

    def parse(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        title = JobParser.clean_text(raw_item.get("title", ""))
        company = JobParser.clean_text(raw_item.get("company", ""))
        location = JobParser.clean_text(raw_item.get("location", ""))
        description = JobParser.clean_text(raw_item.get("description", ""))
        salary = JobParser.extract_salary(description)
        content_text = "\n".join([title, company, location, description])
        content_hash = Deduplicator.compute_hash(content_text)

        return {
            "source": "linkedin",
            "company": company,
            "title": title,
            "location": location,
            "description": description,
            "salary": salary or raw_item.get("salary"),
            "employment_type": raw_item.get("employment_type", "Full-time"),
            "url": raw_item.get("url"),
            "published_date": raw_item.get("published_date"),
            "hash": content_hash,
        }

    def save_to_db(self, db: Session, parsed_item: Dict[str, Any]) -> bool:
        if Deduplicator.is_job_duplicate(
            db,
            parsed_item["source"],
            parsed_item["company"],
            parsed_item["title"],
            parsed_item["location"],
            parsed_item["url"],
            parsed_item["hash"],
        ):
            return False

        job = Job(
            source=parsed_item["source"],
            company=parsed_item["company"],
            title=parsed_item["title"],
            location=parsed_item["location"],
            description=parsed_item["description"],
            salary=parsed_item.get("salary"),
            employment_type=parsed_item.get("employment_type"),
            url=parsed_item["url"],
            published_date=datetime.fromisoformat(parsed_item["published_date"])
            if parsed_item.get("published_date")
            else None,
            hash=parsed_item["hash"],
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        Deduplicator.get_or_create_company(
            db,
            parsed_item["company"],
            industry="Maritime",
            headquarters=None,
            website=None,
        )
        return True


if __name__ == "__main__":
    db = SessionLocal()
    scraper = LinkedInScraper()
    scraper.run(db)
    db.close()
