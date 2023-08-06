import unittest
from tokenquery.nlp.tokenizer import Tokenizer
from tokenquery.nlp.pos_tagger import POSTagger
from tokenquery.tokenquery import TokenQuery


class TestTokenQueryClass(unittest.TestCase):

    def show_results(self, result):
        for group in result:
            print ('==='*3)
            for chunk_name in group:
                print ('---' + chunk_name + '---')
                chunk = group[chunk_name]
                for token in chunk:
                    print (token.get_token_id())
                    print (token.get_text())

    def assert_result(self, result, desired_result):
        self.assertEqual(len(result), len(desired_result))
        for group, desired_group in zip(result, desired_result):
            for chunk_name in group:
                self.assertIn(chunk_name, desired_group)
                chunk = group[chunk_name]
                desired_chunk = desired_group[chunk_name]
                for token, desired_token in zip(chunk, desired_chunk):
                    self.assertEqual(token.get_token_id(), desired_token.get_token_id())

    def test_regex_match(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist.')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')

        test_cases = []
        desired_results = []
        test_cases += ['[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] [/artist|painter/]']
        desired_results.append([{'chunk 1': input_tokens[:4]},
                                {'chunk 1': input_tokens[5:10]},
                                {'chunk 1': input_tokens[6:10]}]
                               )

        # desired_results
        test_cases += ['([ner:"NUMBER"]+) [/km|kilometers?/]']
        desired_results.append([])

        test_cases += ['[ner:"PERSON"]? [pos:/V.*/]']
        desired_results.append([{'chunk 1': input_tokens[:2]},
                                {'chunk 1': input_tokens[1:2]},
                                {'chunk 1': input_tokens[6:8]},
                                {'chunk 1': input_tokens[7:8]}]
                               )

        for test_case, desired_result in zip(test_cases, desired_results):
            # print('<>'*30)
            # print (test_case)
            # print('<>'*20)
            # unit = TokenQuery(test_case, verbose=True)
            unit = TokenQuery(test_case)
            result = unit.match_tokens(input_tokens)
            # self.show_results(result)
            self.assert_result(result, desired_result)

    def test_repetition(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist. Sir Isaac Newton ...')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')
        input_tokens[11].add_a_label('ner', 'PERSON')
        input_tokens[12].add_a_label('ner', 'PERSON')
        input_tokens[13].add_a_label('ner', 'PERSON')

        test_cases = []
        desired_results = []
        test_cases += ['[ner:str_eq(PERSON)]*']
        desired_results.append([{'chunk 1': input_tokens[:1]},  # David
                                {'chunk 1': input_tokens[5:7]},  # Ramtin Muller
                                {'chunk 1': input_tokens[6:7]},  # Muller
                                {'chunk 1': input_tokens[11:14]},  # Sir Isaac Newton
                                {'chunk 1': input_tokens[12:14]},  # Isaac Newton
                                {'chunk 1': input_tokens[13:14]}]  # Newton
                               )

        test_cases += ['[ner:str_eq(PERSON)]?']
        desired_results.append([{'chunk 1': input_tokens[:1]},  # David
                                {'chunk 1': input_tokens[5:6]},  # Ramtin
                                {'chunk 1': input_tokens[6:7]},  # Muller
                                {'chunk 1': input_tokens[11:12]},  # Sir
                                {'chunk 1': input_tokens[12:13]},  # Isaac
                                {'chunk 1': input_tokens[13:14]}]  # Newton
                               )

        test_cases += ['[ner:str_eq(PERSON)]+']
        desired_results.append([{'chunk 1': input_tokens[:1]},  # David

                                {'chunk 1': input_tokens[5:7]},  # Ramtin Muller
                                {'chunk 1': input_tokens[6:7]},  # Muller

                                {'chunk 1': input_tokens[11:14]},  # Sir Isaac Newton
                                {'chunk 1': input_tokens[12:14]},  # Isaac Newton
                                {'chunk 1': input_tokens[13:14]}]  # Newton
                               )

        test_cases += ['[ner:str_eq(PERSON)]{2}']
        desired_results.append([{'chunk 1': input_tokens[5:7]},  # Ramtin Muller
                                {'chunk 1': input_tokens[11:13]},  # Sir Isaac
                                {'chunk 1': input_tokens[12:14]}]  # Isaac Newton
                               )

        test_cases += ['[ner:str_eq(PERSON)]{1,2}']  # ? where is Ramtin
        desired_results.append([{'chunk 1': input_tokens[:1]},  # David
                                {'chunk 1': input_tokens[5:7]},  # Ramtin Muller
                                {'chunk 1': input_tokens[6:7]},  # Muller
                                {'chunk 1': input_tokens[11:13]},  # Sir Isaac
                                {'chunk 1': input_tokens[12:14]},  # Isaac Newton
                                {'chunk 1': input_tokens[13:14]}]  # Newton
                               )

        # test range repetition
        # test_cases += ['[ner:str_eq(PERSON)]{1,3} [pos:str_eq(VBZ)]']
        # test_cases += ['[ner:str_eq(PERSON)]{2,3} [pos:str_eq(VBZ)]']
        # test_cases += ['[ner:str_eq(PERSON)]{3,6} [pos:str_eq(VBZ)]']
        # test_cases += ['[ner:str_eq(PERSON)]{1,2} [pos:str_eq(VBZ)]']
        # test_cases += ['[ner:str_eq(PERSON)]{1,6} [pos:str_eq(VBZ)]']

        for test_case, desired_result in zip(test_cases, desired_results):
            # print('<>'*30)
            # print (test_case)
            # print('<>'*20)
            # unit = TokenQuery(test_case, verbose=True)
            unit = TokenQuery(test_case)
            result = unit.match_tokens(input_tokens)
            # self.show_results(result)
            self.assert_result(result, desired_result)


    def test_logics(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist. Sir Isaac Newton ...')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')
        input_tokens[11].add_a_label('ner', 'PERSON')
        input_tokens[12].add_a_label('ner', 'PERSON')
        input_tokens[13].add_a_label('ner', 'PERSON')

        test_cases = []
        desired_results = []

        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&"a"] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&pos:"DT"] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&pos:str_eq(DT)] [str_eq(painter)]']


    def test_capturing(self):
        test_cases = []
        desired_results = []
        test_cases += ['[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+ [pos:"VBZ"]) [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+ [pos:"VBZ"] )[/an?/] ["painter"]']
        test_cases += ['[ner:"PERSON"]+ ([pos:"VBZ"] [/an?/] ["painter"])']

    def test_by_pos_tag(self):
        tokenizer = Tokenizer('PTBTokenizer')
        pos_tagger = POSTagger()
        test_text = """
                    I am a painter, you're also a painter!
                    """

        tokens = tokenizer.tokenize(test_text)
        tokens = pos_tagger.tag(tokens)

        # test_tokenregex_1 = '[/.*/] [pos:"VBP"] [/an?/] ["painter"]'
        # unit = TokenRegex(test_tokenregex_1)
        # unit.machine.print_state_machine()

        # print unit.match_tokens(tokens)

        # test_tokenregex_2 = '([/.*/]) [pos:"VBP"] [/an?/] ["painter"]'
        # unit = TokenRegex(test_tokenregex_1)
        # unit.machine.print_state_machine()

        # print unit.match_tokens(tokens)

        # self.assertListEqual(expected_tags, [token.get_a_label('POS') for token in tokens])


if __name__ == "__main__":
    unittest.main()
