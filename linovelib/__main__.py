if __name__ == '__main__':
    import fire
    from linovelib_download import *
else:
    import fire
    from .linovelib_download import *

class Lensi(object):
    def __init__(self) -> None:
        pass
    def download(self,id,wait_time=0.5,split_char='\n'):
        if type(id) == int:
            id = str(id)
        if id.find('https://www.linovelib.com/novel/') != -1:
            if id.find('catalog') != -1:
                id = id.split('/')[-2]
            elif id.count('/') == 5:
                get_chapter_all_txt(id,wait_time,split_char)
            elif id.count('/') == 4:
                id = id.split('/')[-1].strip(".html")
        # print(id)
        linovelib_download(id,wait_time,split_char)

def main():
    fire.Fire(Lensi)