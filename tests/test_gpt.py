from app.gpt import GPTHandler

def test_generar_folio_format():
    gpt = GPTHandler(api_key="test")
    folio = gpt.generar_folio()
    assert folio.startswith("KVK25-")
    assert len(folio.split("-")[1]) == 6
