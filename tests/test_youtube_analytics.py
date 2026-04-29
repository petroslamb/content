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
import analyze_youtube_srt_content as content_rubric  # noqa: E402
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


class FakeChannels:
    def list(self, **kwargs):
        return FakeExecute(
            {
                "items": [
                    {
                        "contentDetails": {
                            "relatedPlaylists": {"uploads": "UPLOADS"}
                        }
                    }
                ]
            }
        )


class FakePlaylists:
    def list(self, **kwargs):
        return FakeExecute(
            {
                "items": [
                    {
                        "id": "COURSE",
                        "snippet": {"title": "Rooted Layers Course", "description": ""},
                        "contentDetails": {"itemCount": 1},
                        "status": {"privacyStatus": "public"},
                    },
                    {
                        "id": "SHORTS",
                        "snippet": {"title": "AI Architecture Shorts", "description": ""},
                        "contentDetails": {"itemCount": 1},
                        "status": {"privacyStatus": "public"},
                    },
                ]
            }
        )


class FakePlaylistItems:
    def __init__(self):
        self.items = {
            "UPLOADS": [
                {
                    "id": "UPLOAD_ITEM",
                    "snippet": {
                        "title": "Uploaded Video",
                        "publishedAt": "2026-04-20T00:00:00Z",
                        "resourceId": {"videoId": "UPLOADED"},
                    },
                }
            ],
            "COURSE": [
                {
                    "id": "COURSE_ITEM",
                    "snippet": {
                        "title": "Course Only Video",
                        "publishedAt": "2026-04-21T00:00:00Z",
                        "position": 0,
                        "resourceId": {"videoId": "COURSEONLY"},
                    },
                }
            ],
            "SHORTS": [
                {
                    "id": "SHORTS_ITEM",
                    "snippet": {
                        "title": "Uploaded Video",
                        "publishedAt": "2026-04-22T00:00:00Z",
                        "position": 0,
                        "resourceId": {"videoId": "UPLOADED"},
                    },
                }
            ],
        }

    def list(self, **kwargs):
        return FakeExecute({"items": self.items.get(kwargs["playlistId"], [])})


class FakeYouTubeDiscovery:
    def channels(self):
        return FakeChannels()

    def playlists(self):
        return FakePlaylists()

    def playlistItems(self):
        return FakePlaylistItems()


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

    def test_playlist_membership_can_drive_format_inference(self) -> None:
        records = {
            "VIDEO123": {
                "video_id": "VIDEO123",
                "title": "Confidence Debt",
                "format": "unknown",
                "duration_seconds": 3272,
                "workflow": "youtube_recent_upload",
            }
        }
        memberships = {
            "VIDEO123": [
                {
                    "id": "PLAYLIST123",
                    "title": "Visual Deep Research Dives",
                    "position": 0,
                }
            ]
        }

        fetch.apply_playlist_memberships(records, memberships)

        self.assertEqual(records["VIDEO123"]["format"], "cinematic")
        self.assertEqual(records["VIDEO123"]["format_source"], "playlist")
        self.assertEqual(records["VIDEO123"]["playlists"][0]["title"], "Visual Deep Research Dives")
        self.assertEqual(
            fetch.infer_format(
                title="Confidence Debt",
                duration_seconds=3272,
                playlists=[{"title": "Rooted Layers Main Podcast"}],
            ),
            "podcast",
        )

    def test_all_channel_discovery_merges_uploads_playlists_and_repo_sources(self) -> None:
        youtube = FakeYouTubeDiscovery()
        records = {
            "UPLOADED": {
                "video_id": "UPLOADED",
                "title": "Uploaded Video From Repo",
                "discovery_sources": ["repo_upload_report"],
                "source_reports": ["publications/demo/upload_report.json"],
            }
        }
        for record in fetch.fetch_channel_uploads(youtube).values():
            fetch.merge_video_record(records, record)
        playlists, memberships, playlist_records = fetch.fetch_playlist_inventory_and_memberships(youtube)
        for record in playlist_records.values():
            fetch.merge_video_record(records, record)
        fetch.apply_playlist_memberships(records, memberships)

        self.assertEqual(set(records), {"UPLOADED", "COURSEONLY"})
        self.assertEqual(
            records["UPLOADED"]["discovery_sources"],
            ["channel_playlist", "channel_uploads", "repo_upload_report"],
        )
        self.assertEqual(records["COURSEONLY"]["discovery_sources"], ["channel_playlist"])
        self.assertEqual(len(playlists), 2)
        self.assertEqual(records["COURSEONLY"]["playlists"][0]["title"], "Rooted Layers Course")

    def test_release_timing_and_thumbnail_extraction(self) -> None:
        timing = fetch.release_timing_from_published_at("2026-04-29T06:00:02Z")
        self.assertEqual(timing["timezone"], "Europe/Athens")
        self.assertEqual(timing["weekday"], "Wednesday")
        self.assertEqual(timing["hour"], 9)
        thumbnails = fetch.compact_thumbnail_set(
            {
                "default": {"url": "default.jpg", "width": 120, "height": 90},
                "high": {"url": "high.jpg", "width": 480, "height": 360},
                "maxres": {"url": "maxres.jpg", "width": 1280, "height": 720},
            }
        )
        self.assertEqual(thumbnails["best_url"], "maxres.jpg")
        self.assertEqual(thumbnails["variants"][0]["quality"], "maxres")

    def test_length_fit_bands_cover_supported_formats(self) -> None:
        self.assertEqual(dashboard.length_fit("short", 37)["bucket"], "target")
        self.assertEqual(dashboard.length_fit("short", 80)["bucket"], "too_long")
        self.assertEqual(dashboard.length_fit("cinematic", 300)["bucket"], "target")
        self.assertEqual(dashboard.length_fit("tldr", 720)["bucket"], "acceptable_long")
        self.assertEqual(dashboard.length_fit("podcast", 3600)["severity"], "neutral")

    def test_srt_content_analysis_present_missing_and_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            srt = root / "publications" / "demo" / "artifacts" / "video" / "demo_cinematic.srt"
            srt.parent.mkdir(parents=True)
            srt.write_text(
                "1\n00:00:01,000 --> 00:00:04,000\nWhy agents fail in production.\n\n"
                "2\n00:00:10,000 --> 00:00:13,000\nThe system loses memory and control.\n\n"
                "3\n00:00:40,000 --> 00:00:43,000\nWatch the full brief below.\n"
            )
            video = self.video(
                "SRT",
                "Why Agents Fail",
                "cinematic",
                views=10,
                avg_pct=40,
                source_reports=["publications/demo/artifacts/video/shorts_upload_report.json"],
            )
            mapped = content_rubric.map_srt_for_video(video, root=root)
            self.assertEqual(mapped["status"], "present")
            self.assertEqual(mapped["first_spoken_line"], "Why agents fail in production.")
            self.assertTrue(mapped["closing_cta_presence"])

            missing = content_rubric.map_srt_for_video(
                {**video, "package": "other", "title": "No Match", "source_reports": []},
                root=root,
            )
            self.assertEqual(missing["status"], "missing")

            bad = root / "publications" / "bad" / "bad.srt"
            bad.parent.mkdir(parents=True)
            bad.write_text("not a subtitle")
            malformed = content_rubric.analyze_srt(bad, title="Bad")
            self.assertEqual(malformed["status"], "malformed")

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
                "channel_playlists": [
                    {
                        "id": "PLAYLIST123",
                        "title": "Visual Deep Research Dives",
                        "item_count": 3,
                        "observed_item_count": 3,
                        "privacy_status": "public",
                        "url": "https://www.youtube.com/playlist?list=PLAYLIST123",
                    },
                    {
                        "id": "COURSE123",
                        "title": "Rooted Layers Course",
                        "item_count": 7,
                        "observed_item_count": 7,
                        "privacy_status": "public",
                        "url": "https://www.youtube.com/playlist?list=COURSE123",
                    },
                ],
                "videos": [
                    self.video(
                        "SCALE",
                        "Scale Candidate",
                        "cinematic",
                        views=1400,
                        avg_pct=60,
                        subs=3,
                        playlists=[
                            {
                                "id": "PLAYLIST123",
                                "title": "Visual Deep Research Dives",
                                "position": 0,
                            }
                        ],
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
            self.assertEqual(payload["totals"]["playlist_videos"], 1)
            self.assertEqual(payload["playlist_rollups"][0]["playlist"], "Visual Deep Research Dives")
            self.assertEqual(payload["playlist_rollups"][0]["video_count"], 1)
            course_inventory = {
                row["playlist_id"]: row
                for row in payload["playlist_inventory"]
            }["COURSE123"]
            self.assertEqual(course_inventory["in_scope_video_count"], 0)
            self.assertEqual(course_inventory["missing_from_scope_count"], 7)
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
            self.assertEqual(
                payload["findings"]["by_category"]["scale"][0]["primary_playlist"]["title"],
                "Visual Deep Research Dives",
            )
            self.assertEqual(payload["funnel_rollups"]["totals"]["shorts_with_related"], 1)
            self.assertIn("rubric", payload)
            self.assertEqual(payload["rubric"]["items"][0]["video_id"], "SCALE")
            self.assertEqual(payload["rubric"]["items"][0]["length_fit"]["bucket"], "target")
            self.assertIn("release_rollups_by_horizon", payload)
            self.assertIn("length_rollups_by_horizon", payload)
            self.assertEqual(payload["sort_defaults"]["videos"]["key"], "useful")
            self.assertEqual(payload["coverage"]["metrics"]["views"]["total"], 2)
            self.assertEqual(payload["coverage"]["metrics"]["views"]["count"], 2)
            self.assertIn("metric_coverage", payload["help_text"])
            self.assertIn("srt_hook", payload["help_text"])
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
            html = output_path.read_text()
            self.assertIn("YouTube Analytics Dashboard", html)
            self.assertIn("dashboard-tooltip", html)
            self.assertIn("data-tooltip", html)
            self.assertIn('<button class="tab active" data-tab="overview">Overview</button>', html)
            self.assertNotIn('data-tab="daily-delta"', html)
            self.assertNotIn('data-tab="packaging"', html)
            self.assertNotIn('data-tab="funnel"', html)
            self.assertNotIn('data-tab="release-lab"', html)
            self.assertNotIn('data-tab="production"', html)
            self.assertEqual(json.loads(payload_path.read_text())["totals"]["videos"], 2)

    def test_dashboard_warns_when_reach_reports_are_ready_but_not_hydrated(self) -> None:
        ledger = {
            "created_at": "2026-04-28T00:00:00+00:00",
            "analytics_end_date": "2026-04-27",
            "read_only": True,
            "videos": [
                self.video(
                    "NOCTR",
                    "No CTR",
                    "short",
                    views=20,
                    avg_pct=40,
                    impressions=None,
                    ctr=None,
                )
            ],
        }
        report_summary = {
            "report_date": "2026-04-28",
            "read_only": True,
            "summary_counts": {},
            "top_actions": [],
            "classifications": [
                {
                    "video_id": "NOCTR",
                    "title": "No CTR",
                    "url": "https://www.youtube.com/watch?v=NOCTR",
                    "format": "short",
                    "package": "demo",
                    "published_at": "2026-04-20T00:00:00Z",
                    "selected_window": "7d",
                    "data_age_days": 8,
                    "categories": ["ignore"],
                    "reasons": [],
                    "recommended_actions": [],
                    "manual_fields_missing": ["video_thumbnail_impressions", "video_thumbnail_ctr"],
                    "metrics": {},
                }
            ],
        }
        jobs = {
            "jobs": {
                "channel_reach_basic_a1": {
                    "name": "Reach basic",
                    "report_type_id": "channel_reach_basic_a1",
                    "available_report_count": 1,
                    "downloaded_report_count": 1,
                    "latest_report_end_time": "2026-04-27T07:00:00Z",
                    "purpose": "Daily per-video thumbnail impressions and thumbnail CTR.",
                }
            }
        }

        payload = dashboard.build_dashboard_payload(ledger, report_summary, jobs)

        self.assertTrue(payload["reporting_status"]["reach_hydration_gap"])
        self.assertEqual(payload["warnings"][0]["key"], "reporting_reach_not_hydrated")

    def test_v4_dashboard_decision_cockpit_payloads(self) -> None:
        ledger = {
            "created_at": "2026-04-28T00:00:00+00:00",
            "analytics_end_date": "2026-04-27",
            "read_only": True,
            "videos": [
                self.video(
                    "PACK",
                    "AI Memory Failure in Multi-Agent Systems",
                    "short",
                    views=350,
                    avg_pct=62,
                    impressions=1000,
                    ctr=2.1,
                    traffic_sources=[
                        {"window": "7d", "source_type": "RELATED_VIDEO", "views": 8}
                    ],
                    daily_metrics=[
                        {
                            "window": "7d",
                            "day": "2026-04-25",
                            "metrics": {
                                "views": 10,
                                "estimatedMinutesWatched": 4,
                                "averageViewDuration": 20,
                                "averageViewPercentage": 40,
                                "likes": 0,
                                "comments": 0,
                                "shares": 0,
                                "subscribersGained": 0,
                            },
                        },
                        {
                            "window": "7d",
                            "day": "2026-04-26",
                            "metrics": {
                                "views": 30,
                                "estimatedMinutesWatched": 15,
                                "averageViewDuration": 30,
                                "averageViewPercentage": 55,
                                "likes": 1,
                                "comments": 0,
                                "shares": 0,
                                "subscribersGained": 1,
                            },
                        },
                    ],
                    manual_observations={
                        "related_video_clicks": 2,
                        "card_clicks": 4,
                        "end_screen_clicks": 1,
                        "retention_notes": None,
                    },
                ),
                self.video(
                    "WAIT",
                    "Useful But Underdistributed Agent Memory",
                    "short",
                    views=24,
                    avg_pct=74,
                    impressions=90,
                    ctr=8.0,
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
            "summary_counts": {},
            "top_actions": [],
            "classifications": classifications,
        }
        content = {
            "items": {
                "PACK": {
                    "status": "present",
                    "specificity_hints": ["agent", "memory", "multi-agent"],
                }
            },
            "status_counts": {"present": 1},
        }
        previous_snapshot = {
            "generated_at": "2026-04-27T00:00:00+00:00",
            "findings": {
                "classifications": [
                    {
                        "video_id": "PACK",
                        "horizon_metrics": {
                            "weekly": {
                                "metrics": {
                                    "views_per_day": 10,
                                    "videoThumbnailImpressionsClickRate": 3.5,
                                    "averageViewPercentage": 58,
                                    "subscribersGained": 0,
                                }
                            }
                        },
                        "funnel": {"known_downstream_clicks": 1},
                        "traffic_sources": [
                            {"window": "7d", "source_type": "RELATED_VIDEO", "views": 2}
                        ],
                    }
                ]
            },
        }
        registry = {
            "source_path": "fixture.yaml",
            "experiments": [
                {
                    "id": "packaging_test",
                    "name": "Packaging Test",
                    "type": "title_test",
                    "status": "active",
                    "hypothesis": "Sharper title should improve CTR.",
                    "video_ids": ["PACK"],
                    "start_date": "2026-04-27",
                    "metric_target": "videoThumbnailImpressionsClickRate",
                    "notes": "",
                }
            ],
        }

        payload = dashboard.build_dashboard_payload(
            ledger,
            report_summary,
            reporting_jobs=None,
            content_rubric=content,
            experiment_registry=registry,
            previous_snapshot=previous_snapshot,
        )

        self.assertEqual(payload["delta_summary"]["status"], "ready")
        self.assertEqual(payload["daily_movement"]["status"], "ready")
        self.assertEqual(payload["daily_movement"]["latest_day"], "2026-04-26")
        self.assertEqual(
            payload["daily_movement"]["groups"]["latest_day_views"]["items"][0]["video_id"],
            "PACK",
        )
        self.assertEqual(
            payload["delta_summary"]["groups"]["views_day_movers"]["items"][0]["video_id"],
            "PACK",
        )
        self.assertEqual(payload["experiments"]["experiments"][0]["id"], "packaging_test")
        self.assertEqual(payload["experiments"]["experiments"][0]["cohort_found"], 1)
        self.assertEqual(
            payload["packaging_lab"]["buckets"]["high_impression_low_ctr"]["items"][0]["video_id"],
            "PACK",
        )
        self.assertEqual(payload["funnel_map"]["buckets"]["card_clicks"]["items"][0]["video_id"], "PACK")
        self.assertEqual(payload["funnel_map"]["buckets"]["end_screen_clicks"]["items"][0]["video_id"], "PACK")
        self.assertEqual(
            payload["funnel_map"]["buckets"]["related_video_traffic"]["items"][0]["related_video_traffic_views"],
            8,
        )
        self.assertTrue(payload["topic_clusters"]["clusters"])
        self.assertIn("short", payload["release_time_lab"]["by_format"])
        self.assertEqual(payload["production_queue"]["items"][0]["action"], "thumbnail_review")
        self.assertIn("daily_delta", payload["help_text"])
        self.assertIn("production_queue", payload["help_text"])
        snapshot = dashboard.compact_snapshot_payload(payload)
        self.assertEqual(snapshot["findings"]["classifications"][0]["video_id"], "PACK")

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
                "video_thumbnail_impressions_ctr": "0.025",
                "source_file": "experiments/youtube-analytics/reporting_downloads/channel_reach_basic_a1/2026-04-24.csv",
            },
            {
                "report_type_id": "channel_basic_a3",
                "date": "20260424",
                "video_id": "REPORTING",
                "card_clicks": "4",
                "card_impressions": "20",
                "card_click_rate": "0.2",
                "card_teaser_clicks": "2",
                "card_teaser_impressions": "50",
                "card_teaser_click_rate": "0.04",
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
        self.assertEqual(observations["card_click_rate"], 20.0)

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
        playlists: list[dict] | None = None,
        duration_seconds: float = 300,
        thumbnail_url: str | None = "https://i.ytimg.com/vi/demo/maxresdefault.jpg",
        traffic_sources: list[dict] | None = None,
        manual_observations: dict | None = None,
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
            "release_timing": dashboard.release_timing_from_published_at(published_at),
            "duration_seconds": duration_seconds,
            "thumbnail_url": thumbnail_url,
            "thumbnails": [
                {
                    "quality": "maxres",
                    "url": thumbnail_url,
                    "width": 1280,
                    "height": 720,
                }
            ]
            if thumbnail_url
            else [],
            "format": format_name,
            "format_source": "fixture",
            "package": "demo",
            "topic": "demo",
            "playlists": playlists or [],
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
            "traffic_sources": traffic_sources or [],
            "manual_observations": manual_observations or {
                "related_video_clicks": None,
                "card_clicks": None,
                "end_screen_clicks": None,
                "retention_notes": None,
            },
        }


if __name__ == "__main__":
    unittest.main()
