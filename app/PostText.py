from bs4 import BeautifulSoup
import re
import openai
from typing import Union, List
from config import GPT_MODEL, GPT_START_MSG, OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


class PostText:
    def __init__(self, text: str = None):
        self.text: str = text or ''

    def remove_patterns(self, pattern_list: Union[List[str], str]):
        """
        Removes patterns from the post
        :param pattern_list: can be a list of patterns or a string in the format 'pattern1,pattern2,..'
        :return: edited text
        """
        if len(self.text) < 1:
            return self.text

        # Create a regular expression pattern for matching any of the phrases in the list
        regex_pattern = r'\b(?:' + '|'.join(pattern_list) + r')\b'
        # Use re.sub() to replace all occurrences of the patterns with an empty string
        self.text = re.sub(regex_pattern, '', self.text)

        return self.text

    def remove_empty_tags(self):
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
        new_paragraph = '\n\n' + new_paragraph.strip()

        # Remove any existing blank lines at the end of the text and add new_paragraph
        print(self.text.rstrip())
        self.text = self.text.rstrip() + new_paragraph

        return self.text

    async def translate_on_ru(self):
        if len(self.text) < 1:
            return self.text

        response = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=[{"role": "system", "content": GPT_START_MSG},
                      {"role": "user", "content": f"""
                      Переведи новость на русский. Используй Telegram HTML formatting:
                      
                      {self.text}"""}],

        )
        self.text = response.choices[0].message.content

        return self.text

    async def translate_on_en(self):
        if len(self.text) < 1:
            return self.text

        response = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=[{"role": "system", "content": GPT_START_MSG},
                      {"role": "user", "content": f"""
                      Translate the post on English. Use telegram HTML formatting:
                      
                      {self.text}"""}],
        )
        self.text = response.choices[0].message.content

        return self.text
