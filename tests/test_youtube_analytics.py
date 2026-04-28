from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
YOUTUBE_SKILL_SCRIPTS = (
    REPO_ROOT / "workflows" / "skills" / "youtube-data-api" / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(YOUTUBE_SKILL_SCRIPTS))

import build_youtube_decision_report as report  # noqa: E402
import build_youtube_analytics_dashboard as dashboard  # noqa: E402
import fetch_youtube_analytics as fetch  # noqa: E402
import sync_youtube_reporting_reports as reporting_sync  # noqa: E402
import youtube_common  # noqa: E402


class FakeExecute:
    def __init__(self, response: dict):
        self.response = response

    def execute(self) -> dict:
        return self.response


class EmptyAnalytics:
    def reports(self):
        return self

    def query(self, **kwargs):
        dimensions = kwargs["dimensions"].split(",")
        metrics = kwargs["metrics"].split(",")
        headers = [{"name": name} for name in dimensions + metrics]
        return FakeExecute({"columnHeaders": headers, "rows": []})


class YouTubeAnalyticsTests(unittest.TestCase):
    maxDiff = None

    def test_oauth_scope_check_reports_missing_analytics_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = Path(tmpdir) / "token.json"
            token_path.write_text(
                json.dumps(
                    {
                        "token": "token",
                        "refresh_token": "refresh",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "client_id": "client",
                        "client_secret": "secret",
                        "scopes": [youtube_common.YOUTUBE_FORCE_SSL_SCOPE],
                    }
                )
            )

            missing = youtube_common.missing_oauth_scopes(
                youtube_common.SCOPES,
                token_file=token_path,
            )

        self.assertIn(youtube_common.YOUTUBE_READONLY_SCOPE, missing)
        self.assertIn(youtube_common.YOUTUBE_ANALYTICS_READONLY_SCOPE, missing)

    def test_upload_report_inventory_normalizes_shorts_and_related_video(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report_path = (
                root
                / "publications"
                / "demo-topic"
                / "artifacts"
                / "video"
                / "daily-cinematic-rollout"
                / "shorts_upload_report.json"
            )
            report_path.parent.mkdir(parents=True)
            report_path.write_text(
                json.dumps(
                    {
                        "workflow": "publication_shorts",
                        "related_video": {
                            "id": "LONG123",
                            "url": "https://www.youtube.com/watch?v=LONG123",
                        },
                        "items": [
                            {
                                "video_id": "SHORT123",
                                "title": "A Useful Hook #shorts",
                                "url": "https://www.youtube.com/watch?v=SHORT123",
                                "publish_at": "2026-04-20T06:00:00Z",
                                "video_path": "publications/demo-topic/artifacts/video/shorts/portrait/01.mp4",
                                "probe": {"duration": 25.0},
                                "youtube_readback": {
                                    "privacy_status": "public",
                                    "published_at": "2026-04-20T06:00:00Z",
                                },
                            }
                        ],
                    }
                )
            )

            records = fetch.collect_upload_report_videos(root)

        self.assertIn("SHORT123", records)
        self.assertEqual(records["SHORT123"]["format"], "short")
        self.assertEqual(records["SHORT123"]["package"], "demo-topic")
        self.assertEqual(records["SHORT123"]["related_video"]["id"], "LONG123")

    def test_missing_analytics_rows_become_nullable_windows(self) -> None:
        windows, daily, traffic, content_type, notes = fetch.build_analytics_windows(
            EmptyAnalytics(),
            video_ids=["VIDEO123"],
            end_date="2026-04-27",
        )

        self.assertTrue(windows["VIDEO123"]["7d"]["missing"])
        self.assertIsNone(windows["VIDEO123"]["7d"]["metrics"]["views"])
        self.assertEqual(daily["VIDEO123"], [])
        self.assertEqual(traffic["VIDEO123"], [])
        self.assertEqual(content_type["VIDEO123"], [])
        self.assertEqual(notes, [])

    def test_decision_classification_covers_core_buckets(self) -> None:
        rules = {
            "minimum_data_age_days": 2,
            "preferred_window": "7d",
            "thresholds": yaml.safe_load(
                (REPO_ROOT / "experiments" / "youtube-analytics" / "decision_rules.yaml").read_text()
            )["thresholds"],
        }
        ledger = {
            "videos": [
                self.video(
                    "SCALE",
                    "Scale Candidate",
                    "cinematic",
                    views=1400,
                    avg_pct=60,
                    subs=3,
                ),
                self.video(
                    "RETITLE",
                    "Retitle Candidate",
                    "short",
                    views=140,
                    avg_pct=48,
                    impressions=1000,
                    ctr=2.1,
                    source_reports=["publications/demo/artifacts/video/shorts_upload_report.json"],
                ),
                self.video(
                    "HOOK",
                    "Hook Problem",
                    "short",
                    views=140,
                    avg_pct=22,
                    source_reports=["publications/demo/artifacts/video/shorts_upload_report.json"],
                ),
                self.video(
                    "YOUNG",
                    "Too Young",
                    "short",
                    views=4000,
                    avg_pct=90,
                    published_at="2026-04-27T00:00:00Z",
                ),
            ]
        }

        classifications = report.classify_ledger(
            ledger,
            rules,
            as_of_date=date(2026, 4, 28),
        )
        by_id = {item["video_id"]: item for item in classifications}

        self.assertIn("scale", by_id["SCALE"]["categories"])
        self.assertIn("retitle", by_id["RETITLE"]["categories"])
        self.assertIn("hook_problem", by_id["HOOK"]["categories"])
        self.assertIn("ignore", by_id["YOUNG"]["categories"])
        self.assertNotIn("scale", by_id["YOUNG"]["categories"])

    def test_report_cli_writes_markdown_and_json_without_api_access(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            ledger_path = tmp / "ledger.json"
            rules_path = tmp / "rules.yaml"
            out_dir = tmp / "weekly_reports"
            ledger_path.write_text(
                json.dumps(
                    {
                        "created_at": "2026-04-28T00:00:00+00:00",
                        "analytics_end_date": "2026-04-27",
                        "query_notes": [],
                        "videos": [
                            self.video(
                                "SCALE",
                                "Scale Candidate",
                                "cinematic",
                                views=1400,
                                avg_pct=60,
                                subs=3,
                            )
                        ],
                    }
                )
            )
            rules_path.write_text(
                (REPO_ROOT / "experiments" / "youtube-analytics" / "decision_rules.yaml").read_text()
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_youtube_decision_report.py",
                    "--ledger",
                    str(ledger_path),
                    "--rules",
                    str(rules_path),
                    "--output-dir",
                    str(out_dir),
                    "--report-date",
                    "2026-04-28",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((out_dir / "2026-04-28.md").exists())
            summary = json.loads((out_dir / "2026-04-28.json").read_text())
            self.assertEqual(summary["summary_counts"]["scale"], 1)

    def test_dashboard_payload_and_cli_write_static_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            ledger_path = tmp / "ledger.json"
            report_path = tmp / "weekly_reports" / "2026-04-28.json"
            jobs_path = tmp / "reporting_jobs.json"
            output_path = tmp / "dashboard" / "index.html"
            payload_path = tmp / "dashboard" / "dashboard_payload.json"

            ledger = {
                "created_at": "2026-04-28T00:00:00+00:00",
                "analytics_end_date": "2026-04-27",
                "read_only": True,
                "query_notes": [],
                "reporting_api_sync": {
                    "merged_at": "2026-04-28T01:00:00+00:00",
                    "source_file_count": 2,
                    "videos_updated": 1,
                },
                "videos": [
                    self.video(
                        "SCALE",
                        "Scale Candidate",
                        "cinematic",
                        views=1400,
                        avg_pct=60,
                        subs=3,
                        daily_metrics=[
                            {
                                "window": "7d",
                                "day": "2026-04-27",
                                "metrics": {
                                    "views": 25,
                                    "estimatedMinutesWatched": 10,
                                    "averageViewDuration": 20,
                                    "averageViewPercentage": 55,
                                    "likes": 1,
                                    "comments": 0,
                                    "shares": 0,
                                    "subscribersGained": 1,
                                },
                            }
                        ],
                    ),
                    self.video(
                        "REMASTER",
                        "Remaster Candidate",
                        "short",
                        views=140,
                        avg_pct=22,
                        source_reports=["publications/demo/artifacts/video/shorts_upload_report.json"],
                    ),
                ],
            }
            rules = {
                "minimum_data_age_days": 2,
                "preferred_window": "7d",
                "thresholds": yaml.safe_load(
                    (REPO_ROOT / "experiments" / "youtube-analytics" / "decision_rules.yaml").read_text()
                )["thresholds"],
            }
            classifications = report.classify_ledger(
                ledger,
                rules,
                as_of_date=date(2026, 4, 28),
            )
            report_summary = {
                "report_date": "2026-04-28",
                "created_at": "2026-04-28T00:00:00+00:00",
                "analytics_end_date": "2026-04-27",
                "read_only": True,
                "summary_counts": {"scale": 1},
                "top_actions": [],
                "classifications": classifications,
            }
            jobs = {
                "jobs": {
                    "channel_reach_basic_a1": {
                        "name": "Reach basic",
                        "report_type_id": "channel_reach_basic_a1",
                        "available_report_count": 0,
                        "downloaded_report_count": 0,
                        "latest_report_end_time": None,
                        "purpose": "Daily per-video thumbnail impressions and thumbnail CTR.",
                    }
                }
            }
            ledger_path.write_text(json.dumps(ledger))
            report_path.parent.mkdir(parents=True)
            report_path.write_text(json.dumps(report_summary))
            jobs_path.write_text(json.dumps(jobs))

            payload = dashboard.build_dashboard_payload(ledger, report_summary, jobs)
            self.assertEqual(payload["totals"]["videos"], 2)
            self.assertEqual(payload["totals"]["actionable_videos"], 2)
            self.assertEqual(payload["findings"]["by_category"]["scale"][0]["video_id"], "SCALE")
            self.assertIn("retitle", payload["findings"]["by_category"])
            self.assertEqual(payload["action_lanes"]["do_now"]["count"], 2)
            self.assertEqual(payload["action_lanes"]["waiting_for_ctr"]["count"], 2)
            self.assertEqual(payload["action_lanes"]["needs_studio_check"]["count"], 2)
            self.assertEqual(payload["data_gap_groups"]["api_pending"]["fields"][0]["label"], "Thumbnail impressions")
            self.assertEqual(payload["package_rollups"][0]["package"], "demo")
            self.assertEqual(payload["package_rollups"][0]["video_count"], 2)
            self.assertEqual(payload["package_rollups"][0]["action_items"], 2)
            self.assertEqual(payload["horizons"]["monthly"]["label"], "28 Days")
            self.assertEqual(payload["horizon_summaries"]["daily"]["total_views"], 25)
            self.assertEqual(
                payload["package_rollups_by_horizon"]["daily"][0]["total_views"],
                25,
            )
            self.assertEqual(
                payload["findings"]["by_category"]["scale"][0]["horizon_metrics"]["daily"]["day"],
                "2026-04-27",
            )
            self.assertEqual(payload["funnel_rollups"]["totals"]["shorts_with_related"], 1)
            self.assertEqual(payload["sort_defaults"]["videos"]["key"], "score")
            self.assertEqual(
                payload["findings"]["by_category"]["remaster"][0]["actions_by_category"]["remaster"],
                "Queue this Short for the overlay remaster workflow instead of unlisting it immediately.",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_youtube_analytics_dashboard.py",
                    "--ledger",
                    str(ledger_path),
                    "--report",
                    str(report_path),
                    "--reporting-jobs",
                    str(jobs_path),
                    "--output",
                    str(output_path),
                    "--payload-output",
                    str(payload_path),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("YouTube Analytics Dashboard", output_path.read_text())
            self.assertEqual(json.loads(payload_path.read_text())["totals"]["videos"], 2)

    def test_reporting_rows_merge_reach_and_card_fields_into_ledger(self) -> None:
        ledger = {
            "videos": [
                self.video(
                    "REPORTING",
                    "Reporting Candidate",
                    "short",
                    views=140,
                    avg_pct=48,
                    impressions=None,
                    ctr=None,
                )
            ]
        }
        rows = [
            {
                "report_type_id": "channel_reach_basic_a1",
                "date": "20260424",
                "video_id": "REPORTING",
                "video_thumbnail_impressions": "1000",
                "video_thumbnail_impressions_ctr": "2.5",
                "source_file": "experiments/youtube-analytics/reporting_downloads/channel_reach_basic_a1/2026-04-24.csv",
            },
            {
                "report_type_id": "channel_basic_a3",
                "date": "20260424",
                "video_id": "REPORTING",
                "card_clicks": "4",
                "card_impressions": "20",
                "card_click_rate": "20",
                "card_teaser_clicks": "2",
                "card_teaser_impressions": "50",
                "card_teaser_click_rate": "4",
                "source_file": "experiments/youtube-analytics/reporting_downloads/channel_basic_a3/2026-04-24.csv",
            },
        ]

        reporting_sync.merge_reporting_rows_into_ledger(ledger, rows)
        video = ledger["videos"][0]
        metrics = video["analytics_windows"]["7d"]["metrics"]
        observations = video["manual_observations"]

        self.assertEqual(metrics["videoThumbnailImpressions"], 1000)
        self.assertEqual(metrics["videoThumbnailImpressionsClickRate"], 2.5)
        self.assertEqual(observations["card_clicks"], 4)
        self.assertEqual(observations["card_impressions"], 20)

        rules = {
            "minimum_data_age_days": 2,
            "preferred_window": "7d",
            "thresholds": yaml.safe_load(
                (REPO_ROOT / "experiments" / "youtube-analytics" / "decision_rules.yaml").read_text()
            )["thresholds"],
        }
        classification = report.classify_video(
            video,
            rules,
            as_of_date=date(2026, 4, 28),
        )
        self.assertIn("retitle", classification["categories"])

    def video(
        self,
        video_id: str,
        title: str,
        format_name: str,
        *,
        views: int,
        avg_pct: float,
        subs: int = 0,
        impressions: int | None = None,
        ctr: float | None = None,
        published_at: str = "2026-04-20T00:00:00Z",
        source_reports: list[str] | None = None,
        daily_metrics: list[dict] | None = None,
    ) -> dict:
        metrics = {
            "views": views,
            "estimatedMinutesWatched": 100,
            "averageViewDuration": 20,
            "averageViewPercentage": avg_pct,
            "likes": 1,
            "comments": 0,
            "shares": 0,
            "subscribersGained": subs,
            "videoThumbnailImpressions": impressions,
            "videoThumbnailImpressionsClickRate": ctr,
        }
        return {
            "video_id": video_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "published_at": published_at,
            "format": format_name,
            "package": "demo",
            "topic": "demo",
            "source_reports": source_reports or [],
            "related_video": {"id": "LONG123"},
            "analytics_windows": {
                "7d": {
                    "start_date": "2026-04-21",
                    "end_date": "2026-04-27",
                    "missing": False,
                    "metrics": metrics,
                }
            },
            "daily_metrics": daily_metrics or [],
            "manual_observations": {
                "related_video_clicks": None,
                "card_clicks": None,
                "end_screen_clicks": None,
                "retention_notes": None,
            },
        }


if __name__ == "__main__":
    unittest.main()
