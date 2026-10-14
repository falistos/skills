"""Unit tests for scripts/ci: python3 skills/fast-ci/scripts/ci_test.py (stdlib only)."""
import importlib.machinery
import importlib.util
import os
import sys
import unittest

sys.dont_write_bytecode = True  # keep installed skill folders clean

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ci")
_spec = importlib.util.spec_from_loader("ci", importlib.machinery.SourceFileLoader("ci", _path))
ci = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ci)


class Classify(unittest.TestCase):
    def kind(self, text, conclusion="failure"):
        return ci.classify(text, conclusion)[:2]

    def test_infra(self):
        cases = {
            "actions budget": "The job was not started because an Actions budget is preventing further use.",
            "runner lost": "The runner has received a shutdown signal. This can happen when the runner service is stopped",
            "no space left": "tar: write error: No space left on device",
            "runner permission": "EACCES: permission denied, mkdir '/home/runner/_work/_temp/x'",
            "wrong architecture": "/usr/local/bin/protoc: cannot execute binary file: Exec format error",
        }
        for cause, line in cases.items():
            with self.subTest(cause):
                self.assertEqual(self.kind(line), ("infra", cause))

    def test_network_is_unclear(self):
        self.assertEqual(self.kind("curl: (28) Failed to connect: Connection timed out after 30000 milliseconds"),
                         ("unclear", "network"))

    def test_wrong_arch_go_crash(self):
        self.assertEqual(self.kind("fatal error: lfstack.push"), ("infra", "wrong architecture"))

    def test_timed_out_conclusion(self):
        self.assertEqual(self.kind("anything", "timed_out"), ("unclear", "timeout"))

    def test_step_timeout_message(self):
        self.assertEqual(self.kind("The job running on runner runner-1 has exceeded the maximum execution time of 30 minutes."),
                         ("unclear", "timeout"))

    def test_code(self):
        for line in [
            "error[E0308]: mismatched types",
            "FAILED tests/test_api.py::test_login - AssertionError",
            "A public key has been found, but no private key. Make sure to set `TAURI_SIGNING_PRIVATE_KEY`",
            "ERROR: permission denied for table users",
            "Error: Process completed with exit code 1.",
        ]:
            with self.subTest(line):
                self.assertEqual(self.kind(line)[0], "code")

    def test_evidence_is_the_matching_line(self):
        self.assertEqual(ci.classify("a\nENOSPC: no space left on device, write\nb", "failure")[2],
                         "ENOSPC: no space left on device, write")


class Logs(unittest.TestCase):
    RAW = ("﻿2026-10-13T22:55:23.1196070Z ##[group]Run make\n"
           "2026-10-13T22:55:23.1196253Z \x1b[36;1mmake test\x1b[0m\n"
           "2026-10-13T22:55:23.1207886Z ##[endgroup]\n"
           "2026-10-13T22:55:24.0000000Z boom\r\n"
           "2026-10-13T22:55:24.1000000Z ##[error]Process completed with exit code 2.\n"
           "2026-10-13T22:55:25.0000000Z Post job cleanup.\n")

    def test_clean_strips_ansi_timestamps_bom(self):
        lines = ci.clean_log(self.RAW)
        self.assertEqual(lines[1], "make test")
        self.assertEqual(lines[0], "##[group]Run make")
        self.assertEqual(lines[3], "boom")

    def test_failed_step_lines_stop_at_error_and_skip_earlier_steps(self):
        self.assertEqual(ci.failed_step_lines(ci.clean_log(self.RAW)),
                         ["boom", "##[error]Process completed with exit code 2."])

    def test_no_error_marker_keeps_everything_after_last_group(self):
        self.assertEqual(ci.failed_step_lines(["##[endgroup]", "a", "b", ""]), ["a", "b"])


def _run(name, sha, created, event="pull_request", attempt=1):
    return {"name": name, "head_sha": sha, "created_at": created, "event": event, "status": "completed",
            "run_attempt": attempt}


def _job(name, started, completed, conclusion="success"):
    return {"name": name, "status": "completed", "conclusion": conclusion, "started_at": started,
            "completed_at": completed}


class Verdict(unittest.TestCase):
    T = "2026-10-14T10:%02d:00Z"

    def runs(self):
        t = self.T
        ci_run = _run("CI", "a", t % 0)
        bench = _run("Bench", "a", t % 0)
        return [
            (ci_run, [_job("test", t % 1, t % 9), _job("lint", t % 1, t % 3), _job("ci-ok", t % 9, t % 10)]),
            (bench, [_job("bench", t % 1, t % 30)]),
        ]

    def test_required_check_sets_the_verdict_and_optional_jobs_do_not(self):
        [v], left_out, external = ci.pr_verdicts(self.runs(), {"ci-ok"})
        self.assertEqual((left_out, external), (0, []))
        self.assertEqual(v["s"], 600)
        self.assertEqual(v["pole"], ("CI", "test"))
        self.assertFalse(v["red"])

    def test_unknown_required_checks_count_every_check(self):
        [v] = ci.pr_verdicts(self.runs(), None)[0]
        self.assertEqual(v["s"], 1800)
        self.assertEqual(v["pole"], ("Bench", "bench"))

    def test_incomplete_commits_and_push_runs_are_skipped(self):
        runs = self.runs()
        runs[1][0]["status"] = "in_progress"
        self.assertEqual(ci.pr_verdicts(runs, {"ci-ok"})[:2], ([], 1))
        push = [(_run("CI", "b", self.T % 0, event="push"), [_job("ci-ok", self.T % 1, self.T % 2)])]
        self.assertEqual(ci.pr_verdicts(push, {"ci-ok"})[0], [])

    def test_a_commit_missing_a_required_check_is_left_out(self):
        t = self.T
        runs = self.runs() + [(_run("Other", "c", t % 0), [_job("lint", t % 1, t % 2)])]
        verdicts, left_out, _ = ci.pr_verdicts(runs, {"ci-ok"})
        self.assertEqual((len(verdicts), left_out), (1, 1))

    def test_a_skipped_required_check_still_ends_the_verdict(self):
        t = self.T
        runs = [(_run("CI", "d", t % 0), [_job("a", t % 1, t % 2), _job("b", t % 3, t % 10, "skipped")])]
        [v] = ci.pr_verdicts(runs, {"a", "b"})[0]
        self.assertEqual((v["s"], v["red"]), (600, False))

    def test_required_checks_outside_actions_are_reported(self):
        self.assertEqual(ci.pr_verdicts(self.runs(), {"ci-ok", "codecov/patch"})[2], ["codecov/patch"])


class RequiredState(unittest.TestCase):
    def test_expected_check_not_created_yet_is_pending(self):
        self.assertEqual(ci.required_state([], {"ci-ok"}), (["ci-ok"], False))

    def test_red_as_soon_as_one_required_check_fails(self):
        rollup = [{"name": "a", "bucket": "fail"}, {"name": "b", "bucket": "pending"}]
        self.assertEqual(ci.required_state(rollup, None), (["b"], True))

    def test_green_when_all_reported_and_done(self):
        rollup = [{"name": "a", "bucket": "pass"}, {"name": "b", "bucket": "skipping"}]
        self.assertEqual(ci.required_state(rollup, {"a"}), ([], False))


class Helpers(unittest.TestCase):
    def test_p90_and_median(self):
        self.assertEqual(ci.p90(list(range(1, 11))), 9)
        self.assertIsNone(ci.p90([]))
        self.assertEqual(ci.median([1, 3, 2]), 2)

    def test_fmt_dur(self):
        self.assertEqual([ci.fmt_dur(x) for x in (None, 5, 65, 3700)], ["-", "5s", "1m05s", "1h01m"])

    def test_parse_target(self):
        self.assertEqual(ci.parse_target("62", "r"), (62, None))
        self.assertEqual(ci.parse_target("#62", "r"), (62, None))
        self.assertEqual(ci.parse_target("41ab8a6", "r"), (None, "41ab8a6"))
        self.assertEqual(ci.parse_target(None, "r"), (None, None))
        with self.assertRaises(ci.CiError):
            ci.parse_target("nope", "r")

    def test_pending_includes_runs_that_may_still_add_jobs(self):
        checks = [{"name": "a", "status": "completed"}]
        runs = [{"name": "wf", "status": "in_progress"}]
        self.assertEqual(ci.pending(checks, runs), ["run wf (in_progress)"])


if __name__ == "__main__":
    unittest.main()
