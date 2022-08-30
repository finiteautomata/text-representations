

patterns = [
    # (pattern, top_level, title_group_index)
    # pattern is the proper regex
    # top_level is a boolean indicating if this pattern is a top level node
    # title_group_index is the index of the group in the regex that contains the title reference
    (r"^(exhibit (\S*))", True, 1),
    (r"^(schedules? (\S*))", True, 1),
    (r"^(article (\S*))", True, 1),
    (r"^(section (\S*))", True, 1),
    (r"^(\d{1,2}\.(\d{1,2}\.?)*)", True, 0),
    #(r"^(\d{1,2}\.)", True, 0),
    # Numbers
    (r"^(\(\d{1,4}\))", False, 0),
    # Mando este para arriba y le pongo True...
    #(r"^(\d{1,2}\.(\d{1,2}\.?)*)", False, 0),
    # Roman numbers
    (r"^(\([ivx]{1,4}\))", False, 0),
    (r"^([ivx]{1,4}\.)", False, 0),
    # Letters (A), A.
    (r"^(\([a-h]{1,4}\))", False, 0),
    (r"^([\da-z]{1,2}\.([\da-z]{1,2}\.?)*)", False, 0),
]
