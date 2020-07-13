import os
import argparse
from glob import glob

from config import Config
from lsi_itemloader import LsiItemLoader
from lsi_content import LsiContentTransforms
from lsi_visual import LsiVisualTransforms

class Lsi():
    def __init__(
            self,
            dir,
            show_all=False,
            show_only_directories=False,
            show_only_files=False,
            show_file_num=False,
            limit_file_num=50,
            search_word=''
            ):
        """
        Constructor
        Set all optional command line arguments here.
        
        Parameters
        ----------
        dir : String
            Directory Path
        show_all : Boolean (Optional)
            (command) -a, --all
            True -> Show all files and directories.
        show_only_directories : Boolean (Optional)
            (command) -d, --only-directories
            True -> Do not show files.
        show_only_files : Boolean (Optional)
            (command) -f, --only-files
            True -> Do not show directories.
        show_file_num : Boolean (Optional)
            (command) -l, --show-file-num
            True -> Show number of children files.
        limit_file_num : Int (Optional)
            (command) -n, --limit-file-num
            Set confirm condition (num of children files).
        """
        
        # Set CommandLine Arguments
        self.dir = dir
        self.show_all = show_all
        self.show_only_files = show_only_files
        self.show_only_directories = show_only_directories
        self.limit_file_num = limit_file_num
        self.show_file_num = show_file_num
        
        # Set Lsi Modules
        self.config = Config()
        self.item_loader = LsiItemLoader()
        self.content_transforms = LsiContentTransforms(
                search_word=search_word
                )
        self.visual_transforms = LsiVisualTransforms()

    def print_items(self, children, condition):
        """
        Repeat self._visual_tr_manager() along directories and files on this level.
        Then (or while), Print these.
        
        Parameters
        ----------
        children : List[children_d, children_f]
        condition : Dict

        Return
        ------
        status : Boolean
            0 == success
            1 == failed
        """
        children = children[0]+children[1]
        for item in children:
            s, output = self.visual_transforms.run(item, condition)
            print(output)
        status = 0
        return status

    def run(self):
        """
        Management all functions.
        """
        status, children = self.item_loader.get_items(
                self.dir, 
                show_all=self.show_all,
                show_only_directories=self.show_only_directories,
                show_only_files=self.show_only_files
                )

        condition = {
                'status': 0
                }
        status, children = self.content_transforms.run(
                children,
                condition
                )

        condition = {
                'status': 0
                }
        status = self.print_items(
                children,
                condition
                )
        
        
def main():
    # Parser setting
    parser = argparse.ArgumentParser(description="lsi ==lsImproved==")
    parser.add_argument('dir', type=str, nargs='?', default="./", metavar='DirectoryPath', help='directory where you want to look. (default: current directory)')
    parser.add_argument('-a','--all', action='store_true', help='show hidden files and directories. (default: Hidden)')
    parser.add_argument('-d','--only-directories', action='store_true', help='show only directories.')
    parser.add_argument('-f','--only-files', action='store_true', help='show only files.')
    parser.add_argument('-s','--search', default='', help='search word inside of file names and descriptions')
    parser.add_argument('-l','--show-file-num', action='store_true', help='show files num of directory')
    parser.add_argument('-n', '--limit-file-num', type=int, default=50, help='set threshold for opening directory by many files')
    args = parser.parse_args()

    # Get parser arguments
    dir = args.dir
    dir = dir+'/' if dir[-1] != '/' else dir
    show_all = args.all
    show_only_directories = args.only_directories
    show_only_files = args.only_files
    show_file_num = args.show_file_num
    limit_file_num = args.limit_file_num
    search_word = args.search

    lsi = Lsi(
            dir,
            show_all=show_all, 
            show_only_directories=show_only_directories, 
            show_only_files=show_only_files, 
            show_file_num=show_file_num,
            limit_file_num=limit_file_num,
            search_word=search_word
            )

    lsi.run()

if __name__ == '__main__':
    main()
