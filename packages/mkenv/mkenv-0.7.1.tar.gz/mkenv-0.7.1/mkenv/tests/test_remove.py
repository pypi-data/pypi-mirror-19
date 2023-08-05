from unittest import TestCase
import os

from mkenv import remove
from mkenv.tests.utils import CLIMixin


class TestRemove(CLIMixin, TestCase):

    cli = remove

    def test_remove_removes_an_env_with_the_given_name(self):
        boom = self.locator.for_name("boom")
        boom.create()
        self.assertTrue(boom.exists)
        self.run_cli(["boom"])
        self.assertFalse(boom.exists)

    def test_cannot_remove_non_existing_envs(self):
        boom = self.locator.for_name("boom")
        self.assertFalse(boom.exists)
        self.run_cli(["boom"], exit_status=os.EX_NOINPUT)

    def test_can_remove_non_existing_envs_with_force(self):
        boom = self.locator.for_name("boom")
        self.assertFalse(boom.exists)
        self.run_cli(["--force", "boom"])
