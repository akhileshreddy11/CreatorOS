from __future__ import annotations

from app.database import Approval, ContentDraft, SessionLocal


class ArtifactPersistence:
    """
    Persists validated AI employee artifacts into CreatorOS.

    MissionExecutor handles execution and validation.
    ArtifactPersistence handles database persistence and approval records.
    """

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def persist_content(
        self,
        task,
        result: dict,
        validation: dict,
    ) -> int:

        db = self.session_factory()

        try:
            draft = ContentDraft(
                title=task.title or "CreatorOS Content Draft",
                prompt=task.description or "",
                platform="Instagram",
                language="en",
                content=result,
                validation=validation,
                status="needs_review",
                action_class="approval_required",
            )

            db.add(draft)
            db.flush()

            approval = Approval(
                resource_type="content_draft",
                resource_id=draft.id,
                status="needs_review",
                action_class="approval_required",
                reason=(
                    "Validated AI-generated content "
                    "requires owner approval."
                ),
            )

            db.add(approval)

            db.commit()
            db.refresh(draft)

            return draft.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def persist_product(
        self,
        task,
        result: dict,
        validation: dict,
    ) -> int:

        db = self.session_factory()

        try:
            draft = ContentDraft(
                title=task.title or (result.get("product_name") if isinstance(result, dict) else None) or "CreatorOS Product Playbook",
                prompt=task.description or "",
                platform="Playbook",
                language="en",
                content=result,
                validation=validation,
                status="needs_review",
                action_class="approval_required",
            )

            db.add(draft)
            db.flush()

            approval = Approval(
                resource_type="content_draft",
                resource_id=draft.id,
                status="needs_review",
                action_class="approval_required",
                reason=(
                    "Validated AI-generated campaign asset "
                    "requires owner approval."
                ),
            )

            db.add(approval)

            db.commit()
            db.refresh(draft)

            return draft.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()