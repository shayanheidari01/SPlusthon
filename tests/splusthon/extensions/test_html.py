"""
Tests for `splusthon.extensions.html`.
"""
from splusthon.extensions import html
from splusthon.tl.types import MessageEntityBold, MessageEntityItalic, MessageEntityTextUrl


def test_entity_edges():
    """
    Test that entities at the edges (start and end) don't crash.
    """
    text = 'Hello, world'
    entities = [MessageEntityBold(0, 5), MessageEntityBold(7, 5)]
    result = html.unparse(text, entities)
    assert result == '<strong>Hello</strong>, <strong>world</strong>'


def test_malformed_entities():
    """
    Test that malformed entity offsets from bad clients
    don't crash and produce the expected results.
    """
    text = '🏆SoroushPlus Official Android Challenge is over🏆.'
    entities = [MessageEntityTextUrl(offset=2, length=43, url='https://example.com')]
    result = html.unparse(text, entities)
    assert result == '🏆<a href="https://example.com">SoroushPlus Official Android Challenge is over</a>🏆.'


def test_trailing_malformed_entities():
    """
    Similar to `test_malformed_entities`, but for the edge
    case where the malformed entity offset is right at the end
    (note the lack of a trailing dot in the text string).
    """
    text = '🏆SoroushPlus Official Android Challenge is over🏆'
    entities = [MessageEntityTextUrl(offset=2, length=43, url='https://example.com')]
    result = html.unparse(text, entities)
    assert result == '🏆<a href="https://example.com">SoroushPlus Official Android Challenge is over</a>🏆'


def test_entities_together():
    """
    Test that an entity followed immediately by a different one behaves well.
    """
    original = '<strong>⚙️</strong><em>Settings</em>'
    stripped = '⚙️Settings'

    text, entities = html.parse(original)
    assert text == stripped
    assert entities == [MessageEntityBold(0, 2), MessageEntityItalic(2, 8)]

    text = html.unparse(text, entities)
    assert text == original


def test_nested_entities():
    """
    Test that an entity nested inside another one behaves well.
    """
    original = '<a href="https://example.com"><strong>Example</strong></a>'
    original_entities = [MessageEntityTextUrl(0, 7, url='https://example.com'), MessageEntityBold(0, 7)]
    stripped = 'Example'

    text, entities = html.parse(original)
    assert text == stripped
    assert entities == original_entities

    text = html.unparse(text, entities)
    assert text == original


def test_offset_at_emoji():
    """
    Tests that an entity starting at a emoji preserves the emoji.
    """
    text = 'Hi\n👉 See example'
    entities = [MessageEntityBold(0, 2), MessageEntityItalic(3, 2), MessageEntityBold(10, 7)]
    parsed = '<strong>Hi</strong>\n<em>👉</em> See <strong>example</strong>'

    assert html.parse(parsed) == (text, entities)
    assert html.unparse(text, entities) == parsed
