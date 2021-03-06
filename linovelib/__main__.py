if __name__ == '__main__':
    import fire
    from linovelib_all import *
else:
    import fire
    from .linovelib_all import *

class Lensi(object):
    def __init__(self) -> None:
        pass
    def download(self,id,type_book="txt",begin_chapter=0,end_chapter=0,path=os.getcwd(),wait_time=0.5,split_char='\n',enable_pic_download=True):
        if type(id) == int:
            id = str(id)
        else:
            if id.count('/') == 5 and id.find('catalog') == 0:
                    get_chapter_all_txt(id,wait_time,split_char,path)
            else:
                id = change_to_id(id)
        linovelib_download(id,wait_time,split_char,path,type_book,enable_pic_download,begin_chapter,end_chapter)
    def search(self,keyword,num=5):
        linovelib_search(keyword,num)
    def show(self,id):
        id = change_to_id(id)
        linovelib_show(id)
    def info(self,id):
        id = change_to_id(id)
        linovelib_info(id)
    def rec(self,type='monthvisit',page=1):
        type_list = ["monthvisit","allvisit","allvote","monthvote","allflower","monthflower","lastupdate","poastdate","signtime","words","goodnum","newhot"]
        if type == "random" or type == "rand" or type == "r":
            type = type_list[random.randint(0,len(type_list)-1)]
        if type not in type_list:
            print("type error")
            return
        else:
            linovelib_rec(type,page)
    def pic(self,id,begin_chapter=0,end_chapter=0,wait_time=1,path=os.getcwd()):
        id = change_to_id(id)
        linovelib_pic(id,wait_time,path,begin_chapter,end_chapter)

def main():
    fire.Fire(Lensi)