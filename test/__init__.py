def get_local_dir(file):
    from pathlib import Path
    return Path(file).parent.as_posix()