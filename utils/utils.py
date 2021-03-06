import pytesseract
import glob
import re


def extract(path='./data/*.jpg'):
    pages = glob.glob(path)
    pages.sort()

    text = ''

    for page in pages:
        print('extracting: {}'.format(page))
        text += pytesseract.image_to_string(page)

    lines = text.split('\n')
    return lines


def build_chapters(lines):
    chapters = {}
    cur_chapter = 'Intro'
    for line in lines:
        is_chapter = re.match(r"^(Chapter [0-9]+:)", line)

        if is_chapter:
            cur_chapter = line
        elif cur_chapter in chapters.keys():
            content = '{}\n'.format(line)
            chapters[cur_chapter] += content
        else:
            content = '{}\n'.format(line)
            chapters[cur_chapter] = content

    return chapters


def get_chapter_file(chapter):
    chapter_spinal_case = convert_chapter_to_spinal(chapter)
    return '{}.html'.format(chapter_spinal_case)


def build_html_files(chapters, dest='./html/'):
    chapter_keys = list(chapters.keys())
    for index, chapter in enumerate(chapter_keys):
        chapter_file = get_chapter_file(chapter)
        file_name = '{0}{1}'.format(dest, chapter_file)
        html_file = open(file_name, 'w')

        prev_link = ''
        next_link = ''
        if index > 0:
            prev_chapter = chapter_keys[index - 1]
            prev_chapter_file = get_chapter_file(prev_chapter)
            prev_link = '<p><a href="{}">Previous</a></p>'.format(
                prev_chapter_file)

        if (index < len(chapters.keys()) - 1):
            next_chapter = chapter_keys[index + 1]
            next_chapter_file = get_chapter_file(next_chapter)
            next_link = '<p><a href="{}">Next</a></p>'.format(
                next_chapter_file)
        paragraph = chapters[chapter].replace('\n\n', '<br/><br/>')
        content = """<html>
<head>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div>
<h1>{0}</h1>
<p>{1}</p>{2}{3}</div></body>
</html>""".format(chapter, paragraph, prev_link, next_link)
        html_file.write(content)
        html_file.close()


def convert_chapter_to_spinal(chapter):
    name = re.sub(r"^(Chapter [0-9]+: )", '', chapter)
    if name == chapter:
        raise InvalidChapterException
    name = name.lower()
    return name.replace(' ', '-')


class InvalidChapterException(Exception):
    """Chapter name is invalid"""
    pass
