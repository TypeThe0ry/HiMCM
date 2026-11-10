"""Focused integrity-boundary tests for task4_current_research_bindings."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("task4_current_research_bindings.py")
SPEC = importlib.util.spec_from_file_location("current_bindings", SCRIPT)
bindings = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bindings)


REGISTRIES = list(bindings.REGISTRIES)
CONTRACT = bindings.CONTRACT


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


class Fixture:
    """A disposable repo with two registries, reports and a pinned source."""

    def __init__(self, root):
        self.repo = Path(root) / "repo"
        self.analysis = self.repo / "research" / "2026-a"
        self.analysis.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        self.contract = {
            "schema_version": 1,
            "registries": REGISTRIES,
            "reports": {},
            "live_source_sha256": {},
            "historical_sources": [],
        }
        self.registry_values = [{}, {}]
        self.files = {}

    def put(self, name, data):
        path = self.analysis / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            path.write_bytes(data)
        else:
            path.write_text(data, encoding="utf-8")
        self.files[name] = path.read_bytes()
        return path

    def json_file(self, name, value):
        data = (json.dumps(value, sort_keys=True) + "\n").encode()
        self.put(name, data)
        return sha(data)

    def make_report(self, name="results/report/verification.json", source_field="source_sha256", sources=None):
        sources = sources or {}
        report = {source_field: sources}
        h = self.json_file(name, report)
        self.contract["reports"][name] = {"expand_source_maps": [source_field]}
        self.registry_values[0]["report_path"] = name
        self.registry_values[0]["report_path_sha256"] = h
        return name

    def finalize(self):
        for name, value in zip(REGISTRIES, self.registry_values):
            dump(self.analysis / name, value)
        dump(self.analysis / CONTRACT, self.contract)

    def run(self):
        self.finalize()
        return bindings.verify_current_research(self.analysis)

    def historic(self, name, old_data, current_data):
        git_path = "research/2026-a/" + name
        p = self.repo / git_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(old_data)
        subprocess.run(["git", "-C", str(self.repo), "add", git_path], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "historical"], check=True)
        commit = subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "HEAD"], text=True).strip()
        p.write_bytes(current_data)
        h = sha(old_data)
        self.put(name, current_data)
        self.contract["live_source_sha256"][name] = sha(current_data)
        return {"report": "results/report/verification.json", "source_path": name,
                "commit": commit, "git_path": git_path, "sha256": h, "reason": "fixture"}, h


class CurrentResearchBindingTests(unittest.TestCase):
    def fixture(self):
        temp = tempfile.TemporaryDirectory(dir="/data/scratch")
        self.addCleanup(temp.cleanup)
        return Fixture(temp.name)

    def test_nested_source_maps_and_hash_pairs_protect_bytes(self):
        f = self.fixture()
        f.put("data/input.csv", "x\n1\n")
        h = sha(b"x\n1\n")
        f.registry_values[0] = {"nested": {"source_sha256": {"data/input.csv": h}},
                                "audit": "data/input.csv", "verification_sha256": h}
        summary, protected = f.run()
        self.assertEqual(summary["registry_source_maps"], 1)
        self.assertEqual(summary["hash_path_pairs"], 1)
        self.assertEqual(protected[str(f.analysis / "data/input.csv")], h)
        self.assertTrue(any("verification_sha256 -> audit" in x for x in summary["aliases"]))

    def test_both_direct_report_source_map_forms_are_expanded(self):
        for field in ("source_sha256", "source_hashes"):
            with self.subTest(field=field):
                f = self.fixture()
                f.put("inputs/a.txt", b"a")
                f.make_report(source_field=field, sources={"inputs/a.txt": sha(b"a")})
                summary, _ = f.run()
                self.assertEqual(summary["report_direct_source_maps"], 1)
                self.assertEqual(summary["current_reports_checked"], 1)

    def test_modified_and_missing_registered_file_fail(self):
        for mode in ("modified", "missing"):
            with self.subTest(mode=mode):
                f = self.fixture()
                f.put("inputs/a", b"a")
                f.registry_values[0] = {"source_sha256": {"inputs/a": sha(b"a")}}
                if mode == "modified":
                    (f.analysis / "inputs/a").write_bytes(b"b")
                else:
                    (f.analysis / "inputs/a").unlink()
                with self.assertRaises(ValueError):
                    f.run()

    def test_malformed_hashes_and_nonmap_source_map_fail(self):
        for value in ("ABC", "f" * 63, "g" * 64, 7):
            with self.subTest(value=value):
                f = self.fixture()
                f.registry_values[0] = {"source_sha256": {"inputs/a": value}}
                f.put("inputs/a", b"a")
                with self.assertRaises(ValueError):
                    f.run()
        f = self.fixture()
        name = "results/report/verification.json"
        h = f.json_file(name, {"source_sha256": ["bad"]})
        f.contract["reports"][name] = {"expand_source_maps": ["source_sha256"]}
        f.registry_values[0] = {"report_path": name, "report_path_sha256": h}
        with self.assertRaises(ValueError):
            f.run()

    def test_conflicting_duplicate_hash_fails(self):
        f = self.fixture()
        f.put("inputs/a", b"a")
        f.registry_values[0] = {"source_sha256": {"inputs/a": sha(b"a")}}
        f.contract["live_source_sha256"] = {"inputs/a": sha(b"b")}
        with self.assertRaises(ValueError):
            f.run()

    def test_same_source_with_conflicting_registry_hashes_fails(self):
        f = self.fixture()
        f.put("inputs/a", b"a")
        f.registry_values[0] = {"source_sha256": {"inputs/a": sha(b"a")}}
        f.registry_values[1] = {"source_hashes": {"inputs/a": sha(b"b")}}
        with self.assertRaises(ValueError):
            f.run()

    def test_contract_metadata_cannot_be_rebound_to_different_bytes(self):
        f = self.fixture()
        # A source-map binding to the contract itself conflicts with its metadata pin.
        f.registry_values[0] = {"source_sha256": {CONTRACT: sha(b"different")}}
        with self.assertRaises(ValueError):
            f.run()

    def test_unsafe_noncanonical_absolute_traversal_and_symlink_paths_fail(self):
        unsafe = ("/tmp/a", "../outside", "inputs/../a", "inputs//a", "inputs\\a")
        for name in unsafe:
            with self.subTest(name=name):
                f = self.fixture()
                f.registry_values[0] = {"source_sha256": {name: sha(b"a")}}
                with self.assertRaises(ValueError):
                    f.run()
        f = self.fixture()
        outside = Path(f.repo.parent) / "outside"
        outside.write_bytes(b"a")
        (f.analysis / "inputs").mkdir()
        os.symlink(outside, f.analysis / "inputs" / "link")
        f.registry_values[0] = {"source_sha256": {"inputs/link": sha(b"a")}}
        with self.assertRaises(ValueError):
            f.run()

    def test_unpaired_hash_and_unknown_report_policy_fail(self):
        f = self.fixture()
        f.registry_values[0] = {"orphan_sha256": sha(b"x")}
        with self.assertRaises(ValueError):
            f.run()

    def test_report_policy_must_list_every_actual_direct_map(self):
        f = self.fixture()
        name = "results/report/verification.json"
        report = {"source_sha256": {}, "source_hashes": {}}
        h = f.json_file(name, report)
        f.contract["reports"][name] = {"expand_source_maps": ["source_sha256"]}
        f.registry_values[0] = {"report_path": name, "report_path_sha256": h}
        with self.assertRaises(ValueError):
            f.run()

    def test_second_registry_is_included_in_integrity_check(self):
        f = self.fixture()
        f.put("inputs/b", b"b")
        f.registry_values[1] = {"source_sha256": {"inputs/b": sha(b"wrong")}}
        with self.assertRaises(ValueError):
            f.run()
        f = self.fixture()
        f.put("results/report/verification.json", b"{}\n")
        f.registry_values[0] = {"report_path": "results/report/verification.json",
                                "report_path_sha256": sha(b"{}\n")}
        with self.assertRaises(ValueError):
            f.run()

    def test_upstream_historical_graph_is_pinned_but_not_traversed(self):
        f = self.fixture()
        upstream = "results/upstream/verification.json"
        nested = {"source_sha256": {"absent/old-input.csv": "0" * 64}}
        upstream_hash = f.json_file(upstream, nested)
        name = "results/report/verification.json"
        f.json_file(name, {"source_sha256": {upstream: upstream_hash}})
        f.contract["reports"][name] = {"expand_source_maps": ["source_sha256"]}
        f.registry_values[0] = {"report_path": name,
                                "report_path_sha256": sha((json.dumps({"source_sha256": {upstream: upstream_hash}}, sort_keys=True) + "\n").encode())}
        summary, _ = f.run()
        self.assertFalse(summary["transitive_historical_report_graphs_expanded"])
        self.assertEqual(summary["current_reports_checked"], 1)

    def test_historical_pinned_git_version_and_current_counterpart_are_checked(self):
        f = self.fixture()
        path = "design/routes.csv"
        old, current = b"old routes\n", b"current routes\n"
        record, old_hash = f.historic(path, old, current)
        report = "results/report/verification.json"
        report_hash = f.json_file(report, {"source_hashes": {path: old_hash}})
        f.contract["reports"][report] = {"expand_source_maps": ["source_hashes"]}
        f.contract["historical_sources"] = [record]
        f.registry_values[0] = {"report_path": report, "report_path_sha256": report_hash}
        summary, protected = f.run()
        self.assertEqual(summary["historical_source_versions_checked"][0]["commit"], record["commit"])
        self.assertEqual(protected[str(f.analysis / path)], sha(current))

    def test_missing_wrong_or_unpinned_historical_version_fails(self):
        for mutation in ("missing_commit", "wrong_bytes", "no_live_binding"):
            with self.subTest(mutation=mutation):
                f = self.fixture()
                path = "design/routes.csv"
                record, old_hash = f.historic(path, b"old", b"current")
                report = "results/report/verification.json"
                report_hash = f.json_file(report, {"source_sha256": {path: old_hash}})
                f.contract["reports"][report] = {"expand_source_maps": ["source_sha256"]}
                f.contract["historical_sources"] = [record]
                f.registry_values[0] = {"report_path": report, "report_path_sha256": report_hash}
                if mutation == "missing_commit":
                    record["commit"] = "f" * 40
                elif mutation == "wrong_bytes":
                    record["sha256"] = sha(b"other")
                else:
                    f.contract["live_source_sha256"] = {}
                with self.assertRaises(ValueError):
                    f.run()

    def test_checker_does_not_mutate_any_input(self):
        f = self.fixture()
        f.put("inputs/a", b"a")
        f.registry_values[0] = {"source_sha256": {"inputs/a": sha(b"a")}}
        f.finalize()
        before = {p.relative_to(f.analysis).as_posix(): p.read_bytes()
                  for p in f.analysis.rglob("*") if p.is_file()}
        bindings.verify_current_research(f.analysis)
        after = {p.relative_to(f.analysis).as_posix(): p.read_bytes()
                 for p in f.analysis.rglob("*") if p.is_file()}
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
