from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(
    0,
    str(REPO_ROOT / "workflows" / "skills" / "youtube-data-api" / "scripts"),
)

import apply_youtube_portfolio as operator  # noqa: E402
import rooted_layers_portfolio as portfolio  # noqa: E402


class FakeExecute:
    def __init__(self, callback):
        self.callback = callback

    def execute(self):
        return self.callback()


class FakeChannels:
    def __init__(self, api):
        self.api = api

    def list(self, **kwargs):
        def response():
            self.api.channel_list_call_count += 1
            override = self.api.channel_overrides.get(
                self.api.channel_list_call_count, {}
            )
            return {
                "items": [
                    {
                        "id": override.get("channel_id", self.api.channel_id),
                        "snippet": {
                            "title": override.get(
                                "channel_title", self.api.channel_title
                            )
                        },
                        "contentDetails": {
                            "relatedPlaylists": {
                                "uploads": override.get(
                                    "uploads_playlist_id",
                                    self.api.uploads_playlist_id,
                                )
                            }
                        },
                    }
                ]
            }

        return FakeExecute(response)


class FakeVideos:
    def __init__(self, api):
        self.api = api

    def list(self, **kwargs):
        ids = kwargs["id"].split(",")
        self.api.list_batches.append(ids)

        def response():
            self.api.video_list_call_count += 1
            if self.api.fail_video_list_call == self.api.video_list_call_count:
                raise RuntimeError("simulated video readback quota failure")
            return {
                "items": [
                    {
                        "id": video_id,
                        "snippet": {
                            "title": f"Video {video_id}",
                            "channelId": self.api.video_channels.get(
                                video_id, self.api.channel_id
                            ),
                        },
                        "status": {
                            "privacyStatus": self.api.statuses[video_id],
                            "license": "youtube",
                            "embeddable": True,
                        },
                    }
                    for video_id in ids
                    if video_id in self.api.statuses
                ]
            }

        return FakeExecute(response)

    def update(self, **kwargs):
        video_id = kwargs["body"]["id"]
        body = kwargs["body"]

        def response():
            if self.api.before_video_update is not None:
                self.api.before_video_update(video_id)
            self.api.update_calls.append(body)
            if video_id == self.api.fail_update_id:
                raise RuntimeError("simulated quota failure")
            if video_id != self.api.readback_mismatch_id:
                self.api.statuses[video_id] = body["status"]["privacyStatus"]
            return {"id": video_id, "status": body["status"]}

        return FakeExecute(response)


class FakePlaylists:
    def __init__(self, api):
        self.api = api

    def list(self, **kwargs):
        return FakeExecute(lambda: {"items": list(self.api.playlists_data)})

    def insert(self, **kwargs):
        body = kwargs["body"]

        def response():
            playlist_id = "PLAYLIST_CREATED"
            self.api.playlist_insert_calls.append(body)
            self.api.playlists_data.append(
                {
                    "id": playlist_id,
                    "snippet": dict(body["snippet"]),
                    "status": dict(body["status"]),
                    "contentDetails": {"itemCount": 0},
                }
            )
            self.api.playlist_items_by_id[playlist_id] = []
            return {"id": playlist_id}

        return FakeExecute(response)


class FakePlaylistItems:
    def __init__(self, api):
        self.api = api

    def list(self, **kwargs):
        playlist_id = kwargs["playlistId"]

        def response():
            self.api.playlist_list_call_count += 1
            if self.api.fail_playlist_list_call == self.api.playlist_list_call_count:
                raise RuntimeError("simulated playlist readback quota failure")
            return {"items": list(self.api.playlist_items_by_id.get(playlist_id, []))}

        return FakeExecute(response)

    def delete(self, **kwargs):
        item_id = kwargs["id"]

        def response():
            self.api.playlist_delete_calls.append(item_id)
            if self.api.fail_playlist_action == ("delete", item_id):
                raise RuntimeError("simulated playlist quota failure")
            for items in self.api.playlist_items_by_id.values():
                items[:] = [item for item in items if item.get("id") != item_id]
                for position, item in enumerate(items):
                    item["snippet"]["position"] = position
            return {}

        return FakeExecute(response)

    def update(self, **kwargs):
        body = kwargs["body"]

        def response():
            self.api.playlist_update_calls.append(body)
            if self.api.fail_playlist_action == ("update", body["id"]):
                raise RuntimeError("simulated playlist quota failure")
            playlist_id = body["snippet"]["playlistId"]
            items = self.api.playlist_items_by_id[playlist_id]
            item = next(item for item in items if item["id"] == body["id"])
            item["snippet"].update(body["snippet"])
            items.sort(key=lambda value: value["snippet"]["position"])
            for position, value in enumerate(items):
                value["snippet"]["position"] = position
            return {"id": body["id"]}

        return FakeExecute(response)

    def insert(self, **kwargs):
        snippet = kwargs["body"]["snippet"]
        video_id = snippet["resourceId"]["videoId"]

        def response():
            self.api.playlist_item_insert_calls.append(kwargs["body"])
            if self.api.fail_playlist_action == ("insert", video_id):
                raise RuntimeError("simulated playlist quota failure")
            playlist_id = snippet["playlistId"]
            items = self.api.playlist_items_by_id[playlist_id]
            item_id = f"ITEM_{video_id}"
            for item in items:
                if item["snippet"]["position"] >= snippet["position"]:
                    item["snippet"]["position"] += 1
            items.append(
                {
                    "id": item_id,
                    "snippet": {
                        **snippet,
                        "title": f"Video {video_id}",
                        "videoOwnerChannelId": self.api.channel_id,
                    },
                }
            )
            items.sort(key=lambda value: value["snippet"]["position"])
            return {"id": item_id}

        return FakeExecute(response)


class FakeYouTube:
    def __init__(self, statuses: dict[str, str]):
        self.channel_id = "CHANNEL123"
        self.channel_title = "Rooted Layers"
        self.uploads_playlist_id = "UPLOADS"
        self.channel_list_call_count = 0
        self.channel_overrides: dict[int, dict[str, str]] = {}
        self.statuses = dict(statuses)
        self.video_channels = {video_id: self.channel_id for video_id in statuses}
        self.list_batches: list[list[str]] = []
        self.update_calls: list[dict] = []
        self.before_video_update = None
        self.fail_update_id: str | None = None
        self.readback_mismatch_id: str | None = None
        self.video_list_call_count = 0
        self.fail_video_list_call: int | None = None
        self.playlists_data: list[dict] = []
        self.playlist_items_by_id: dict[str, list[dict]] = {}
        self.playlist_insert_calls: list[dict] = []
        self.playlist_item_insert_calls: list[dict] = []
        self.playlist_update_calls: list[dict] = []
        self.playlist_delete_calls: list[str] = []
        self.fail_playlist_action: tuple[str, str] | None = None
        self.playlist_list_call_count = 0
        self.fail_playlist_list_call: int | None = None

    def channels(self):
        return FakeChannels(self)

    def videos(self):
        return FakeVideos(self)

    def playlists(self):
        return FakePlaylists(self)

    def playlistItems(self):
        return FakePlaylistItems(self)


def youtube_artifact(video_id: str, *, target: str = "UNLIST") -> dict:
    return {
        "artifact_id": f"youtube:{video_id}",
        "platform": "YOUTUBE",
        "platform_id": video_id,
        "title": f"Video {video_id}",
        "current_url": f"https://www.youtube.com/watch?v={video_id}",
        "current_visibility": "PUBLIC",
        "family_id": "youtube:test",
        "relationships": [
            {"type": "DUPLICATES", "target_artifact_id": "youtube:RETAINED"}
        ]
        if target == "UNLIST"
        else [],
        "selection_tier": "ARCHIVE",
        "editorial_action": "NONE",
        "target_visibility": target,
        "homepage": {"section": None, "order": None},
        "provenance": {
            "status": "DOCUMENTED",
            "documented_contribution": "Video derivative.",
        },
        "source_lineage": {"status": "RESOLVED", "notes": "Matched."},
        "factual_risk": {"status": "LOW", "notes": "No open issue."},
        "evidence_anchors": ["captions.srt"],
        "rationale": "Duplicate of retained representative.",
        "confidence": "HIGH",
        "approval_status": "PENDING",
        "application_status": "NOT_APPLIED",
    }


def manifest(video_ids: list[str]) -> dict:
    retained = youtube_artifact("RETAINED", target="UNCHANGED")
    artifacts = [retained, *[youtube_artifact(video_id) for video_id in video_ids]]
    return {
        "youtube": {
            "expected_channel_id": "CHANNEL123",
            "expected_channel_title": "Rooted Layers",
            "expected_uploads_playlist_id": "UPLOADS",
            "unlist_video_ids": video_ids,
        },
        "artifacts": artifacts,
    }


def playlist_manifest(video_ids: list[str]) -> dict:
    artifacts = [youtube_artifact(video_id, target="UNCHANGED") for video_id in video_ids]
    for artifact in artifacts:
        artifact["selection_tier"] = "SUPPORTING"
    return {
        "youtube": {
            "expected_channel_id": "CHANNEL123",
            "expected_channel_title": "Rooted Layers",
            "expected_uploads_playlist_id": "UPLOADS",
            "selected_video_ids": video_ids,
            "unlist_video_ids": [],
            "playlist": {
                "title": portfolio.PLAYLIST_TITLE,
                "create_or_update": len(video_ids) >= 2,
                "surface_on_channel_homepage": len(video_ids) >= 2,
            },
        },
        "artifacts": artifacts,
    }


def playlist_item(item_id: str, video_id: str, position: int) -> dict:
    return {
        "id": item_id,
        "snippet": {
            "playlistId": "PLAYLIST1",
            "position": position,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
            "title": f"Video {video_id}",
            "videoOwnerChannelId": "CHANNEL123",
        },
    }


class YouTubePortfolioOperatorTests(unittest.TestCase):
    def test_apply_requires_release_gate_before_validation_or_auth(self) -> None:
        argv = ["apply_youtube_portfolio.py", "playlist", "--apply"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(operator.portfolio, "validate_manifest_document") as validate,
            mock.patch.object(operator, "build_youtube") as authenticate,
            self.assertRaisesRegex(SystemExit, "requires --release-readiness"),
        ):
            operator.main()
        validate.assert_not_called()
        authenticate.assert_not_called()

    def test_dry_run_uses_preapproval_validation_without_approval_or_gate(self) -> None:
        data = playlist_manifest([])
        validation = {"valid": True, "manifest_sha256": "b" * 64, "errors": []}
        youtube = FakeYouTube({})
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "dry-run.json"
            argv = [
                "apply_youtube_portfolio.py",
                "playlist",
                "--manifest",
                str(Path(tmpdir) / "manifest.yaml"),
                "--report",
                str(report_path),
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(
                    operator.portfolio,
                    "validate_manifest_document",
                    return_value=(data, validation),
                ) as validate,
                mock.patch.object(operator, "build_youtube", return_value=youtube),
                mock.patch("builtins.print"),
            ):
                operator.main()
            report = json.loads(report_path.read_text(encoding="utf-8"))

        validate.assert_called_once()
        self.assertIsNone(validate.call_args.args[1])
        self.assertIsNone(validate.call_args.args[2])
        self.assertEqual(validate.call_args.kwargs["validation_mode"], "preapproval")
        self.assertEqual(report["status"], "DRY_RUN_VERIFIED")

    def test_wrong_account_rejected_before_video_reads(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public"})
        youtube.channel_id = "WRONG"

        with self.assertRaisesRegex(operator.PortfolioYouTubeError, "channel mismatch"):
            operator.visibility_plan(youtube, manifest(["VIDEO1"]))

        self.assertEqual(youtube.list_batches, [])
        self.assertEqual(youtube.update_calls, [])

    def test_dry_run_plan_does_not_mutate_and_retains_rollback_state(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public"})

        channel, plan = operator.visibility_plan(youtube, manifest(["VIDEO1"]))

        self.assertEqual(channel["channel_id"], "CHANNEL123")
        self.assertEqual(plan[0]["expected_before"], "public")
        self.assertEqual(plan[0]["target_after"], "unlisted")
        self.assertEqual(plan[0]["rollback_visibility"], "public")
        self.assertEqual(youtube.statuses["VIDEO1"], "public")
        self.assertEqual(youtube.update_calls, [])

    def test_stale_before_state_makes_rerun_safe(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "unlisted"})

        with self.assertRaisesRegex(operator.PortfolioYouTubeError, "stale before-state"):
            operator.visibility_plan(youtube, manifest(["VIDEO1"]))

        self.assertEqual(youtube.update_calls, [])

    def test_foreign_video_is_rejected_before_mutation(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public"})
        youtube.video_channels["VIDEO1"] = "FOREIGN"

        with self.assertRaisesRegex(operator.PortfolioYouTubeError, "approved channel"):
            operator.visibility_plan(youtube, manifest(["VIDEO1"]))

        self.assertEqual(youtube.update_calls, [])

    def test_uploads_playlist_identity_is_required_exactly(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public"})
        youtube.uploads_playlist_id = "WRONG_UPLOADS"

        with self.assertRaisesRegex(operator.PortfolioYouTubeError, "uploads playlist mismatch"):
            operator.visibility_plan(youtube, manifest(["VIDEO1"]))

        self.assertEqual(youtube.list_batches, [])

    def test_channel_identity_is_reverified_before_each_visibility_mutation(self) -> None:
        cases = (
            ({"channel_id": "DRIFTED_CHANNEL"}, "channel mismatch"),
            ({"channel_title": "Drifted Title"}, "channel title mismatch"),
            (
                {"uploads_playlist_id": "DRIFTED_UPLOADS"},
                "uploads playlist mismatch",
            ),
        )
        for override, message in cases:
            with self.subTest(override=override):
                youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
                _, plan = operator.visibility_plan(
                    youtube, manifest(["VIDEO1", "VIDEO2"])
                )
                # Planning is call 1; mutation checks are calls 2 and 3.
                youtube.channel_overrides[3] = override
                state = {
                    "batches": [],
                    "operations": [],
                    "rollback": [
                        {"video_id": "VIDEO1"},
                        {"video_id": "VIDEO2"},
                    ],
                }

                with self.assertRaisesRegex(
                    operator.PortfolioYouTubeError, message
                ):
                    operator.apply_visibility_batches(
                        youtube,
                        plan,
                        expected_channel_id="CHANNEL123",
                        canary_size=2,
                        state=state,
                    )

                self.assertEqual(
                    [body["id"] for body in youtube.update_calls], ["VIDEO1"]
                )
                self.assertEqual(youtube.statuses["VIDEO1"], "unlisted")
                self.assertEqual(youtube.statuses["VIDEO2"], "public")
                self.assertFalse(state["operations"][1]["mutation_attempted"])

    def test_canary_then_batches_never_exceed_twenty_five(self) -> None:
        video_ids = [f"VIDEO{index:02d}" for index in range(31)]
        youtube = FakeYouTube({video_id: "public" for video_id in video_ids})
        _, plan = operator.visibility_plan(youtube, manifest(video_ids))
        youtube.list_batches.clear()

        results = operator.apply_visibility_batches(
            youtube,
            plan,
            expected_channel_id="CHANNEL123",
            canary_size=3,
        )

        self.assertEqual([len(batch["video_ids"]) for batch in results], [3, 25, 3])
        self.assertTrue(results[0]["canary"])
        self.assertTrue(all(len(batch) <= 25 for batch in youtube.list_batches))
        self.assertEqual(len(youtube.update_calls), 31)
        self.assertEqual(set(youtube.statuses.values()), {"unlisted"})

    def test_quota_failure_retains_incremental_success_and_rollback_state(self) -> None:
        video_ids = ["VIDEO1", "VIDEO2", "VIDEO3"]
        youtube = FakeYouTube({video_id: "public" for video_id in video_ids})
        _, plan = operator.visibility_plan(youtube, manifest(video_ids))
        youtube.fail_update_id = "VIDEO2"
        state = {
            "batches": [],
            "operations": [],
            "rollback": [{"video_id": video_id} for video_id in video_ids],
        }

        with self.assertRaisesRegex(RuntimeError, "quota"):
            operator.apply_visibility_batches(
                youtube,
                plan,
                expected_channel_id="CHANNEL123",
                canary_size=3,
                state=state,
            )

        self.assertEqual(youtube.statuses["VIDEO1"], "unlisted")
        self.assertEqual(youtube.statuses["VIDEO2"], "public")
        self.assertEqual(youtube.statuses["VIDEO3"], "public")
        self.assertEqual(len(state["operations"]), 2)
        self.assertTrue(state["operations"][0]["mutation_succeeded"])
        self.assertIsNone(state["operations"][1]["mutation_succeeded"])
        self.assertTrue(state["rollback"][0]["mutation_succeeded"])
        self.assertIsNone(state["rollback"][1]["mutation_succeeded"])
        self.assertTrue(state["remote_state_uncertain"])

    def test_readback_mismatch_stops_after_canary(self) -> None:
        video_ids = ["VIDEO1", "VIDEO2", "VIDEO3"]
        youtube = FakeYouTube({video_id: "public" for video_id in video_ids})
        _, plan = operator.visibility_plan(youtube, manifest(video_ids))
        youtube.readback_mismatch_id = "VIDEO2"

        with self.assertRaisesRegex(operator.PortfolioYouTubeError, "readback mismatch"):
            state = {
                "batches": [],
                "operations": [],
                "rollback": [
                    {"video_id": video_id} for video_id in video_ids
                ],
            }
            operator.apply_visibility_batches(
                youtube,
                plan,
                expected_channel_id="CHANNEL123",
                canary_size=2,
                state=state,
            )

        self.assertEqual(len(youtube.update_calls), 2)
        self.assertEqual(youtube.statuses["VIDEO3"], "public")
        self.assertEqual(state["batches"][0]["status"], "STOPPED")
        self.assertEqual(len(state["operations"]), 2)
        self.assertTrue(all(item["mutation_succeeded"] for item in state["operations"]))
        self.assertFalse(state["operations"][1]["readback_matched"])

    def test_visibility_readback_quota_failure_keeps_all_successful_mutations(self) -> None:
        video_ids = ["VIDEO1", "VIDEO2"]
        youtube = FakeYouTube({video_id: "public" for video_id in video_ids})
        _, plan = operator.visibility_plan(youtube, manifest(video_ids))
        youtube.fail_video_list_call = 4
        state = {
            "batches": [],
            "operations": [],
            "rollback": [{"video_id": video_id} for video_id in video_ids],
        }

        with self.assertRaisesRegex(RuntimeError, "readback quota"):
            operator.apply_visibility_batches(
                youtube,
                plan,
                expected_channel_id="CHANNEL123",
                canary_size=2,
                state=state,
            )

        self.assertEqual(set(youtube.statuses.values()), {"unlisted"})
        self.assertEqual(state["batches"][0]["status"], "STOPPED")
        self.assertTrue(all(item["mutation_succeeded"] for item in state["operations"]))
        self.assertTrue(all(item["mutation_succeeded"] for item in state["rollback"]))
        self.assertTrue(all(item["readback_visibility"] is None for item in state["rollback"]))
        self.assertTrue(state["remote_state_uncertain"])

    def test_update_body_cannot_edit_title_or_description(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public"})

        operator.update_visibility(
            youtube, "VIDEO1", expected_channel_id="CHANNEL123"
        )

        body = youtube.update_calls[0]
        self.assertEqual(set(body), {"id", "status"})
        self.assertEqual(body["status"]["privacyStatus"], "unlisted")
        self.assertNotIn("snippet", body)

    def test_playlist_plan_rejects_missing_private_and_foreign_selected_videos(self) -> None:
        cases = (
            ({"VIDEO1": "public"}, "VIDEO2", None, "missing"),
            ({"VIDEO1": "private", "VIDEO2": "public"}, None, None, "no longer public"),
            ({"VIDEO1": "public", "VIDEO2": "public"}, None, "VIDEO1", "approved channel"),
        )
        for statuses, remove_id, foreign_id, message in cases:
            with self.subTest(message=message):
                youtube = FakeYouTube(statuses)
                if remove_id:
                    youtube.statuses.pop(remove_id, None)
                if foreign_id:
                    youtube.video_channels[foreign_id] = "FOREIGN"
                with self.assertRaisesRegex(operator.PortfolioYouTubeError, message):
                    operator.playlist_plan(
                        youtube, playlist_manifest(["VIDEO1", "VIDEO2"])
                    )
                self.assertEqual(youtube.playlist_insert_calls, [])

    def test_matching_playlist_rerun_performs_zero_item_mutations(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.playlists_data = [
            {
                "id": "PLAYLIST1",
                "snippet": {"title": portfolio.PLAYLIST_TITLE},
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 2},
            }
        ]
        youtube.playlist_items_by_id["PLAYLIST1"] = [
            playlist_item("ITEM1", "VIDEO1", 0),
            playlist_item("ITEM2", "VIDEO2", 1),
        ]
        data = playlist_manifest(["VIDEO1", "VIDEO2"])
        plan = operator.playlist_plan(youtube, data)

        state = operator.reconcile_playlist(youtube, plan, manifest=data)

        self.assertEqual(state["status"], "VERIFIED")
        self.assertFalse(state["changed"])
        self.assertEqual(state["operations"], [])
        self.assertEqual(youtube.playlist_update_calls, [])
        self.assertEqual(youtube.playlist_item_insert_calls, [])
        self.assertEqual(youtube.playlist_delete_calls, [])

    def test_playlist_application_rejects_membership_drift_before_mutation(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.playlists_data = [
            {
                "id": "PLAYLIST1",
                "snippet": {"title": portfolio.PLAYLIST_TITLE},
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 2},
            }
        ]
        youtube.playlist_items_by_id["PLAYLIST1"] = [
            playlist_item("ITEM1", "VIDEO1", 0),
            playlist_item("ITEM2", "VIDEO2", 1),
        ]
        data = playlist_manifest(["VIDEO1", "VIDEO2"])
        plan = operator.playlist_plan(youtube, data)
        youtube.playlist_items_by_id["PLAYLIST1"].append(
            playlist_item("ITEM3", "VIDEO3", 2)
        )
        state = operator.playlist_application_state(plan)

        with self.assertRaisesRegex(
            operator.PortfolioYouTubeError, "membership or order drifted"
        ):
            operator.reconcile_playlist(
                youtube,
                plan,
                manifest=data,
                state=state,
            )

        self.assertEqual(state["operations"], [])
        self.assertFalse(state["changed"])
        self.assertEqual(youtube.playlist_update_calls, [])
        self.assertEqual(youtube.playlist_item_insert_calls, [])
        self.assertEqual(youtube.playlist_delete_calls, [])

    def test_playlist_application_rejects_second_exact_title_after_planning(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.playlists_data = [
            {
                "id": "PLAYLIST1",
                "snippet": {"title": portfolio.PLAYLIST_TITLE},
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 2},
            }
        ]
        youtube.playlist_items_by_id["PLAYLIST1"] = [
            playlist_item("ITEM1", "VIDEO1", 0),
            playlist_item("ITEM2", "VIDEO2", 1),
        ]
        data = playlist_manifest(["VIDEO1", "VIDEO2"])
        plan = operator.playlist_plan(youtube, data)
        youtube.playlists_data.append(
            {
                "id": "PLAYLIST2",
                "snippet": {"title": portfolio.PLAYLIST_TITLE},
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 0},
            }
        )
        state = operator.playlist_application_state(plan)

        with self.assertRaisesRegex(
            operator.PortfolioYouTubeError,
            "another exact-title playlist appeared after planning",
        ):
            operator.reconcile_playlist(
                youtube,
                plan,
                manifest=data,
                state=state,
            )

        self.assertEqual(state["operations"], [])
        self.assertEqual(youtube.playlist_insert_calls, [])
        self.assertEqual(youtube.playlist_update_calls, [])
        self.assertEqual(youtube.playlist_item_insert_calls, [])
        self.assertEqual(youtube.playlist_delete_calls, [])

    def test_playlist_partial_failure_retains_created_id_operations_and_rollback(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.fail_playlist_action = ("insert", "VIDEO2")
        data = playlist_manifest(["VIDEO1", "VIDEO2"])
        plan = operator.playlist_plan(youtube, data)
        state = operator.playlist_application_state(plan)

        with self.assertRaisesRegex(RuntimeError, "quota"):
            operator.reconcile_playlist(
                youtube,
                plan,
                manifest=data,
                state=state,
            )

        self.assertEqual(state["status"], "STOPPED")
        self.assertTrue(state["created"])
        self.assertEqual(state["playlist_id"], "PLAYLIST_CREATED")
        self.assertEqual(state["rollback"]["created_playlist_id"], "PLAYLIST_CREATED")
        self.assertFalse(state["rollback"]["restore_before_state"]["playlist_existed"])
        self.assertEqual(
            [item["action"] for item in state["operations"]],
            [
                "create_public_playlist",
                "insert_playlist_item",
                "insert_playlist_item",
            ],
        )
        self.assertEqual(
            [item["mutation_succeeded"] for item in state["operations"]],
            [True, True, None],
        )
        self.assertTrue(state["remote_state_uncertain"])

    def test_playlist_readback_failure_retains_successful_insert_and_full_before_state(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.playlists_data = [
            {
                "id": "PLAYLIST1",
                "snippet": {"title": portfolio.PLAYLIST_TITLE},
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 1},
            }
        ]
        youtube.playlist_items_by_id["PLAYLIST1"] = [
            playlist_item("ITEM1", "VIDEO1", 0)
        ]
        data = playlist_manifest(["VIDEO1", "VIDEO2"])
        plan = operator.playlist_plan(youtube, data)
        youtube.fail_playlist_list_call = 4
        state = operator.playlist_application_state(plan)

        with self.assertRaisesRegex(RuntimeError, "readback quota"):
            operator.reconcile_playlist(
                youtube,
                plan,
                manifest=data,
                state=state,
            )

        self.assertEqual(state["status"], "STOPPED")
        self.assertEqual(
            [(item["video_id"], item["position"]) for item in state["before_state"]["items"]],
            [("VIDEO1", 0)],
        )
        self.assertEqual(len(state["operations"]), 1)
        self.assertEqual(state["operations"][0]["action"], "insert_playlist_item")
        self.assertTrue(state["operations"][0]["mutation_succeeded"])
        self.assertEqual(state["readback_items"], [])
        self.assertTrue(state["remote_state_uncertain"])

    def test_playlist_plan_captures_complete_existing_before_state(self) -> None:
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.playlists_data = [
            {
                "id": "PLAYLIST1",
                "snippet": {
                    "title": portfolio.PLAYLIST_TITLE,
                    "description": "Before description",
                },
                "status": {"privacyStatus": "public"},
                "contentDetails": {"itemCount": 2},
            }
        ]
        youtube.playlist_items_by_id["PLAYLIST1"] = [
            playlist_item("ITEM2", "VIDEO2", 0),
            playlist_item("ITEM1", "VIDEO1", 1),
        ]

        plan = operator.playlist_plan(
            youtube, playlist_manifest(["VIDEO1", "VIDEO2"])
        )

        before = plan["before_state"]
        self.assertTrue(before["playlist_existed"])
        self.assertEqual(before["playlist"]["playlist_id"], "PLAYLIST1")
        self.assertEqual(
            before["playlist"]["snippet"]["description"], "Before description"
        )
        self.assertEqual(
            [(item["playlist_item_id"], item["video_id"], item["position"]) for item in before["items"]],
            [("ITEM2", "VIDEO2", 0), ("ITEM1", "VIDEO1", 1)],
        )

    def test_apply_auth_failure_writes_redacted_immutable_stopped_report(self) -> None:
        data = playlist_manifest([])
        validation = {"valid": True, "manifest_sha256": "a" * 64, "errors": []}
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "auth-failure.json"
            argv = [
                "apply_youtube_portfolio.py",
                "playlist",
                "--manifest",
                str(Path(tmpdir) / "manifest.yaml"),
                "--approval",
                str(Path(tmpdir) / "approval.yaml"),
                "--release-readiness",
                str(Path(tmpdir) / "gate.yaml"),
                "--report",
                str(report_path),
                "--apply",
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(
                    operator.portfolio,
                    "validate_manifest_document",
                    return_value=(data, validation),
                ),
                mock.patch.object(
                    operator,
                    "build_youtube",
                    side_effect=RuntimeError("oauth access_token=SUPER_SECRET"),
                ),
                mock.patch("builtins.print"),
                self.assertRaisesRegex(SystemExit, "STOPPED"),
            ):
                operator.main()

            report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "STOPPED")
        self.assertEqual(report["stage"], "AUTHENTICATING")
        self.assertEqual(report["channel"], None)
        self.assertNotIn("SUPER_SECRET", report["error"])
        self.assertIn("details omitted", report["error"])

    def test_invalid_canary_is_rejected_before_validation_or_auth(self) -> None:
        argv = [
            "apply_youtube_portfolio.py",
            "all",
            "--apply",
            "--canary-size",
            "0",
        ]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(
                operator.portfolio, "validate_manifest_document"
            ) as validate,
            mock.patch.object(operator, "build_youtube") as authenticate,
            self.assertRaises(SystemExit) as raised,
        ):
            operator.main()

        self.assertEqual(raised.exception.code, 2)
        validate.assert_not_called()
        authenticate.assert_not_called()

    def test_keyboard_interrupt_retains_durable_partial_journal(self) -> None:
        data = manifest(["VIDEO1", "VIDEO2"])
        validation = {"valid": True, "manifest_sha256": "d" * 64, "errors": []}
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        snapshot_before_second_request: dict = {}
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "interrupted.json"
            journal_path = Path(tmpdir) / "interrupted.journal.json"

            def interrupt_before_second_update(video_id: str) -> None:
                if video_id == "VIDEO2":
                    snapshot_before_second_request.update(
                        json.loads(journal_path.read_text(encoding="utf-8"))
                    )
                    raise KeyboardInterrupt()

            youtube.before_video_update = interrupt_before_second_update
            argv = [
                "apply_youtube_portfolio.py",
                "visibility",
                "--manifest",
                str(Path(tmpdir) / "manifest.yaml"),
                "--approval",
                str(Path(tmpdir) / "approval.yaml"),
                "--release-readiness",
                str(Path(tmpdir) / "gate.yaml"),
                "--report",
                str(report_path),
                "--journal",
                str(journal_path),
                "--canary-size",
                "2",
                "--apply",
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(
                    operator.portfolio,
                    "validate_manifest_document",
                    return_value=(data, validation),
                ),
                mock.patch.object(operator, "build_youtube", return_value=youtube),
                mock.patch("builtins.print"),
                self.assertRaises(KeyboardInterrupt),
            ):
                operator.main()

            report = json.loads(report_path.read_text(encoding="utf-8"))
            final_journal = json.loads(journal_path.read_text(encoding="utf-8"))

        first_checkpoint_operations = snapshot_before_second_request["report"][
            "visibility"
        ]["operations"]
        self.assertTrue(first_checkpoint_operations[0]["mutation_succeeded"])
        self.assertIsNone(first_checkpoint_operations[1]["mutation_succeeded"])
        self.assertEqual(first_checkpoint_operations[1]["mutation_outcome"], "UNKNOWN")
        self.assertEqual(
            snapshot_before_second_request["event"],
            "visibility_mutation_1_attempting",
        )
        self.assertEqual(report["status"], "STOPPED")
        self.assertEqual(report["stage"], "APPLYING_VISIBILITY")
        self.assertEqual(
            [item["mutation_succeeded"] for item in report["visibility"]["operations"]],
            [True, None],
        )
        self.assertTrue(final_journal["final_report_written"])
        self.assertEqual(final_journal["report"]["status"], "STOPPED")

    def test_main_writes_incremental_partial_report_after_visibility_failure(self) -> None:
        data = manifest(["VIDEO1", "VIDEO2"])
        validation = {"valid": True, "manifest_sha256": "c" * 64, "errors": []}
        youtube = FakeYouTube({"VIDEO1": "public", "VIDEO2": "public"})
        youtube.fail_update_id = "VIDEO2"
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "partial.json"
            argv = [
                "apply_youtube_portfolio.py",
                "visibility",
                "--manifest",
                str(Path(tmpdir) / "manifest.yaml"),
                "--approval",
                str(Path(tmpdir) / "approval.yaml"),
                "--release-readiness",
                str(Path(tmpdir) / "gate.yaml"),
                "--report",
                str(report_path),
                "--canary-size",
                "2",
                "--apply",
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(
                    operator.portfolio,
                    "validate_manifest_document",
                    return_value=(data, validation),
                ),
                mock.patch.object(operator, "build_youtube", return_value=youtube),
                mock.patch("builtins.print"),
                self.assertRaisesRegex(SystemExit, "STOPPED"),
            ):
                operator.main()
            report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "STOPPED")
        self.assertEqual(report["stage"], "APPLYING_VISIBILITY")
        self.assertEqual(
            [item["mutation_succeeded"] for item in report["visibility"]["operations"]],
            [True, None],
        )
        self.assertTrue(report["visibility"]["remote_state_uncertain"])
        self.assertEqual(report["visibility"]["rollback"][0]["restore_visibility"], "public")


if __name__ == "__main__":
    unittest.main()
