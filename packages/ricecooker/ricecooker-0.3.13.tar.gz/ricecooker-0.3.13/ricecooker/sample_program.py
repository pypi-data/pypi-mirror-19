from ricecooker.classes.nodes import Channel, Video, Audio, Document, Topic, Exercise, HTML5App, guess_content_kind
from ricecooker.classes.questions import PerseusQuestion, MultipleSelectQuestion, SingleSelectQuestion, FreeResponseQuestion, InputQuestion
from ricecooker.exceptions import UnknownContentKindError, UnknownQuestionTypeError, raise_for_invalid_channel
from le_utils.constants import content_kinds,file_formats, format_presets, licenses, exercises

SAMPLE_PERSEUS = '{"answerArea":{"chi2Table":false,"periodicTable":false,"tTable":false,"zTable":false,"calculator":false},' + \
'"hints":[{"widgets":{},"images":{"web+graphie:C:/users/jordan/contentcuration-dump/0a0c0f1a1a40226d8d227a07dd143f8c08a4b8a5": {}},"content":"Hint #1","replace":false},{"widgets":{},"images":{},"content":"Hint #2","replace":false}],' +\
'"question":{"widgets":{"radio 1":{"type":"radio","alignment":"default","graded":true,"static":false,' +\
'"options":{"deselectEnabled":false,"multipleSelect":false,"choices":[{"correct":true,"content":"Yes"},{"correct":false,"content":"No"}],' +\
'"displayCount":null,"hasNoneOfTheAbove":false,"randomize":false,"onePerLine":true},"version":{"minor":0,"major":1}}},"images":{"web+graphie:C:/users/jordan/contentcuration-dump/0a0c0f1a1a40226d8d227a07dd143f8c08a4b8a5": {}},' +\
'"content":"Do you like rice?\\\"\\n\\n![](web+graphie:C:/users/jordan/contentcuration-dump/0a0c0f1a1a40226d8d227a07dd143f8c08a4b8a5)\\n\\n[[\\u2603 radio 1]]"},"itemDataVersion":{"minor":1,"major":0}}'

SAMPLE_TREE = [
    {
        "title": "TEST COMPRESSION",
        "id": "6cafe7",
        "author": "Revision 3",
        "description": "Become a master rice cooker",
        "file": "C:/users/jordan/contentcuration-dump/high resolution.mp4",
        "license": licenses.CC_BY_NC_SA,
    },
    {
        "title": "Rice 101",
        "id": "abd115",
        "description": "Learn about how rice",
        "children": [
            {
                "title": "Rice Distribution",
                "id": "aaaa4d",
                "file": "https://ia801407.us.archive.org/21/items/ah_Rice/Rice.mp3",
                "description": "Get online updates regarding world's leading long grain rice distributors, broken rice distributors, rice suppliers, parboiled rice exporter on our online B2B marketplace TradeBanq.",
                "license": licenses.PUBLIC_DOMAIN,
                "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Rice_grains_(IRRI).jpg",
            },
            {
                "title": "Rice History",
                "id": "6ef99c",
                "description": "Discover the history of rice",
                "children": [
                    {
                        "title": "The History of Japanese Rice",
                        "id": "418799",
                        "author": "Sandra Lopez-Richter",
                        "file": "https://ia601301.us.archive.org/31/items/The_History_of_Japanese_Rice_Lopez-Richter/The_History_of_Japanese_Rice_Lopez-Richter.pdf",
                        "license": licenses.CC_BY,
                        "thumbnail" : "http://res.freestockphotos.biz/pictures/17/17321-a-bowl-of-rice-with-chopsticks-pv.jpg",
                    },
                ]
            },
        ]
    },
    {
        "title": "Rice Cookers",
        "id": "d98752",
        "description": "Start cooking rice today!",
        "children": [
            {
                "title": "Rice Chef",
                "id": "6cafe2",
                "author": "Revision 3",
                "description": "Become a master rice cooker",
                "file": "https://ia600209.us.archive.org/27/items/RiceChef/Rice Chef.mp4",
                "license": licenses.CC_BY_NC_SA,
                "thumbnail": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAmFQTFRF////wN/2I0FiNFFuAAAAxdvsN1RxV3KMnrPFFi9PAB1CVG+KXHaQI0NjttLrEjVchIF4AyNGZXB5V087UUw/EzBMpqWeb2thbmpgpqOceXVsERgfTWeADg8QCAEApKGZBAYIop+XCQkIhZ+2T2mEg5mtnK/AobPDkKO2YXqTAAAAJkBetMraZH2VprjIz9zm4enw7/T47fP3wc7ae5GnAAAAN1BsSmSApLfI1ODq2OHp5Orv8PL09vb38fb5wM/bbISbrL/PfZSpxNPgzdnj2+Pr5evw6+/z6e3w3ePp2OPsma2/ABM5Q197ABk4jKG1yNfjytfh1uDo3eXs4unv1t/nztrjqbzMTmmEXneRES1Ji6CzxtXixdPfztrk1N/n1+Dp1d/oz9vlxdPeq73NVG+KYnyUAAAddIuhwtPhvMzaxtTgytfiy9jjwtHewtHenbDCHT1fS2eCRV52qr7PvM3cucrYv87cv8/cvMzavc3bucvacoyl////ByE8WnKKscXWv9Hguszbu8zbvc7dtcnaiJqrcHZ4f4SHEh0nEitFTWZ+hJqumrDDm7HDj6W5dI2lYGJfmZeQl5SNAAAADRciAAATHjdSOVNsPlhyLklmKCYjW1lUlpOLlZKLFSAqWXSOBQAADA0NAAAAHh0bWlhSk5CIk5CIBAYJDRQbERcdDBAUBgkMAAAEDg4NAAAAHBsZWFZQkY6GAAAAAAAABQUEHBsZAAAAGxoYVlROko+GBAQDZ2RdAAAAGhkYcW9oAgICAAAAExMSDQwLjouDjYuDioiAiIV9hoN7VlRO////Z2DcYwAAAMR0Uk5TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACRKrJyrZlBQECaNXCsKaqypMGAUDcu7Gpn5mf03gDo8+4saiipKq3xRMBH83Eu7OsqbG61DkDMdbFvrizsbK3wNs9Ax/VysS/vLq/zNwfArDhxMfExMXE3pMCMe7byMjIzd33ZgYGQtnz6+zooeJXBQMFD1yHejZ1+l8FBgEELlOR+GgFCQ0SGxoBGFKg+m0BBwEMR6v+hAEDM6nRASWURVuYQQ4AAAABYktHRACIBR1IAAAACXBIWXMAAAjLAAAIywGEuOmJAAABCklEQVQY02NgUGZUUVVT19DUYtBmYmZhYdBh1dXTNzA0MjYxZTFjAwqwm1tYWlnb2NrZO3A4cgIFGJycXVzd3D08vbx9uHyBAn7+AYFBwSEhoWHhEdyRQIGo6JjYuPiExKTklFSeNKBAekZmVnZObk5efkEhbxFQgK+4pLSsvKKyqrqGoZZfgIVBsK6+obGpuaW1rV2oQ1hEgKFTtKu7p7evf8LEI5PEJotLMEyZyjJt+oyZsxhmzzk6V3KeFIO01vwFMrJyCxctXrL02DL55QwsClorVq5avWbtuvUbNh7fpMjAwsKyWWvLFJatStu279h5YhdIAAJ2s+zZu+/kfoQAy4HNLAcPHQYA5YtSi+k2/WkAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTMtMTAtMDRUMTk6Mzk6MjEtMDQ6MDAwU1uYAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEzLTEwLTA0VDE5OjM5OjIxLTA0OjAwQQ7jJAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=",
            },
            {
                "title": "Rice Exercise",
                "id": "6cafe3",
                "description": "Test how well you know your rice",
                "license": licenses.CC_BY_NC_SA,
                "mastery_model": exercises.M_OF_N,
                "thumbnail":"http://www.publicdomainpictures.net/pictures/110000/nahled/bowl-of-rice.jpg",
                "questions": [
                    {
                        "id": "eeeee",
                        "question": "Which rice is your favorite? ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAmFQTFRF////wN/2I0FiNFFuAAAAxdvsN1RxV3KMnrPFFi9PAB1CVG+KXHaQI0NjttLrEjVchIF4AyNGZXB5V087UUw/EzBMpqWeb2thbmpgpqOceXVsERgfTWeADg8QCAEApKGZBAYIop+XCQkIhZ+2T2mEg5mtnK/AobPDkKO2YXqTAAAAJkBetMraZH2VprjIz9zm4enw7/T47fP3wc7ae5GnAAAAN1BsSmSApLfI1ODq2OHp5Orv8PL09vb38fb5wM/bbISbrL/PfZSpxNPgzdnj2+Pr5evw6+/z6e3w3ePp2OPsma2/ABM5Q197ABk4jKG1yNfjytfh1uDo3eXs4unv1t/nztrjqbzMTmmEXneRES1Ji6CzxtXixdPfztrk1N/n1+Dp1d/oz9vlxdPeq73NVG+KYnyUAAAddIuhwtPhvMzaxtTgytfiy9jjwtHewtHenbDCHT1fS2eCRV52qr7PvM3cucrYv87cv8/cvMzavc3bucvacoyl////ByE8WnKKscXWv9Hguszbu8zbvc7dtcnaiJqrcHZ4f4SHEh0nEitFTWZ+hJqumrDDm7HDj6W5dI2lYGJfmZeQl5SNAAAADRciAAATHjdSOVNsPlhyLklmKCYjW1lUlpOLlZKLFSAqWXSOBQAADA0NAAAAHh0bWlhSk5CIk5CIBAYJDRQbERcdDBAUBgkMAAAEDg4NAAAAHBsZWFZQkY6GAAAAAAAABQUEHBsZAAAAGxoYVlROko+GBAQDZ2RdAAAAGhkYcW9oAgICAAAAExMSDQwLjouDjYuDioiAiIV9hoN7VlRO////Z2DcYwAAAMR0Uk5TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACRKrJyrZlBQECaNXCsKaqypMGAUDcu7Gpn5mf03gDo8+4saiipKq3xRMBH83Eu7OsqbG61DkDMdbFvrizsbK3wNs9Ax/VysS/vLq/zNwfArDhxMfExMXE3pMCMe7byMjIzd33ZgYGQtnz6+zooeJXBQMFD1yHejZ1+l8FBgEELlOR+GgFCQ0SGxoBGFKg+m0BBwEMR6v+hAEDM6nRASWURVuYQQ4AAAABYktHRACIBR1IAAAACXBIWXMAAAjLAAAIywGEuOmJAAABCklEQVQY02NgUGZUUVVT19DUYtBmYmZhYdBh1dXTNzA0MjYxZTFjAwqwm1tYWlnb2NrZO3A4cgIFGJycXVzd3D08vbx9uHyBAn7+AYFBwSEhoWHhEdyRQIGo6JjYuPiExKTklFSeNKBAekZmVnZObk5efkEhbxFQgK+4pLSsvKKyqrqGoZZfgIVBsK6+obGpuaW1rV2oQ1hEgKFTtKu7p7evf8LEI5PEJotLMEyZyjJt+oyZsxhmzzk6V3KeFIO01vwFMrJyCxctXrL02DL55QwsClorVq5avWbtuvUbNh7fpMjAwsKyWWvLFJatStu279h5YhdIAAJ2s+zZu+/kfoQAy4HNLAcPHQYA5YtSi+k2/WkAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTMtMTAtMDRUMTk6Mzk6MjEtMDQ6MDAwU1uYAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEzLTEwLTA0VDE5OjM5OjIxLTA0OjAwQQ7jJAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=)",
                        "type":exercises.MULTIPLE_SELECTION,
                        "correct_answers": ["White rice", "Brown rice", "Sushi rice"],
                        "all_answers": ["White rice", "Quinoa","Brown rice"],
                    },
                    {
                        "id": "bbbbb",
                        "question": "Which rice is the crunchiest?",
                        "type":exercises.SINGLE_SELECTION,
                        "correct_answer": "Rice Krispies \n![](https://upload.wikimedia.org/wikipedia/commons/c/cd/RKTsquares.jpg)",
                        "all_answers": ["White rice \n![](https://upload.wikimedia.org/wikipedia/commons/4/4b/Thai_jasmine_rice_uncooked.jpg)", "Brown rice \n![](https://c2.staticflickr.com/4/3159/2889140143_b99fd8dd4c_z.jpg?zz=1)", "Rice Krispies \n![](https://upload.wikimedia.org/wikipedia/commons/c/cd/RKTsquares.jpg)"],
                        "hints": "It's delicious",
                    },
                    {
                        "id": "ccccc",
                        "question": "Why a rice cooker?",
                        "type":exercises.FREE_RESPONSE,
                        "answers": [],
                        "images": None,
                    },
                    {
                        "id": "aaaaa",
                        "question": "How many minutes does it take to cook rice? ![](https://upload.wikimedia.org/wikipedia/commons/5/5e/Jeera-rice.JPG)",
                        "type":exercises.INPUT_QUESTION,
                        "answers": ["20", "25", "15"],
                        "hints": ["Takes roughly same amount of time to install kolibri on Windows machine", "Does this help?\n![](http://www.aroma-housewares.com/images/rice101/delay_timer_1.jpg)"],
                    },
                    {
                        "id": "ddddd",
                        "type":exercises.PERSEUS_QUESTION,
                        "item_data":SAMPLE_PERSEUS,
                    },
                ],
            },
            {
                "title": "Rice Exercise 2",
                "id": "6cafe4",
                "description": "Test how well you know your rice",
                "license": licenses.CC_BY_NC_SA,
                "mastery_model": exercises.M_OF_N,
                "thumbnail":"https://c1.staticflickr.com/5/4021/4302326650_b11f0f0aaf_b.jpg",
                "questions": [
                    {
                        "id": "11111",
                        "question": "<h3 id=\"rainbow\" style=\"font-weight:bold\">RICE COOKING!!!</h3><script type='text/javascript'><!-- setInterval(function() {$('#rainbow').css('color', '#'+((1<<24)*Math.random()|0).toString(16));}, 300); --></script>",
                        "type":exercises.SINGLE_SELECTION,
                        "all_answers": ["Answer"],
                        "correct_answer": "Answer",
                    },
                    {
                        "id": "121212",
                        "question": '<math> <mrow> <msup><mi> a </mi><mn>2</mn></msup> <mo> + </mo> <msup><mi> b </mi><mn>2</mn></msup> <mo> = </mo> <msup><mi> c </mi><mn>2</mn></msup> </mrow> </math>',
                        "type":exercises.SINGLE_SELECTION,
                        "all_answers": ["Answer"],
                        "correct_answer": "Answer",
                    },
                ],
            },
            {
                "title": "The Everyday Rice Cooker: Soups, Sides, Grains, Mains, and More",
                "id": "aaaa5d",
                "file": "https://ia601300.us.archive.org/13/items/RiceCookerery/DianePhillips-RiceCooker.mp3",
                "license": licenses.PUBLIC_DOMAIN,
                "author": "Diane Phillips",
            },
            {
                "title": "Rice Exercise 3",
                "id": "6cafe5",
                "description": "Test how well you know your rice",
                "license": licenses.CC_BY_NC_SA,
                "mastery_model": exercises.M_OF_N,
                "thumbnail":"https://upload.wikimedia.org/wikipedia/commons/b/b7/Rice_p1160004.jpg",
                "questions": [
                    {
                        "id": "ccccc",
                        "question": "<h1>Why? <img src='http://agrointel.ro/wp-content/uploads/2015/04/orezul-auriu.jpg' alt='alternative-text'></h1>",
                        "type":exercises.SINGLE_SELECTION,
                        "all_answers": ["Yes", "No", "Rice!"],
                        "correct_answer": "Rice!",
                    },
                ],
            },
        ]
    },
]

def construct_channel(**kwargs):

    channel = Channel(
        domain="learningequality.org",
        channel_id="testing-ricecooker-channel",
        title="Testing Ricecooker Channel",
        thumbnail="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Banaue_Philippines_Banaue-Rice-Terraces-01.jpg/640px-Banaue_Philippines_Banaue-Rice-Terraces-01.jpg",
    )
    _build_tree(channel, SAMPLE_TREE)
    raise_for_invalid_channel(channel)

    return channel


def _build_tree(node, sourcetree):

    for child_source_node in sourcetree:
        try:
            kind = guess_content_kind(child_source_node.get("file"), child_source_node.get("questions"))
        except UnknownContentKindError:
            continue

        if kind == content_kinds.TOPIC:
            child_node = Topic(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
            )
            node.add_child(child_node)

            source_tree_children = child_source_node.get("children", [])

            _build_tree(child_node, source_tree_children)

        elif kind == content_kinds.VIDEO:

            child_node = Video(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),

                # video-specific data
                preset=format_presets.VIDEO_HIGH_RES,
                transcode_to_lower_resolutions=True,
                derive_thumbnail=True,

                # audio and video shared data
                subtitle=child_source_node.get("subtitle"),
                thumbnail=child_source_node.get("thumbnail"),
            )
            node.add_child(child_node)

        elif kind == content_kinds.AUDIO:
            child_node = Audio(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),

                # audio and video shared data
                subtitle=child_source_node.get("subtitle"),
                thumbnail=child_source_node.get("thumbnail"),
            )
            node.add_child(child_node)

        elif kind == content_kinds.DOCUMENT:
            child_node = Document(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),
                thumbnail=child_source_node.get("thumbnail"),
            )
            node.add_child(child_node)

        elif kind == content_kinds.EXERCISE:
            child_node = Exercise(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                exercise_data={}, # Just set to default
                license=child_source_node.get("license"),
                thumbnail=child_source_node.get("thumbnail"),
            )
            for q in child_source_node.get("questions"):
                question = create_question(q)
                child_node.add_question(question)
            node.add_child(child_node)

        elif kind == content_kinds.HTML5:
            child_node = HTML5App(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),
                thumbnail=child_source_node.get("thumbnail"),
            )
            node.add_child(child_node)

        else:                   # unknown content file format
            continue

    return node

def create_question(raw_question):

    if raw_question["type"] == exercises.MULTIPLE_SELECTION:
        return MultipleSelectQuestion(
            id=raw_question["id"],
            question=raw_question["question"],
            correct_answers=raw_question["correct_answers"],
            all_answers=raw_question["all_answers"],
            hints=raw_question.get("hints"),
        )
    if raw_question["type"] == exercises.SINGLE_SELECTION:
        return SingleSelectQuestion(
            id=raw_question["id"],
            question=raw_question["question"],
            correct_answer=raw_question["correct_answer"],
            all_answers=raw_question["all_answers"],
            hints=raw_question.get("hints"),
        )
    if raw_question["type"] == exercises.INPUT_QUESTION:
        return InputQuestion(
            id=raw_question["id"],
            question=raw_question["question"],
            answers=raw_question["answers"],
            hints=raw_question.get("hints"),
        )
    if raw_question["type"] == exercises.FREE_RESPONSE:
        return FreeResponseQuestion(
            id=raw_question["id"],
            question=raw_question["question"],
            hints=raw_question.get("hints"),
        )
    if raw_question["type"] == exercises.PERSEUS_QUESTION:
        return PerseusQuestion(
            id=raw_question["id"],
            raw_data=raw_question["item_data"],
        )
    else:
        raise UnknownQuestionTypeError("Unrecognized question type '{0}': accepted types are {1}".format(raw_question["type"], [key for key, value in exercises.question_choices]))