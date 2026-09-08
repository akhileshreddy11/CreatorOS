from pathlib import Path

from app.services.mission_executor import MissionExecutor
from app.tasks.task import Task


class FakeContentEmployee:
    def create_content(self, task, feedback=None):
        return {
            "hook": "Your first gym visit can be simple.",
            "script": "Know what to bring and what to ask before your trial class.",
            "caption": "A practical first-visit checklist.",
            "cta": "Message the gym to ask about a trial class.",
            "hashtags": ["#HyderabadFitness", "#GymTrial"],
        }


class FakeValidator:
    def validate(self, result, task):
        return {"status": "VALID", "valid": True, "errors": [], "warnings": [], "quality_score": 95}


class FakeReelGenerator:
    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    def __init__(self, output_path):
        self.output_path = Path(output_path)
        self.calls = 0

    def create_reel(self, content, output_name="creatoros_reel.mp4", language="en"):
        self.calls += 1
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_bytes(b"valid mp4 placeholder")
        return str(self.output_path)


class FakeArtifactPersistence:
    def __init__(self):
        self.saved = []

    def persist_content(self, task, result, validation):
        self.saved.append((task, result, validation))
        return 101


def test_reel_task_renders_after_validation_and_remains_approval_gated(tmp_path):
    reel = FakeReelGenerator(tmp_path / "mission_reel.mp4")
    persistence = FakeArtifactPersistence()
    task = Task(
        title="Create Content #1",
        description="Instagram Reel-ready content. Render the validated vertical video.",
        assigned_by="COO",
        assigned_to="Content Employee",
        priority="High",
    )

    result = MissionExecutor(
        content_employee=FakeContentEmployee(),
        product_employee=FakeContentEmployee(),
        validator=FakeValidator(),
        reel_generator=reel,
        artifact_persistence=persistence,
    ).execute_task(task)

    assert result["status"] == "Completed"
    assert result["artifact_status"] == "awaiting_approval"
    assert result["approval_status"] == "needs_review"
    assert result["media_type"] == "video/mp4"
    assert result["media_path"].endswith("mission_reel.mp4")
    assert reel.calls == 1
    assert Path(result["media_path"]).is_file()
    assert persistence.saved[0][1]["media"]["media_type"] == "video/mp4"


def test_reel_generator_scene_helpers_handle_short_and_multisentence_scripts(tmp_path):
    from app.services.reels.reel_generator import ReelGenerator

    generator = ReelGenerator(
        voice_generator=object(),
        visual_engine=object(),
        output_dir=tmp_path,
    )

    scenes = generator._split_script("First sentence. Second sentence! Third sentence?")
    durations = generator._calculate_scene_durations(scenes, 12)

    assert scenes
    assert len(scenes) == len(durations)
    assert all(duration > 0 for duration in durations)
    assert round(sum(durations), 6) == 12
