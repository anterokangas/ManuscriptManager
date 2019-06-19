
from manuscript.elements.work import Work
from manuscript.elements.settings import Settings
import manuscript.tools.constants as mc


def test__init__():
    text = "Test"
    work = Work(text)

    assert (work.settings.name == mc.SETTINGS
            and work.settings.default_lang == mc.DEFAULT_LANG
            and work.settings.data_dirs == [".", "data"]
            and work.settings.temp_dir == "."
            and work.settings.page_width == mc.PAGE_WIDTH
            and work.settings.page_length == mc.PAGE_LENGTH
            and work.settings.text_export == "output.txt"
            and work.settings.export == "output.mp3"
            and work.settings.format == "mp3"
            and work.settings.title == ""
            and work.settings.artist == "Various Artists"
            and work.settings.album == ""
            and work.settings.comments == ""
            and work.settings.date == ""
            and work.settings.genre == ""
            and work.settings.cover == ""
            and work.settings.play_final is True
            and work.settings.print_final_text is False
            and work.settings.play_while is False
            and work.settings.print_supported_languages is False
            and work.settings.print_defining_actions is False
            and work.settings.print_defined_actions is False
            and work.settings.print_manuscript_text is False
            and work.settings.print_manuscript_parsed is False
            and work.settings.print_executions is False
            )

    Settings(work, default_lang="sv")
    print(f"work.settings.default_lang={work.settings.default_lang}")
    assert work.settings.default_lang == "sv"


if __name__ == "__main__":
    test__init__()
