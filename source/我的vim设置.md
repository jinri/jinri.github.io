---
title: 我的vim配置
date: 2017-10-29 22:00:10
tags: 
---
```
set nocompatible         "关闭 vi 兼容模式                                                                                
syntax on                "自动语法高亮      
set number               "显示行号                                                                                        
 "set autoindent           "vim使用自动对齐，也就是把当前行的对齐格式应用到下一行(自动缩进）                               
 "set cindent              "cindent是特别针对 C语言语法自动缩进                                                            
 "set smartindent          "依据上面的对齐格式，智能的选择对齐方式，对于类似C语言编写上有用                                
 "set ai                   "设置自动缩进                                                                                   
 "set cursorline          "为光标所在行加下划线                                                                            
set laststatus=2         "总是显示状态行                                                                                        
set shiftwidth=4         "设定 << 和 >> 命令移动时的宽度为 4                                                              
set tabstop=4            "设定 tab 长度为 4                                                                                     
set softtabstop=4        "使得按退格键时可以一次删掉 4 个空格                                                             
set autoread             "文件在Vim之外修改过，自动重新读入                                                                     
set ignorecase smartcase "搜索时忽略大小写，但在有一个或以上大写字母时仍保持对大小写敏感                                  
set incsearch            "输入搜索内容时就显示搜索结果                                                                          
set hlsearch             "搜索时高亮显示被找到的文本                                                                      
set showmatch            "设置匹配模式，类似当输入一个左括号时会匹配相应的那个右括号      
set history=1000         "记录历史的行数                                                                                  
set ruler                "在编辑过程中，在右下角显示光标位置的状态行                                                            
set nohls                "默认情况下，寻找匹配是高亮度显示，该设置关闭高亮显示                                            
set incsearch            "在程序中查询一单词，自动匹配单词的位置；如查询desk单词，当输到/d时，会自动找到第一个d开头的单词  
set backspace=2          "设置退格键可用                                                                                  
set helplang=cn          "帮助系统设置为中文                                                                                    
"set foldmethod=syntax    "代码折叠      
set encoding=utf-8       "设置字符编码                                                                                    
set termencoding=utf-8                                                                                                    
set fileencoding=utf-8                                                                                                    
set fileencodings=utf-8,gbk
```
