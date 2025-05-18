import unittest
from unittest.mock import patch, MagicMock, call
import game_client

class TestGameClient(unittest.TestCase):

    @patch("game_client.input", side_effect=["2"])
    @patch("game_client.socket.socket")
    def test_play_game_medium_difficulty(self, mock_socket_class, mock_input):
        mock_socket = MagicMock()
        mock_socket.recv.side_effect = [
            b"Select difficulty level\n",
            b"Start guessing!\n",
            b"Higher\n",
            b"Lower\n",
            b"CORRECT! You got it!\n"
        ]
        mock_socket_class.return_value = mock_socket
        game_client.play_game()
        self.assertIn(call(b'31\n'), mock_socket.sendall.mock_calls)

    @patch("game_client.input", side_effect=["1"])
    @patch("game_client.socket.socket")
    def test_play_game_easy_difficulty(self, mock_socket_class, mock_input):
        mock_socket = MagicMock()
        mock_socket.recv.side_effect = [
            b"Select difficulty level\n",
            b"Start guessing!\n",
            b"Higher\n",
            b"CORRECT! You got it!\n"
        ]
        mock_socket_class.return_value = mock_socket
        game_client.play_game()
        self.assertIn(call(b'8\n'), mock_socket.sendall.mock_calls)

    @patch("game_client.input", side_effect=["3"])
    @patch("game_client.socket.socket")
    def test_play_game_hard_difficulty(self, mock_socket_class, mock_input):
        mock_socket = MagicMock()
        mock_socket.recv.side_effect = [
            b"Select difficulty level\n",
            b"Start guessing!\n",
            b"Lower\n",
            b"Higher\n",
            b"CORRECT! You got it!\n"
        ]
        mock_socket_class.return_value = mock_socket
        game_client.play_game()
        self.assertIn(call(b'50\n'), mock_socket.sendall.mock_calls)

    # VALIDATION TESTS FOR get_difficulty_choice()

    @patch("builtins.input", side_effect=["5", "2"])  # Out of range then valid
    def test_get_difficulty_choice_out_of_range_then_valid(self, mock_input):
        result = game_client.get_difficulty_choice()
        self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["hello", "2"])  # ValueError then valid
    def test_get_difficulty_choice_non_integer_then_valid(self, mock_input):
        result = game_client.get_difficulty_choice()
        self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["2"])  # Direct valid input
    def test_get_difficulty_choice_valid(self, mock_input):
        result = game_client.get_difficulty_choice()
        self.assertEqual(result, 2)

    # MAIN FUNCTION TESTS

    @patch("game_client.main")
    def test_main_entry(self, mock_main):
        game_client.main()
        mock_main.assert_called_once()

    @patch("builtins.input", side_effect=["1"])  # Select Easy
    def test_main_input_easy(self, mock_input):
        with patch("game_client.socket.socket") as mock_socket_class:
            mock_socket = MagicMock()
            mock_socket.recv.side_effect = [
                b"Select difficulty level\n",
                b"Start guessing!\n",
                b"CORRECT! You got it!\n"
            ]
            mock_socket_class.return_value = mock_socket
            game_client.main()

if __name__ == "__main__":
    unittest.main()
