from bs4 import BeautifulSoup
import re
import openai
from typing import Union, List
from config import config_data

openai.api_key = config_data['OPEN_AI_KEY']


class PostText:
    def __init__(self, text: str = None):
        self.text: str = text

    def remove_patterns(self, pattern_list: Union[List[str], str]):
        """
        Removes patterns from the post
        :param pattern_list: can be a list of patterns or a string in the format 'pattern1,pattern2'
        :return: edited text
        """
        if not self.text:
            return self.text

        # Create a regular expression pattern for matching any of the phrases in the list
        regex_pattern = r'\b(?:' + '|'.join(pattern_list) + r')\b'
        # Use re.sub() to replace all occurrences of the patterns with an empty string
        self.text = re.sub(regex_pattern, '', self.text)

        return self.text

    def remove_empty_tags(self):
        if not self.text:
            return None

        # Parse the input text using BeautifulSoup
        soup = BeautifulSoup(self.text, 'html.parser')

        for tag in soup.find_all():
            if len(tag.text.replace(" ", "")) == 0:
                tag.extract()

        # Get the cleaned HTML without empty tags
        self.text = str(soup)
        return self.text

    def process_first_paragraph(self, st_char: str = '<b>◌', end_char: str = '◌</b>'):
        """
        Add some character at the beginning and ending of the first paragraph
        :param st_char: The start character to add, default '<b>◌'
        :param end_char: The end character to add, default '◌</b>'
        :return: edited text
        """
        if not self.text:
            return None

        # Find the first paragraph using a regular expression (search until the first empty line or \n\n)
        first_paragraph_match = re.search(r'(.+?)(\n|$)', self.text, re.DOTALL)

        if first_paragraph_match:
            # Extract the first paragraph and remove the trailing period, if present
            first_paragraph = first_paragraph_match.group(1).strip()
            if first_paragraph.endswith('.'):
                first_paragraph = first_paragraph[:-1]

            # Add char at the beginning and end of the first paragraph
            self.text = self.text.replace(first_paragraph_match.group(1), st_char + first_paragraph + end_char, 1)
            return self.text
        else:
            # If the first paragraph is not found, return the original text without changes
            return self.text

    def add_new_paragraph(self, new_paragraph: str):
        if not self.text:
            self.text = ""

        new_paragraph = '\n\n' + new_paragraph.strip()

        # Remove any existing blank lines at the end of the text and add new_paragraph
        print(self.text.rstrip())
        self.text = self.text.rstrip() + new_paragraph

        return self.text

    async def translate(self, language: str = 'English'):
        """
        Translate the text using OpenAI API. RETURNS NEW PostText OBJECT
        :param language: Language to translate to. Better to write it on the language you want to translate to.
         For example, 'English' or 'Українську' or 'Русский'
        :return: new PostText object with translated text
        """
        if len(language) < 2:
            raise Exception("Language must be at least 2 characters long")
        elif len(language) > 20:
            raise Exception("Language must be less than 20 characters long")

        if not self.text:
            return type(self)()

        response = await openai.ChatCompletion.acreate(
            model=config_data['GPT_MODEL'],
            messages=[{"role": "system", "content": config_data['GPT_START_MSG']},
                      {"role": "user", "content": f"""
                      Translate this news on {language}, use Telegram HTML formatting:
                      
                      {self.text}"""}],

        )
        translated_text = response.choices[0].message.content

        return type(self)(text=translated_text)
