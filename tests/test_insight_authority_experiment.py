from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import insight_authority_experiment as experiment  # noqa: E402


def packet(**overrides: object) -> experiment.AuthorityPacket:
    payload = {
        "slug": "trust-boundary",
        "title": "LLM Orchestration Fails | A Cinematic Research Brief",
        "claim": "Teams trusted the plan before checking the boundary.",
        "evidence": ["The run failed after the tool boundary was crossed."],
        "thumbnail_text": "Trust Boundary",
        "source_url": "https://example.com/source",
    }
    payload.update(overrides)
    return experiment.coerce_packet(payload)


class FakeRequest:
    def __init__(self, response):
        self.response = response

    def execute(self):
        if callable(self.response):
            return self.response()
        return self.response


class FakeVideosResource:
    def __init__(self, youtube: "FakeYouTubeClient") -> None:
        self.youtube = youtube

    def list(self, *, part: str, id: str) -> FakeRequest:
        self.youtube.list_calls.append({"part": part, "id": id})

        def response() -> dict[str, object]:
            video = self.youtube.video_state.get(id)
            return {"items": [copy.deepcopy(video)] if video else []}

        return FakeRequest(response)

    def update(self, *, part: str, body: dict[str, object]) -> FakeRequest:
        self.youtube.update_calls.append({"part": part, "body": copy.deepcopy(body)})
        video_id = str(body["id"])
        snippet = copy.deepcopy(body["snippet"])
        self.youtube.video_state[video_id]["snippet"] = snippet
        return FakeRequest({"id": video_id, "snippet": copy.deepcopy(snippet)})


class FakeThumbnailsResource:
    def __init__(self, youtube: "FakeYouTubeClient") -> None:
        self.youtube = youtube

    def set(self, *, videoId: str, media_body: object) -> FakeRequest:
        self.youtube.thumbnail_calls.append({"videoId": videoId, "media_body": media_body})
        return FakeRequest({"videoId": videoId, "uploaded": True})


class FakeCommentThreadsResource:
    def __init__(self, youtube: "FakeYouTubeClient") -> None:
        self.youtube = youtube

    def list(self, **kwargs: object) -> FakeRequest:
        self.youtube.comment_list_calls.append(copy.deepcopy(kwargs))
        if self.youtube.comment_list_error:
            raise self.youtube.comment_list_error
        video_id = str(kwargs["videoId"])
        comments = self.youtube.comment_threads.get(video_id, [])
        page_token = kwargs.get("pageToken")
        start = int(str(page_token)) if page_token else 0
        max_results = int(str(kwargs.get("maxResults", 100)))
        page = comments[start : start + max_results]
        next_start = start + max_results
        response: dict[str, object] = {
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": text,
                            }
                        }
                    }
                }
                for text in page
            ]
        }
        if next_start < len(comments):
            response["nextPageToken"] = str(next_start)
        return FakeRequest(response)

    def insert(self, *, part: str, body: dict[str, object]) -> FakeRequest:
        self.youtube.comment_insert_calls.append({"part": part, "body": copy.deepcopy(body)})
        snippet = body["snippet"]
        video_id = str(snippet["videoId"])
        text = str(snippet["topLevelComment"]["snippet"]["textOriginal"])
        self.youtube.comment_threads.setdefault(video_id, []).append(text)
        return FakeRequest({"id": "comment-1", "snippet": copy.deepcopy(body["snippet"])})


class FakeYouTubeClient:
    def __init__(self) -> None:
        self.video_state = {
            "abc12345678": {
                "id": "abc12345678",
                "snippet": {
                    "title": "Old title",
                    "description": "Old description",
                    "tags": ["old-tag"],
                    "categoryId": "28",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en-US",
                    "publishedAt": "2026-05-01T00:00:00Z",
                    "channelId": "channel-1",
                },
                "status": {"privacyStatus": "public"},
            }
        }
        self.list_calls: list[dict[str, object]] = []
        self.update_calls: list[dict[str, object]] = []
        self.thumbnail_calls: list[dict[str, object]] = []
        self.comment_list_calls: list[dict[str, object]] = []
        self.comment_insert_calls: list[dict[str, object]] = []
        self.comment_threads: dict[str, list[str]] = {"abc12345678": []}
        self.comment_list_error: Exception | None = None

    def videos(self) -> FakeVideosResource:
        return FakeVideosResource(self)

    def thumbnails(self) -> FakeThumbnailsResource:
        return FakeThumbnailsResource(self)

    def commentThreads(self) -> FakeCommentThreadsResource:
        return FakeCommentThreadsResource(self)


class InsightAuthorityExperimentTests(unittest.TestCase):
    maxDiff = None

    def test_forbidden_wrappers_block_packet_source(self) -> None:
        subject = packet(description="As an AI-generated research brief, in this video we explain the result.")

        issues = experiment.validate_packet(subject)

        self.assertTrue(any("forbidden wrapper phrase" in issue["message"] for issue in issues))

    def test_thumbnail_text_is_limited_to_three_words(self) -> None:
        subject = packet(thumbnail_text="Too Many Thumbnail Words")

        issues = experiment.validate_packet(subject)

        self.assertIn(
            {
                "field": "thumbnail_text",
                "message": "thumbnail text must be 3 words or fewer",
            },
            issues,
        )

    def test_metadata_rendering_removes_wrappers_and_jargon(self) -> None:
        subject = packet(
            title="LLM Orchestration Fails | A Cinematic Research Brief",
            description="This video explores AI workflow governance.",
        )

        metadata = experiment.render_metadata(subject)
        rendered = f"{metadata['title']}\n{metadata['description']}".lower()

        self.assertNotIn("cinematic research brief", rendered)
        self.assertNotIn("llm", rendered)
        self.assertNotIn("orchestration", rendered)
        self.assertNotIn("this video", rendered)
        self.assertNotIn("ai", {word.lower() for word in experiment.words(rendered.split("source:")[0])})
        self.assertIn("coordination", rendered)
        self.assertIn("work process control", rendered)

    def test_cadence_governor_defaults_longform_to_tuesday_thursday(self) -> None:
        packets = [
            packet(slug="first", title="First", thumbnail_text="First"),
            packet(slug="second", title="Second", thumbnail_text="Second"),
            packet(slug="third", title="Third", thumbnail_text="Third"),
        ]

        schedule = experiment.governed_schedule(
            packets,
            start_at=datetime(2026, 5, 9, 0, 0, tzinfo=timezone.utc),
            existing=[],
            config=experiment.CadenceConfig(
                timezone_name="UTC",
                slot_times=("09:00",),
                max_per_day=1,
                min_hours_between=3,
            ),
        )

        self.assertEqual(schedule["first"].isoformat(), "2026-05-12T09:00:00+00:00")
        self.assertEqual(schedule["second"].isoformat(), "2026-05-14T09:00:00+00:00")
        self.assertEqual(schedule["third"].isoformat(), "2026-05-19T09:00:00+00:00")

    def test_cadence_governor_ignores_off_day_longform_publish_at(self) -> None:
        packets = [
            packet(
                slug="preferred",
                title="Preferred",
                thumbnail_text="Preferred",
                publish_at="2026-05-11T09:00:00Z",
            )
        ]

        schedule = experiment.governed_schedule(
            packets,
            start_at=datetime(2026, 5, 9, 0, 0, tzinfo=timezone.utc),
            existing=[],
            config=experiment.CadenceConfig(timezone_name="UTC", slot_times=("09:00",)),
        )

        self.assertEqual(schedule["preferred"].isoformat(), "2026-05-12T09:00:00+00:00")

    def test_research_snapshot_short_requires_explicit_format_for_off_day(self) -> None:
        explicit_short = packet(
            slug="snapshot",
            title="Snapshot",
            thumbnail_text="Snapshot",
            content_format="research snapshot short",
        )
        implicit_short = packet(slug="title-short", title="Title Short #shorts", thumbnail_text="Title Short")

        explicit_schedule = experiment.governed_schedule(
            [explicit_short],
            start_at=datetime(2026, 5, 9, 0, 0, tzinfo=timezone.utc),
            existing=[],
            config=experiment.CadenceConfig(timezone_name="UTC", slot_times=("09:00",)),
        )
        implicit_schedule = experiment.governed_schedule(
            [implicit_short],
            start_at=datetime(2026, 5, 9, 0, 0, tzinfo=timezone.utc),
            existing=[],
            config=experiment.CadenceConfig(timezone_name="UTC", slot_times=("09:00",)),
        )

        self.assertEqual(explicit_schedule["snapshot"].isoformat(), "2026-05-09T09:00:00+00:00")
        self.assertEqual(implicit_schedule["title-short"].isoformat(), "2026-05-12T09:00:00+00:00")

    def test_apply_writes_emit_publish_plan_and_thumbnail_png(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = SimpleNamespace(
                packets=root / "packets.yaml",
                out_dir=root / "out",
                plan_file=None,
                emit_plan_file=None,
                publish_plan_file=None,
                history=[],
                start_at="2026-05-09T00:00:00Z",
                timezone="UTC",
                slots=["09:00"],
                max_per_day=1,
                min_hours_between=3,
                privacy="private",
                skip_thumbnails=False,
                apply=True,
            )
            args.packets.write_text(
                yaml.safe_dump(
                    {
                        "packets": [
                            {
                                "slug": "trust-boundary",
                                "title": "The Boundary Failed | AI Explained",
                                "claim": "Teams trusted the plan before checking the boundary.",
                                "evidence": ["The run failed after the tool boundary was crossed."],
                                "thumbnail_text": "Trust Boundary",
                            }
                        ]
                    },
                    sort_keys=False,
                )
            )

            plan = experiment.run(args)

            self.assertTrue(plan["validation"]["ok"])
            publish_item = plan["items"][0]["publish"]
            self.assertEqual(publish_item["scheduled_at"], "2026-05-12T09:00:00Z")
            self.assertEqual(publish_item["allowed_weekdays"], ["tuesday", "thursday"])
            self.assertTrue((args.out_dir / "insight_authority_plan.json").exists())
            self.assertTrue((args.out_dir / "emit_plan.json").exists())
            self.assertTrue((args.out_dir / "publish_plan.json").exists())
            png_path = args.out_dir / "thumbnails" / "trust-boundary.png"
            self.assertEqual(png_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_apply_youtube_updates_snippet_thumbnail_comment_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = SimpleNamespace(
                packets=root / "packets.yaml",
                out_dir=root / "out",
                plan_file=None,
                emit_plan_file=None,
                publish_plan_file=None,
                youtube_report_file=None,
                history=[],
                start_at="2026-05-09T00:00:00Z",
                timezone="UTC",
                slots=["09:00"],
                max_per_day=1,
                min_hours_between=3,
                privacy="public",
                skip_thumbnails=False,
                apply=True,
                apply_youtube=True,
            )
            args.packets.write_text(
                yaml.safe_dump(
                    {
                        "packets": [
                            {
                                "slug": "trust-boundary",
                                "youtube_video_id": "abc12345678",
                                "package": "publications/example",
                                "title": "The Boundary Failed | AI Explained",
                                "claim": "Teams trusted the plan before checking the boundary.",
                                "evidence": ["The run failed after the tool boundary was crossed."],
                                "thumbnail_text": "Trust Boundary",
                                "description": "Boundary checks should happen before delegation.",
                                "author_note": "Keep the operating claim tied to the readback.",
                                "technical_dilemma": "What should own the boundary when the plan and the tool disagree?",
                                "pinned_comment": "Technical dilemma: what should own the boundary when the plan and the tool disagree?",
                                "source_url": "https://example.com/source",
                                "research_breakdown_url": "https://example.com/research",
                                "tags": ["Boundary Checks", "AI"],
                            }
                        ]
                    },
                    sort_keys=False,
                )
            )
            youtube = FakeYouTubeClient()

            def fake_media_upload(path: Path) -> dict[str, str]:
                return {"path": str(path), "mimetype": "image/png"}

            plan = experiment.run(
                args,
                youtube_client=youtube,
                media_upload_factory=fake_media_upload,
            )

            report_path = args.out_dir / "youtube_mutation_report.json"
            report = json.loads(report_path.read_text())
            self.assertTrue(plan["youtube_mutations"])
            self.assertIsNone(plan["items"][0]["publish"]["scheduled_at"])
            self.assertEqual(plan["items"][0]["publish"]["mutation"], "youtube_apply")
            self.assertEqual(report["items"][0]["status"], "applied")
            self.assertEqual(report["items"][0]["pin_status"], experiment.PIN_STATUS_BLOCKED)
            self.assertEqual(len(youtube.list_calls), 2)
            self.assertEqual(len(youtube.comment_list_calls), 1)
            self.assertEqual(youtube.comment_list_calls[0]["videoId"], "abc12345678")

            self.assertEqual(len(youtube.update_calls), 1)
            update_body = youtube.update_calls[0]["body"]
            snippet = update_body["snippet"]
            self.assertEqual(update_body["id"], "abc12345678")
            self.assertEqual(snippet["title"], "The Boundary Failed")
            self.assertEqual(snippet["categoryId"], "28")
            self.assertEqual(snippet["defaultLanguage"], "en")
            self.assertEqual(snippet["defaultAudioLanguage"], "en-US")
            self.assertNotIn("channelId", snippet)
            self.assertNotIn("publishedAt", snippet)
            self.assertIn("rootedlayers", snippet["tags"])
            self.assertIn("boundary-checks", snippet["tags"])

            self.assertEqual(len(youtube.thumbnail_calls), 1)
            thumbnail_call = youtube.thumbnail_calls[0]
            self.assertEqual(thumbnail_call["videoId"], "abc12345678")
            self.assertEqual(
                thumbnail_call["media_body"]["path"],
                str(args.out_dir / "thumbnails" / "trust-boundary.png"),
            )

            self.assertEqual(len(youtube.comment_insert_calls), 1)
            comment_body = youtube.comment_insert_calls[0]["body"]
            comment_snippet = comment_body["snippet"]
            self.assertEqual(comment_snippet["videoId"], "abc12345678")
            comment_text = comment_snippet["topLevelComment"]["snippet"]["textOriginal"]
            self.assertIn("Technical dilemma:", comment_text)
            self.assertEqual(report["items"][0]["after"]["title"], "The Boundary Failed")

    def test_apply_youtube_skips_duplicate_top_level_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            out_dir = root / "out"
            thumbnail_dir = out_dir / "thumbnails"
            thumbnail_dir.mkdir(parents=True)
            (thumbnail_dir / "trust-boundary.png").write_bytes(b"thumbnail")
            subject = packet(
                youtube_video_id="abc12345678",
                package="publications/example",
                description="Boundary checks should happen before delegation.",
                author_note="Keep the operating claim tied to the readback.",
                technical_dilemma="What should own the boundary when the plan and the tool disagree?",
                pinned_comment="Technical dilemma: what should own the boundary when the plan and the tool disagree?",
                research_breakdown_url="https://example.com/research",
                tags=["Boundary Checks", "AI"],
            )
            youtube = FakeYouTubeClient()
            youtube.comment_threads["abc12345678"] = [experiment.render_technical_comment(subject)]

            report = experiment.apply_youtube_mutations(
                [subject],
                validation=experiment.validate_packets([subject]),
                out_dir=out_dir,
                youtube=youtube,
                media_upload_factory=lambda path: {"path": str(path)},
            )

            item = report["items"][0]
            self.assertEqual(item["status"], "applied")
            self.assertTrue(item["comment"]["already_exists"])
            self.assertFalse(item["comment"]["posted"])
            self.assertIsNone(item["comment"]["response"])
            self.assertEqual(len(youtube.comment_list_calls), 1)
            self.assertEqual(len(youtube.comment_insert_calls), 0)
            self.assertEqual(len(youtube.update_calls), 1)
            self.assertEqual(len(youtube.thumbnail_calls), 1)

    def test_apply_youtube_blocks_comment_when_existing_comments_cannot_be_listed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            out_dir = root / "out"
            thumbnail_dir = out_dir / "thumbnails"
            thumbnail_dir.mkdir(parents=True)
            (thumbnail_dir / "trust-boundary.png").write_bytes(b"thumbnail")
            subject = packet(
                youtube_video_id="abc12345678",
                package="publications/example",
                description="Boundary checks should happen before delegation.",
                pinned_comment="Technical dilemma: what should own the boundary when the plan and the tool disagree?",
            )
            youtube = FakeYouTubeClient()
            youtube.comment_list_error = RuntimeError("commentThreads.list unavailable")

            report = experiment.apply_youtube_mutations(
                [subject],
                validation=experiment.validate_packets([subject]),
                out_dir=out_dir,
                youtube=youtube,
                media_upload_factory=lambda path: {"path": str(path)},
            )

            item = report["items"][0]
            self.assertEqual(item["status"], "blocked")
            self.assertEqual(item["pin_status"], experiment.PIN_STATUS_BLOCKED)
            self.assertIn("could not list existing top-level comments", item["issues"][0]["message"])
            self.assertIn("commentThreads.list unavailable", item["issues"][0]["message"])
            self.assertEqual(len(youtube.comment_list_calls), 1)
            self.assertEqual(len(youtube.comment_insert_calls), 0)
            self.assertEqual(len(youtube.update_calls), 0)
            self.assertEqual(len(youtube.thumbnail_calls), 0)

    def test_repair_packet_plan_is_metadata_only_without_future_release_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = SimpleNamespace(
                packets=root / "packets.yaml",
                out_dir=root / "out",
                plan_file=None,
                emit_plan_file=None,
                publish_plan_file=None,
                youtube_report_file=None,
                history=[],
                start_at="2026-05-09T00:00:00Z",
                timezone="UTC",
                slots=["09:00"],
                max_per_day=1,
                min_hours_between=3,
                privacy="public",
                skip_thumbnails=True,
                apply=False,
                apply_youtube=False,
            )
            args.packets.write_text(
                yaml.safe_dump(
                    {
                        "packets": [
                            {
                                "slug": "trust-boundary",
                                "youtube_video_id": "abc12345678",
                                "title": "The Boundary Failed",
                                "claim": "Teams trusted the plan before checking the boundary.",
                                "evidence": ["The run failed after the tool boundary was crossed."],
                                "thumbnail_text": "Trust Boundary",
                            }
                        ]
                    },
                    sort_keys=False,
                )
            )

            plan = experiment.run(args)
            publish_item = plan["items"][0]["publish"]

            self.assertIsNone(publish_item["scheduled_at"])
            self.assertEqual(publish_item["mutation"], "metadata_only")

    def test_cli_apply_youtube_requires_apply(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            packets_path = root / "packets.yaml"
            packets_path.write_text("packets: []\n")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/insight_authority_experiment.py",
                    "--packets",
                    str(packets_path),
                    "--apply-youtube",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("--apply-youtube requires --apply", result.stderr)

    def test_cli_dry_run_does_not_write_plan_or_thumbnail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            packets_path = root / "packets.yaml"
            out_dir = root / "out"
            packets_path.write_text(
                yaml.safe_dump(
                    {
                        "packets": [
                            {
                                "slug": "trust-boundary",
                                "title": "The Boundary Failed | A Cinematic Research Brief",
                                "claim": "Teams trusted the plan before checking the boundary.",
                                "evidence": ["The run failed after the tool boundary was crossed."],
                                "thumbnail_text": "Trust Boundary",
                            }
                        ]
                    },
                    sort_keys=False,
                )
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/insight_authority_experiment.py",
                    "--packets",
                    str(packets_path),
                    "--out-dir",
                    str(out_dir),
                    "--start-at",
                    "2026-05-09T00:00:00Z",
                    "--timezone",
                    "UTC",
                    "--slot",
                    "09:00",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["dry_run"])
            self.assertFalse((out_dir / "insight_authority_plan.json").exists())
            self.assertFalse((out_dir / "emit_plan.json").exists())
            self.assertFalse((out_dir / "publish_plan.json").exists())
            self.assertFalse((out_dir / "thumbnails" / "trust-boundary.png").exists())


if __name__ == "__main__":
    unittest.main()
