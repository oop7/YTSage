import unittest

from ytsage.core.ytsage_yt_dlp import (
    YOUTUBE_PLAYER_CLIENTS,
    get_youtube_player_client_args,
)


class YouTubePlayerClientArgsTests(unittest.TestCase):
    def test_auto_preserves_existing_no_cookie_fallback(self) -> None:
        self.assertEqual(
            get_youtube_player_client_args("auto", has_cookies=False),
            [
                "--extractor-args",
                "youtube:player_client=web_embedded,default",
            ],
        )

    def test_auto_leaves_cookie_client_selection_to_ytdlp(self) -> None:
        self.assertEqual(
            get_youtube_player_client_args("auto", has_cookies=True),
            [],
        )

    def test_explicit_client_is_used_with_or_without_cookies(self) -> None:
        expected = ["--extractor-args", "youtube:player_client=ios_producer"]
        self.assertEqual(
            get_youtube_player_client_args("ios_producer", has_cookies=False),
            expected,
        )
        self.assertEqual(
            get_youtube_player_client_args("ios_producer", has_cookies=True),
            expected,
        )

    def test_only_retained_clients_can_be_selected(self) -> None:
        retained_clients = {
            "web_safari",
            "web_embedded",
            "ios_producer",
            "visionos",
            "tv_samsung",
        }
        self.assertEqual(set(YOUTUBE_PLAYER_CLIENTS) - {"auto"}, retained_clients)
        for player_client in YOUTUBE_PLAYER_CLIENTS:
            if player_client == "auto":
                continue
            with self.subTest(player_client=player_client):
                self.assertEqual(
                    get_youtube_player_client_args(player_client, has_cookies=True),
                    ["--extractor-args", f"youtube:player_client={player_client}"],
                )

    def test_removed_client_falls_back_to_auto(self) -> None:
        self.assertEqual(
            get_youtube_player_client_args("web", has_cookies=False),
            [
                "--extractor-args",
                "youtube:player_client=web_embedded,default",
            ],
        )

    def test_unknown_saved_client_falls_back_to_auto(self) -> None:
        self.assertEqual(
            get_youtube_player_client_args("unknown", has_cookies=False),
            [
                "--extractor-args",
                "youtube:player_client=web_embedded,default",
            ],
        )


if __name__ == "__main__":
    unittest.main()
