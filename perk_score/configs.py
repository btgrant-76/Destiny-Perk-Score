config_file_identifier = '_perk_score_config.txt'  # TODO make this private?


def config_files(file_names):
    return list(filter(lambda n: n.endswith(config_file_identifier), file_names))


# class Config:
#     pass

