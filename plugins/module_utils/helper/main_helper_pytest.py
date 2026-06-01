import pytest

# todo: add more tests for simplify_translate and other essential functions to catch regressions


@pytest.mark.parametrize('existing, translate, simple', [
    ({'api_name': 'value'}, {'ansible_name': 'api_name'}, {'ansible_name': 'value'}),
    ({'api': {'name': 'value'}}, {'ansible_name': ('api', 'name')}, {'ansible_name': 'value'}),
])
def test_simplify_translate_translate(existing, translate, simple):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import simplify_translate

    assert simple == simplify_translate(existing=existing, translate=translate, ignore=['api'])


def test_simplify_translate_skips_missing_typed_fields():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import simplify_translate

    existing = {'name': 'WAN_DHCP6', 'ipprotocol': 'inet6'}
    translate = {'ip_protocol': 'ipprotocol', 'far_gw': 'fargw'}
    typing = {'bool': ['far_gw'], 'select': ['ip_protocol']}

    assert simplify_translate(existing=existing, translate=translate, typing=typing) == {
        'name': 'WAN_DHCP6',
        'ip_protocol': 'inet6',
    }
