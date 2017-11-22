


""""vundle"""""""""""""""""""""""""""""""""""""
set nocompatible              
filetype off                  
set rtp+=$VIM/vimfiles/bundle/Vundle.vim/
call vundle#begin('$VIM/vimfiles/bundle/')	"插件安装目录

"""""Vundle安装插件有多种形式，
" 1、Github上的插件
" 格式为 Plugin '用户名/插件仓库名'
"Plugin 'tpope/vim-fugitive'
" 2、来自 http://vim-scripts.org/vim/scripts.html 的插件
" Plugin '插件名称' 实际上是 Plugin 'vim-scripts/插件仓库名' 只是此处的用户名可以省略
"Plugin 'L9'
" 3、由Git支持但不再github上的插件仓库 Plugin 'git clone 后面的地址'
"Plugin 'git://git.wincent.com/command-t.git'
" 4、本地的Git仓库(例如自己的插件) Plugin 'file:///+本地插件仓库绝对路径'
"Plugin 'file:///home/gmarik/path/to/plugin'
" 5、插件在仓库的子目录中.
" 正确指定路径用以设置runtimepath. 以下范例插件在sparkup/vim目录下
"Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" 6、避免插件名冲突,例如L9已存在,则可以指定
"Plugin 'user/L9', {'name': 'newL9'}

Plugin 'VundleVim/Vundle.vim'

Plugin 'python-mode/python-mode'
"Plugin 'scrooloose/nerdtree'
"Plugin 'kien/ctrlp.vim'
Plugin 'altercation/vim-colors-solarized'
"Plugin 'vim-scripts/taglist.vim'
"Plugin 'majutsushi/tagbar'
"Plugin 'vim-scripts/TaskList.vim'
"Plugin 'Valloric/YouCompleteMe'
"Plugin 'davidhalter/jedi-vim'
"Plugin 'w0rp/ale'
call vundle#end()            " required
filetype plugin indent on    " required

""""""""""""""""END""""""""""""""""

"""""""""others""""""""""""""""""""""""""""""
""""language"""""""""""""""""""""""""""""""""""
let &termencoding=&encoding
set fileencodings=utf-8,gbk

"""" set solarized"""""""""""""""""""""""""""""
syntax enable
set background=dark
colorscheme solarized
"colorscheme molokai
"colorscheme phd


"显示行号
set nu

"启动时隐去援助提示
set shortmess=atI

"语法高亮
syntax on

"使用vim的键盘模式
"set nocompatible

"不需要备份
set nobackup

"没有保存或文件只读时弹出确认
set confirm

"鼠标可用
set mouse=a

"tab缩进
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab

"文件自动检测外部更改
set autoread

"c文件自动缩进
set cindent

"自动对齐
set autoindent

"智能缩进
set smartindent

"高亮查找匹配
set hlsearch

"背景色
set background=dark

"显示匹配
set showmatch

"显示标尺，就是在右下角显示光标位置
set ruler

"去除vi的一致性
set nocompatible

"允许折叠
set foldenable
"""""""""""""""""设置折叠"""""""""""""""""""""
"
"根据语法折叠
set fdm=syntax

"手动折叠
"set fdm=manual

"设置键盘映射，通过空格设置折叠
nnoremap <space> @=((foldclosed(line('.')<0)?'zc':'zo'))<CR>
""""""""""""""""""""""""""""""""""""""""""""""
"不要闪烁
set novisualbell

"启动显示状态行
set laststatus=2

"浅色显示当前行
autocmd InsertLeave * se nocul

"用浅色高亮当前行
autocmd InsertEnter * se cul

"显示输入的命令
set showcmd

"被分割窗口之间显示空白
set fillchars=vert:/

set fillchars=stl:/

set fillchars=stlnc:/

"Toggle Menu and Toolbar
set guioptions-=m  "remove menu bar  
set guioptions-=T  "remove toolbar 

"""""python 支持
"set filetype=python
"au BufNewFile,BufRead *.py,*.pyw setf python
map <F5> :w<cr>:!python %<cr> 

""""NERD_tree
"autocmd vimenter * NERDTree
map <F2> :NERDTreeToggle<CR>
"nerdtree end
