import unittest
from types import SimpleNamespace

from src.llm.client import ask


class FakeClient:
    def __init__(self):
        self.calls = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        self.calls.append(kwargs)
        message = SimpleNamespace(content="ok")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class AskReasoningTest(unittest.TestCase):
    def test_default_keeps_model_behaviour(self):
        client = FakeClient()
        ask([{"role": "user", "content": "x"}], client=client, temperature=0)
        self.assertNotIn("reasoning_effort", client.calls[0])
        self.assertNotIn("reasoning", client.calls[0])
        self.assertEqual(client.calls[0]["temperature"], 0)

    def test_disabled_sends_reasoning_effort_none(self):
        client = FakeClient()
        ask([{"role": "user", "content": "x"}], client=client, reasoning=False)
        self.assertEqual(client.calls[0]["reasoning_effort"], "none")
        self.assertNotIn("reasoning", client.calls[0])


if __name__ == "__main__":
    unittest.main()
