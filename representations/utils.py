import re
import unicodedata
import logging
from .patterns import patterns

logger = logging.getLogger(__name__)


def preprocess_paragraph(paragraph, capitalize=True):
    paragraph = unicodedata.normalize("NFKD", paragraph)
    paragraph = normalize(paragraph)

    if capitalize:
        for x in re.finditer(r"[A-Z]+(?=[\.\s$,])", paragraph):
            """
            Capitalize word
            """
            span = x.span()
            substr = paragraph[span[0]:span[1]]
            paragraph = paragraph[:span[0]] + substr.capitalize() + paragraph[span[1]:]

    return paragraph.strip()

def normalize(line):
    """
    Normalize a line of text

    Arguments:
    ----------

    line: str
        Line to normalize
    """
    line = line.replace("\t", " ")
    line = line.replace("  ", " ")
    line = re.sub("[“”]", "\"", line)
    return line

def preprocess_text(paragraphs, capitalize=True):
    """
    Preprocess text

    Returns paragraphs in a generator

    Arguments:
    ----------

    paragraphs: iterable of strings
        Paragraphs to preprocess
    capitalize: bool
        Whether to capitalize the first letter of each word (that is in uppercase)
    """
    previous_number = True
    processed_paragraphs = []
    end_of_sentence_markers = [ ".", "!", "?" ]
    for line in paragraphs:
        line = preprocess_paragraph(line, capitalize=capitalize)
        if not line:
            continue

        line = normalize(line)
        if re.match(r"^[-\.\s]*\d{1,3}[-\.\s]*$", line) or re.match(r"^[-_]+$", line) or ("Page" in line and len(line) < 10):
            """
            Page number or separator
            """
            previous_number = True
            continue
        elif previous_number and processed_paragraphs and not processed_paragraphs[-1][-1] in end_of_sentence_markers:
            # append to previous paragraph
            processed_paragraphs[-1] = processed_paragraphs[-1] +" "+ line
            line = processed_paragraphs[-1]
            previous_number = False
        else:
            processed_paragraphs.append(line)
            previous_number = False

    return processed_paragraphs

def split_sentences(text):
    """
    Split text in sentences
    """
    sentences = []
    for sentence in text.split("."):
        sentence = sentence.strip()
        if sentence == "":
            continue
        sentences.append(sentence)
    return sentences


def get_reference_string(title):
    """
    Returns reference string
    """
    for pattern in patterns:
        match = re.match(pattern[0], title.lower())
        if match:
            # Get the group index
            return match.groups()[pattern[2]]
    raise ValueError(f"No reference found in {title}")

def get_path(title):
    """
    Returns the path of a title
    """
    ref_string = get_reference_string(title)
    splitted = re.split(r'[\s\.:()]', ref_string)
    splitted = [s for s in splitted if s]
    return splitted

def references_match(ref1, ref2):
    """
    Returns True if the references match
    """
    roman_to_int = {
        "i": 1,
        "ii": 2,
        "iii": 3,
        "iv": 4,
        "v": 5,
        "vi": 6,
        "vii": 7,
        "viii": 8,
        "ix": 9,
        "x": 10,
    }

    ref1 = ref1.lower()
    ref2 = ref2.lower()

    if ref1 == ref2:
        return True
    elif ref1 in roman_to_int:
        return str(roman_to_int[ref1]) == ref2
    elif ref2 in roman_to_int:
        return str(roman_to_int[ref2]) == ref1
    return False
