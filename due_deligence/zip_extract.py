import zipfile


def zip_extract(filename):
    """ファイル名を指定して zip ファイルをカレントディレクトリに展開する
    """
    target_directory = '.'
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target_directory)
