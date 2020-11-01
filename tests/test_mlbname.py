import mlbname

def test_real_name():
    assert mlbname.translate("Noah Syndergaard") == "ノア・シンダーガード"

def test_mix_name():
    assert mlbname.translate("Max Verlander") == "マックス・バーランダー"

def test_dummy_name():
    assert mlbname.translate("AAA BBB") == "AAA・BBB"