import os
import pathlib


def directory_search(directory: str, *,
                     recursive=True,
                     max_depth=None,
                     ignore_hidden=None,
                     include=None,
                     exclude=None,

                     dir_include=None,
                     dir_exclude=None,
                     ) -> tuple:
    directory = os.path.expanduser(directory)

    directory_depth = 0
    for directory, subdir, files in os.walk(directory):
        if include or exclude:
            for directory, file in file_include_exclude(files,
                                                        directory=directory,
                                                        include=include,
                                                        exclude=exclude
                                                        ):
                yield os.path.join(directory, file)
        else:
            for file in files:
                yield os.path.join(directory, file)

        # Break after 1st iteration to prevent recursiveness
        if recursive is False:
            break
        elif max_depth is int and max_depth > 0:
            directory_depth += 1
            if directory_depth == max_depth:
                break


def file_include_exclude(files, *, directory, include, exclude):
    if include:
        included_filenames = {file for glob_match in include
                              for file in files
                              if pathlib.PurePath(file).match(glob_match)}
    else:
        included_filenames = set()
    if exclude:
        excluded_filenames = {file for glob_match in exclude
                              for file in files
                              if pathlib.PurePath(file).match(glob_match)}
    else:
        excluded_filenames = set()
    for file in files:
        if file in included_filenames:
            yield (directory, file)
        elif file not in excluded_filenames and len(excluded_filenames) > 0:
            yield (directory, file)


if __name__ == '__main__':
    for directory, files in directory_search("tests/directory_search"):
        print(directory, files)
