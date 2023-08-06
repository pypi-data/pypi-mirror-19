import pytest
from . import text
from ... import matchers, Story
from ...utils import answer, build_fake_session, build_fake_user, SimpleTrigger

story = None


def teardown_function(function):
    print('tear down!')
    story and story.clear()


@pytest.mark.asyncio
async def test_should_run_story_on_equal_message():
    trigger = SimpleTrigger()
    session = build_fake_session()
    user = build_fake_user()

    global story
    story = Story()

    @story.on('hi there!')
    def one_story():
        @story.part()
        def then(message):
            trigger.passed()

    await answer.pure_text('hi there!', session, user, story)

    assert trigger.is_triggered


@pytest.mark.asyncio
async def test_should_not_run_story_on_non_equal_message():
    trigger = SimpleTrigger()
    session = build_fake_session()
    user = build_fake_user()

    global story
    story = Story()

    @story.on('hi there!')
    def one_story():
        @story.part()
        def then(message):
            trigger.passed()

    await answer.pure_text('buy!', session, user, story)

    assert not trigger.is_triggered


@pytest.mark.asyncio
async def test_should_catch_any_text_message():
    trigger = SimpleTrigger()
    session = build_fake_session()
    user = build_fake_user()

    global story
    story = Story()

    @story.on(text.Any())
    def one_story():
        @story.part()
        def then(message):
            trigger.passed()

    await answer.pure_text('hi there!', session, user, story)

    assert trigger.is_triggered


@pytest.mark.asyncio
async def test_should_ignore_any_non_text_message():
    trigger = SimpleTrigger()
    session = build_fake_session()
    user = build_fake_user()

    global story
    story = Story()

    @story.on(text.Any())
    def one_story():
        @story.part()
        def then(message):
            trigger.passed()

    await answer.location('some where', session, user, story)

    assert not trigger.is_triggered


def test_serialize_text_any():
    m_old = text.Any()
    m_new = matchers.deserialize(matchers.serialize(m_old))
    assert isinstance(m_new, text.Any)
