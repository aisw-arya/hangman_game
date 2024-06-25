import unittest
from hangman import get_word,image,start,masking_word,validation,previous_choice,chance_left,unmasking_word,result
from io import StringIO
import sys
from unittest.mock import patch,MagicMock

class TestGetWord(unittest.TestCase):
    def test_get_word(self):
        word= get_word()
        
        self.assertIsInstance(word, str)  # Check if the returned word is a string
        self.assertTrue(len(word) > 0)    # Check if the returned word is not empty

   
class TestImageFunction(unittest.TestCase):
    
    @patch('builtins.print')
    def test_image(self, mock_print):
        image(6)
        mock_print.assert_any_call(
            "|_______\n|  |\n|\n|\n|\n|\n|_"
        )


class TestStartFunction(unittest.TestCase):


    @patch('hangman.result')
    @patch('builtins.print')
    def test_start(self,mock_print, mocked_result):
        start()
        mock_print.assert_any_call(
           '___Welcome__'

        )
        mock_print.assert_any_call(
           """Rules for this game:
            1.Guess a word.
            2.You're allowed to guess using any letter of the alphabet.
            3.You have a total of 7 chances.
            4.If you fail to guess correctly, the hangman will be gradually drawn."""
        )

        mock_print.assert_any_call(
            "Let's start the game."
        )
        mocked_result.assert_called_once()


class TestMaskingwordFunction(unittest.TestCase):

    def setUp(self):
        self.word = "hangman"



    def test_initial_maskedword(self):
        word=""
        masked_word=masking_word(word)
        expected_masked_word = ""
        self.assertEqual(masked_word,expected_masked_word)

    def test_length_of_the_word(self):
        masked_word = masking_word(self.word)
        self.assertEqual(len(masked_word),len(self.word))

    def test_maked_word_output(self):
        masked_word = masking_word(self.word)
        expected_masked_word = "-------"
        self.assertEqual(masked_word,expected_masked_word)



class TestValidationFunction(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        
    def tearDown(self):
         sys.stdout = sys.__stdout__ 

    def test_alphabet_small(self):
        guessed_letter = "a"
        result = validation(guessed_letter)
        self.assertFalse(result)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_alphabet_Capital(self):
        guessed_letter = "A"
        result = validation(guessed_letter)
        self.assertFalse(result)
        self.assertEqual(self.held_output.getvalue(), "")
    
    def test_number(self):
        guessed_letter = "1"
        result = validation(guessed_letter)
        self.assertTrue(result)
        self.assertEqual(self.held_output.getvalue(), "Please enter a single alphabetic character.\n")

    def test_multiple_letter(self):
        guessed_letter = "aa"
        result = validation(guessed_letter)
        self.assertTrue(result)
        self.assertEqual(self.held_output.getvalue(), "Please enter a single alphabetic character.\n")
    
    def test_empty_input(self):
        guessed_letter = " "
        result = validation(guessed_letter)
        self.assertTrue(result)
        self.assertEqual(self.held_output.getvalue(), "Please enter a single alphabetic character.\n")



class TestPreviousChoiceFunction(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        
    def tearDown(self):
         sys.stdout = sys.__stdout__ 

    def test_new_guessed_letter(self):
        guessed_letter ='a'
        guessed_letter_list = []
        expected_guessed_letter_list = ['a',]
        guessed_letter_list_output = previous_choice(guessed_letter,guessed_letter_list)
        self.assertEqual(expected_guessed_letter_list,guessed_letter_list)


    def test_guessed_letter_already_present(self):
        guessed_letter ='a'
        guessed_letter_list = ['a']
        guessed_letter_list_output = previous_choice(guessed_letter,guessed_letter_list)
        self.assertEqual(self.held_output.getvalue(), "You made this choice earlier.\n")


class TestChanceLeftFunction(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        self.word ="hangman"
    def tearDown(self):
         sys.stdout = sys.__stdout__ 


    def test_redusing_chance(self):
        guessed_letter ='p'
        guessed_letter_list = []
        chance = 7
        chance_output= chance_left(guessed_letter,guessed_letter_list,self.word,chance)
        expected_chance_left=6
        self.assertEqual(expected_chance_left,chance_output)
        self.assertEqual(self.held_output.getvalue(), "|_______\n|  |\n|\n|\n|\n|\n|_\nchances left 6\n")

    def test_not_redusing_chance_letterInWord(self):
        guessed_letter ='a'
        guessed_letter_list = []
        chance = 7
        chance_output= chance_left(guessed_letter,guessed_letter_list,self.word,chance)
        expected_chance_left=7
        self.assertEqual(expected_chance_left,chance_output)

    def test_not_redusing_chance_letterInList(self):
        guessed_letter ='p'
        guessed_letter_list = ['p','q']
        chance = 6
        chance_output= chance_left(guessed_letter,guessed_letter_list,self.word,chance)
        expected_chance_left=6
        self.assertEqual(expected_chance_left,chance_output)
    
        
    

class TestUnmaskingwordFunction(unittest.TestCase):
    def setUp(self):
        self.word = "hangman"
        
    def test_single_appearance_of_letter(self):
        guessed_letter='h'   
        masked_word = '-------'
        unmasked_word=unmasking_word(guessed_letter,self.word,masked_word)
        expected_unmasked_word ='h------'
        self.assertEqual(expected_unmasked_word,unmasked_word)

    def test_multiple_appearance_of_letter(self):
        guessed_letter='a'   
        masked_word = '-------'
        unmasked_word=unmasking_word(guessed_letter,self.word,masked_word)
        expected_unmasked_word ='-a---a-'
        self.assertEqual(expected_unmasked_word,unmasked_word)

    def test_no_appearance_of_letter(self):
        guessed_letter='q'   
        masked_word = '-------'
        unmasked_word=unmasking_word(guessed_letter,self.word,masked_word)
        expected_unmasked_word ='-------'
        self.assertEqual(expected_unmasked_word,unmasked_word)

    def test_already_unmasked_letter(self):
        guessed_letter='h'   
        masked_word = 'h------'
        unmasked_word=unmasking_word(guessed_letter,self.word,masked_word)
        expected_unmasked_word ='h------'
        self.assertEqual(expected_unmasked_word,unmasked_word)




class TestResult(unittest.TestCase):

    def setUp(self):
        
        self.mock_input = MagicMock(side_effect=['w', 'o', 'r', 'd'])  
        self.mock_output = StringIO()
        sys.stdout = self.mock_output  

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.open', unittest.mock.mock_open(read_data='word\n'))  
    def test_result_correct_guess(self):
        with patch('builtins.input', self.mock_input):
            with self.assertRaises(SystemExit):  
                result()
            output = self.mock_output.getvalue()
            self.assertIn("Congratulations", output)



if __name__ == '__main__':
    unittest.main()