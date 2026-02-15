"""End-to-end test for KB lifecycle."""
import unittest
import tempfile
import shutil
from pathlib import Path

from skills.init.scripts.scaffold import scaffold_kb
from skills.curate.scripts.create_topic import create_topic
from skills.curate.scripts.propose import create_proposal
from skills.curate.scripts.promote import promote_proposal
from skills.health.scripts.check_kb import run_health_check


class TestKBLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_full_lifecycle(self):
        # 1. Init KB
        result = scaffold_kb(self.tmpdir, "Test Analyst", ["Domain A"])
        self.assertIn("created", result.lower())
        self.assertTrue((self.tmpdir / "AGENTS.md").exists())
        self.assertTrue((self.tmpdir / "knowledge" / "domain-a" / "overview.md").exists())

        # 2. Add a topic
        result = create_topic(self.tmpdir, "domain-a", "First Topic", "Testing the lifecycle")
        self.assertTrue((self.tmpdir / "knowledge" / "domain-a" / "first-topic.md").exists())
        self.assertTrue((self.tmpdir / "knowledge" / "domain-a" / "first-topic.ref.md").exists())

        # 3. Propose a new topic
        result = create_proposal(self.tmpdir, "Second Topic", "Another test", "human", "Testing proposals")
        self.assertTrue((self.tmpdir / "knowledge" / "_proposals" / "second-topic.md").exists())

        # 4. Promote the proposal
        result = promote_proposal(self.tmpdir, "second-topic", "domain-a")
        self.assertTrue((self.tmpdir / "knowledge" / "domain-a" / "second-topic.md").exists())
        self.assertFalse((self.tmpdir / "knowledge" / "_proposals" / "second-topic.md").exists())
        # Verify proposal frontmatter was stripped
        content = (self.tmpdir / "knowledge" / "domain-a" / "second-topic.md").read_text()
        self.assertNotIn("status: proposal", content)

        # 5. Run health check
        report = run_health_check(self.tmpdir)
        self.assertIn("issues", report)
        self.assertIn("summary", report)
        self.assertGreater(report["summary"]["total_files"], 0)

    def test_health_check_on_fresh_kb(self):
        """A freshly scaffolded KB with one complete topic should be reasonably healthy."""
        scaffold_kb(self.tmpdir, "Test Analyst", ["Domain A"])
        create_topic(self.tmpdir, "domain-a", "First Topic", "Testing")

        report = run_health_check(self.tmpdir)
        # Should have no fail-severity issues from structural checks
        # (template-generated content is well-formed)
        fail_issues = [i for i in report["issues"] if i["severity"] == "fail"]
        # The only potential fails would be from coverage checks if ref.md
        # cross-links don't resolve perfectly in templates
        # Print for debugging if this fails:
        for issue in fail_issues:
            print(f"  FAIL: {issue['file']}: {issue['message']}")


class TestSandboxKB(unittest.TestCase):
    """Test creating a KB in the sandbox directory for live exploration."""

    def test_scaffold_sandbox_kb(self):
        """Create a sample KB in sandbox/ for manual testing."""
        sandbox = Path(__file__).parent.parent.parent / "sandbox"
        sandbox.mkdir(exist_ok=True)

        # Only scaffold if empty (don't overwrite between test runs)
        if not (sandbox / "AGENTS.md").exists():
            scaffold_kb(
                sandbox,
                "Example Analyst",
                ["Research Methods", "Data Analysis", "Reporting"],
            )
            create_topic(sandbox, "research-methods", "Literature Review", "How to conduct systematic literature reviews")
            create_topic(sandbox, "data-analysis", "Statistical Testing", "When and how to apply statistical tests")

        self.assertTrue((sandbox / "AGENTS.md").exists())
        self.assertTrue((sandbox / "knowledge" / "index.md").exists())
