#!/usr/bin/env python3
"""Unit tests for the guards and record builders in workflows/bsky.py.

No network, no credentials: every test uses a throwaway audit log.
Run: python3 workflows/test_bsky.py
"""

import json
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bsky  # noqa: E402


def rec(action, ts, **extra):
    return {"v": 1, "ts": bsky.iso(ts), "account": "lt", "action": action, "status": "ok", **extra}


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".ndjson", delete=False)
        self.tmp.close()
        self.log = Path(self.tmp.name)
        self.acct = bsky.Account("lt")

    def tearDown(self):
        self.log.unlink(missing_ok=True)

    def write(self, records):
        self.log.write_text("\n".join(json.dumps(r) for r in records) + "\n")

    def test_reply_cap_five_in_24h(self):
        now = bsky.now_utc()
        self.write([rec("reply", now - timedelta(minutes=20 * i + 20), thread_root=f"t{i}")
                    for i in range(5)])
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.guard_reply(self.acct, "t9", log=self.log)
        self.assertIn("reply cap reached", str(ctx.exception))

    def test_reply_spacing_ten_minutes(self):
        now = bsky.now_utc()
        self.write([rec("reply", now - timedelta(seconds=60), thread_root="t1")])
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.guard_reply(self.acct, "t2", log=self.log)
        self.assertIn("minimum 600s", str(ctx.exception))

    def test_two_replies_per_thread(self):
        now = bsky.now_utc()
        self.write([rec("reply", now - timedelta(minutes=15), thread_root="root-A"),
                    rec("reply", now - timedelta(minutes=12), thread_root="root-A")])
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.guard_reply(self.acct, "root-A", log=self.log)
        self.assertIn("thread limit", str(ctx.exception))

    def test_force_bypasses_and_records(self):
        now = bsky.now_utc()
        self.write([rec("reply", now - timedelta(seconds=30), thread_root="root-A")])
        out = bsky.guard_reply(self.acct, "root-A", force=True, log=self.log)
        self.assertTrue(out["forced"])

    def test_post_cap(self):
        now = bsky.now_utc()
        self.write([rec("post", now - timedelta(minutes=i + 1)) for i in range(bsky.POST_CAP_24H)])
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.guard_post(self.acct, 1, log=self.log)
        self.assertIn("post cap", str(ctx.exception))

    def test_old_actions_drop_out_of_the_window(self):
        now = bsky.now_utc()
        self.write([rec("post", now - timedelta(hours=25)) for _ in range(30)])
        self.assertEqual(bsky.guard_post(self.acct, 1, log=self.log)["posts_24h"], 0)


class InputTests(unittest.TestCase):
    def test_text_limit_is_graphemes(self):
        self.assertEqual(bsky.graphemes("café"), 4)
        self.assertEqual(bsky.graphemes("👋🏽"), 2)  # emoji + skin-tone modifier
        self.assertEqual(len(bsky.validate_text("a" * 300)), 300)
        with self.assertRaises(bsky.Refused):
            bsky.validate_text("a" * 301)

    def test_empty_text_refused(self):
        with self.assertRaises(bsky.Refused):
            bsky.validate_text("   ")

    def test_naive_timestamp_refused(self):
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.parse_iso("2026-11-13T12:05:00", "publish_at")
        self.assertIn("UTC offset", str(ctx.exception))

    def test_aware_timestamp_parses(self):
        dt = bsky.parse_iso("2026-11-13T12:05:00-06:00")
        self.assertEqual(dt.astimezone(bsky.timezone.utc).hour, 18)

    def test_facets_use_byte_offsets(self):
        text = "é https://example.com/x"
        facets = bsky.build_facets(text, resolve_mentions=False)
        url_at = text.index("https")
        start = len(text[:url_at].encode())
        self.assertIsNotNone(facets)
        self.assertEqual(facets[0]["index"]["byteStart"], start)
        self.assertNotEqual(start, url_at)  # é is 2 bytes: offsets must differ

    def test_facets_none_for_plain_text(self):
        self.assertIsNone(bsky.build_facets("no links here", resolve_mentions=False))

    def test_trailing_punctuation_trimmed_from_link(self):
        facets = bsky.build_facets("see https://example.com/x.", resolve_mentions=False)
        self.assertIsNotNone(facets)
        self.assertEqual(facets[0]["features"][0]["uri"], "https://example.com/x")


class QuoteTests(unittest.TestCase):
    """Quote posts: embed.record shape, quote_asset resolution, refusals."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.outbox = Path(self.tmp.name)
        self._outbox = bsky.OUTBOX
        bsky.OUTBOX = self.outbox
        self._public = bsky.public_call
        bsky.public_call = lambda method, params: {
            "posts": [{"uri": params["uris"][0], "cid": "bafyfakecid"}]}
        self.log = self.outbox / "audit.ndjson"

    def tearDown(self):
        bsky.OUTBOX = self._outbox
        bsky.public_call = self._public
        self.tmp.cleanup()

    def item(self, name, **fields):
        path = self.outbox / f"{name}.json"
        path.write_text(json.dumps({"id": name, **fields}))
        return path

    def test_quote_asset_resolves_published_uri(self):
        self.item("target", uri="at://did:plc:a/app.bsky.feed.post/abc")
        self.assertEqual(bsky.resolve_quote({"id": "q", "quote_asset": "target"}),
                         "at://did:plc:a/app.bsky.feed.post/abc")

    def test_quote_asset_not_published_refuses(self):
        self.item("target")
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.resolve_quote({"id": "q", "quote_asset": "target"})
        self.assertIn("has not published yet", str(ctx.exception))

    def test_quote_asset_missing_item_refuses(self):
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.resolve_quote({"id": "q", "quote_asset": "ghost"})
        self.assertIn("no outbox item", str(ctx.exception))

    def test_explicit_and_asset_together_refused(self):
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.resolve_quote({"id": "q", "quote": "at://did:plc:a/app.bsky.feed.post/1",
                                "quote_asset": "target"})
        self.assertIn("not both", str(ctx.exception))

    def test_no_quote_returns_none(self):
        self.assertIsNone(bsky.resolve_quote({"id": "q"}))

    def test_dry_run_record_uses_strong_ref(self):
        acct = bsky.Account("lt")
        entry = bsky.do_post(acct, "Quote post body", quote="at://did:plc:a/app.bsky.feed.post/abc",
                             dry_run=True, log=self.log)
        embed = entry["record"]["embed"]
        self.assertEqual(embed["$type"], "app.bsky.embed.record")
        self.assertEqual(embed["record"], {"uri": "at://did:plc:a/app.bsky.feed.post/abc",
                                           "cid": "bafyfakecid"})
        self.assertEqual(entry["audit"]["quote"], "at://did:plc:a/app.bsky.feed.post/abc")

    def test_non_at_uri_quote_refused(self):
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.do_post(bsky.Account("lt"), "body", quote="https://bsky.app/x", dry_run=True, log=self.log)
        self.assertIn("must be an AT-URI", str(ctx.exception))

    def test_quote_with_images_refused(self):
        img = self.outbox / "x.png"
        img.write_bytes(b"not-an-image")
        with self.assertRaises(bsky.Refused) as ctx:
            bsky.do_post(bsky.Account("lt"), "body", images=[img], alts=["a"],
                         quote="at://did:plc:a/app.bsky.feed.post/abc", dry_run=True, log=self.log)
        self.assertIn("cannot also carry images", str(ctx.exception))


class CredentialTests(unittest.TestCase):
    def test_fb_without_password_refuses(self):
        acct = bsky.Account("fb")
        acct.password = ""
        with self.assertRaises(bsky.Refused) as ctx:
            acct.require_credentials()
        self.assertIn("FLAMBEEE_BSKY_APP_PASSWORD", str(ctx.exception))

    def test_unknown_account_refused(self):
        with self.assertRaises(bsky.Refused):
            bsky.Account("nope")

    def test_app_password_shape(self):
        self.assertTrue(bsky.APP_PW_RE.match("abcd-efgh-ijkl-mnop"))
        self.assertFalse(bsky.APP_PW_RE.match("hunter2hunter2"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
