from app.sender import TwilioMessenger

def test_send_whatsapp_mock(monkeypatch):
    class MockClient:
        def messages(self):
            class Message:
                def create(self, from_, to, body):
                    return type("msg", (), {"sid": "fake_sid"})
            return Message()
    monkeypatch.setattr("app.sender.Client", lambda *a, **kw: MockClient())
    sender = TwilioMessenger("sid", "token", "from")
    sid = sender.send_whatsapp("to", "Hola")
    assert sid == "fake_sid"
