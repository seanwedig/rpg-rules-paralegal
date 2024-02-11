import fitz
import re
from collections import namedtuple

DocChunk = namedtuple('DocChunk', ['chapter', 'section', 'subsection', 'subsubsection', 'starting_page', 'content'])

class SrdParser():
    CHAPTER = { 'font': 'GillSans-SemiBold', 'size': 25.920000076293945, 'color': 9647668 } # ('Races'): 'GillSans-SemiBold', size ~25.920000076293945, color 9647668
    SECTION = { 'font': 'GillSans-SemiBold', 'size': 18, 'color': 9647668 } # ('Dwarf'): 'GillSans-SemiBold', size 18, color 9647668
    SUBSECTION = { 'font': 'GillSans-SemiBold', 'size': 13.920000076293945, 'color': 9647668 } # ('Racial Traits'): 'GillSans-SemiBold', size ~13.920000076293945, color 9647668
    SUBSUBSECTION = { 'font': 'GillSans-SemiBold', 'size': 12, 'color': 9647668 } # ('Ability Score Increase'): 'GillSans-SemiBold', size 12, color 9647668

    # TODO: term & definition - e.g., Adventuring Gear with the bold, italic lead in to the paragraph
    # TODO: table header / capturing tables
    # TODO: sidebars like "Self-Sufficiency" on page 73E
    # TODO: handle two back-to-back sections, like "Using Ablility" followed by "Scores" on 76
    # TODO: monster headers for individual monster stat blocks

    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)


    def chunk_srd_pdf(self) -> list[DocChunk]:
        wayfinding = { 'chapter': 'Legal Information', 'section': None, 'subsection': None, 'subsubsection': None, 'starting_page': None}
        chunk_content = ""
        doc_chunks = []

        for i, page in enumerate(self.doc):
            page_num = i+1

            d = page.get_text('dict')
            blocks = d['blocks']
            for block in blocks:
                if "lines" in block.keys():
                    spans = block['lines']
                    for span in spans:
                        data = span['spans']
                        for lines in data:
                            found_heading = False
                            trimmed_text = self.__clean_text_lines(lines['text'].strip())
                            # clone last heading
                            last_heading = wayfinding.copy()

                            # each new heading resets the wayfinding for the lower levels
                            if self.__is_heading_block(lines, self.CHAPTER):
                                wayfinding['chapter'] = trimmed_text
                                wayfinding['section'] = None
                                wayfinding['subsection'] = None
                                wayfinding['subsubsection'] = None
                                found_heading = True

                            if self.__is_heading_block(lines, self.SECTION):
                                wayfinding['section'] = trimmed_text
                                wayfinding['subsection'] = None
                                wayfinding['subsubsection'] = None
                                found_heading = True

                            if self.__is_heading_block(lines, self.SUBSECTION):
                                wayfinding['subsection'] = trimmed_text
                                wayfinding['subsubsection'] = None
                                found_heading = True

                            if self.__is_heading_block(lines, self.SUBSUBSECTION):
                                wayfinding['subsubsection'] = trimmed_text
                                found_heading = True

                            if not found_heading:
                                chunk_content += trimmed_text + " "
                            else:
                                # end the content of the previous chunk, if there was any
                                if chunk_content != "":
                                    previous_chunk = DocChunk(last_heading['chapter'],
                                                              last_heading['section'],
                                                              last_heading['subsection'],
                                                              last_heading['subsubsection'],
                                                              wayfinding['starting_page'],
                                                              chunk_content)
                                    doc_chunks.append(previous_chunk)
                                chunk_content = ""
                                wayfinding['starting_page'] = page_num

        # finish the last chunk
        previous_chunk = DocChunk(wayfinding['chapter'],
                                  wayfinding['section'],
                                  wayfinding['subsection'],
                                  wayfinding['subsubsection'],
                                  wayfinding['starting_page'],
                                  chunk_content)
        doc_chunks.append(previous_chunk)
        
        return doc_chunks


    def __strip_boilerplate(self, text: str) -> str:
        text = text
        page_boilerplate = 'System\xa0Reference\xa0Document\xa05.1\xa0\n\xa0 \d+\xa0\n'
        text = re.sub(page_boilerplate, '', text)
        text = re.sub('System\s+Reference\s+Document\s+5.1\s+\d+\s+', '', text)
        
        error_note = 'If you note any errors in this document, please let us know by \nemailing askdnd@wizards.com. \n'
        if error_note in text:
            text = text.replace(error_note, '')
    
        return text


    def __clean_text_lines(self, text: str) -> str:
        text = text.replace('\t\r \xa0', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('\xa0', ' ')
        text = text.replace('-\xad‐‑', '-')
        text = self.__strip_boilerplate(text)
        return text


    def __is_heading_block(self, line, heading_traits) -> bool:
        if line['font'] == heading_traits['font'] and line['size'] == heading_traits['size'] and line['color'] == heading_traits['color']:
            return True
        return False
