# 这个程序的目的是快速进行latex模板的修改
# 引入包
import os

# 引入函数
from function import *

# 在总文件夹中，有很多个从外部下载下来的期刊latex模板作为例子
# 你可以新建一个文件夹来放你需要被修改的latex文件，例如可以给这个文件夹起名叫做your_work_to_be_converted
# 你也可以新建一个文件夹来放你需要修改成的期刊latex模板，例如可以给这个文件夹起名叫做target_converted_template

# 选择需要被修改的文件夹路径

# 由于这里我想把CVPR 2022模板作为我需要被修改的latex文件，把ECCV 2016模板作为目标模板，我直接选择了这两个模板的文件夹
# 如果你想要放你的文件夹和别的目标模板的话，你也可以自行修改下面的两行代码为：
# your_work_folder = './your_work_to_be_converted'
# target_template_folder = './target_converted_template'

your_work_folder = './CVPR 2022'
target_template_folder = './ECCV 2016'



# 为了不影响原始的文件，我们新建两个副本文件夹来放要被修改的文件和目标模板
# 之后的操作我们都在这两个副本文件夹上操作，最终的结果会储存在converted_result_folder文件夹中
converted_result_folder = './converted_result'
target_template_folder_copy = './target_template_copy'

create_copy_folder(your_work_folder,converted_result_folder)
create_copy_folder(target_template_folder,target_template_folder_copy)

# 获取需修改文件和目标模板的tex文件
yourwork_tex_files = get_tex_files(converted_result_folder)
target_tex_files = get_tex_files(target_template_folder_copy)

# 在实际操作中，发现一个完整的latex文件夹中可能出现多个tex文件，所以在这种情况时需要让用户手动选择以下哪个tex文件是论文主体的tex文件

# 检查需修改的latex文件夹中是否有.tex文件
if not yourwork_tex_files:
    print("需修改的文件夹中没有 .tex 文件！")
else:
    if len(yourwork_tex_files) > 1:
        print(f"需修改的文件夹中有 {len(yourwork_tex_files)} 个.tex文件：")
        yourwork_main_tex = choose_main_tex_file(yourwork_tex_files)
        print(f"选择的需修改的主文件: {yourwork_main_tex}\n")
    else:
        yourwork_main_tex = yourwork_tex_files[0]
        print(f"需修改的文件夹中只有一个.tex文件，自动选择: {yourwork_main_tex}\n")

# 检查目标模板是否有.tex文件
if not target_tex_files:
    print("目标模板文件夹中没有 .tex 文件！")
else:
    if len(target_tex_files) > 1:
        print(f"目标模板文件夹中有 {len(target_tex_files)} 个.tex文件：")
        target_main_tex = choose_main_tex_file(target_tex_files)
        print(f"选择的目标模板主文件: {target_main_tex}\n")
    else:
        target_main_tex = target_tex_files[0]
        print(f"目标模板文件夹中只有一个.tex文件，自动选择: {target_main_tex}\n")

# 至此，我们已经新建了副本文件夹作为工作区，并找到了需修改和目标模板文件夹中的tex文件，下面我们需要对工作区中的tex文件内容进行一些修改
# 做以下修改顺序的操作是为了分开\maketitle的部分和论文最开头定义排版格式的部分

# 需要对\maketitle, \begin{document}, title{...}, \author{...}, \institution{...}进行位置上的更改操作
# 想要基于\maketitle的位置，得到以下顺序：

# \begin{document}
# title{...}
# \author{...}
# \institution{...}
# \maketitle

# 对于被修改的文件夹中的论文主体tex文件：

# （调试部分可删去）先来看一下最开始\maketitle在什么位置
origin_maketitle_line = find_maketitle_line(yourwork_main_tex)
print(f"最初\\maketitle 在第{origin_maketitle_line}行")

# 为了防止注释对后续操作进行影响，我们先将\maketitle上方的注释给删掉
remove_comments_before_maketitle(yourwork_main_tex)

# （调试部分可删去）看一下删除注释后的\maketitle在什么位置
afterdeletecomment_maketitle_line = find_maketitle_line(yourwork_main_tex)
print(f"删除注释后新的\\maketitle 在第{afterdeletecomment_maketitle_line}行")

# 将\begin{document}放到\maketitle的上面
move_begindocument_before_maketitle(yourwork_main_tex)

# 将\title{...},\author{...}, \institution{...}依次放到\maketitle的上面
modify_command_position(yourwork_main_tex, 'title')
modify_command_position(yourwork_main_tex, 'author')
modify_command_position(yourwork_main_tex, 'institute')

# 除此之外，对于目标模板文件夹，我们也做一样的操作
# 做该操作的目的相同，是为了分开\maketitle的部分和论文最开头定义排版格式的部分
remove_comments_before_maketitle(target_main_tex)
move_begindocument_before_maketitle(target_main_tex)
modify_command_position(target_main_tex, 'title')
modify_command_position(target_main_tex, 'author')
modify_command_position(target_main_tex, 'institute')

# 我们已经做好了准备工作，下面正式来修改格式

# 对于被修改的文件夹中的论文主体tex文件：
# 删除被修改tex文件的\documentclass， \userpackage{sty_file_name}, 包含 mm 的 \usepackage{...} 语句
remove_documentclass(yourwork_main_tex)
remove_userpackage_sty_lines(your_work_folder, yourwork_main_tex)
remove_userpackage_mm_lines(yourwork_main_tex)

# 删掉\begin{document}上面除了\userpackage和\def之外的行
remove_lines_before_document(yourwork_main_tex)

# 识别新模板的sty和cls文件复制到旧模板里
manage_sty_files(target_template_folder_copy, converted_result_folder)
copy_cls_files(target_template_folder_copy, converted_result_folder)

# 把目标模板的tex文件中的\begin{document}的前面的部分全部复制到old_main_tex中，即把目标模板的格式代码复制到被修改的tex文件最前面
copy_pre_document_to_first_line(target_main_tex, yourwork_main_tex)

# ------------------------------
# 将目标文件夹下的.bst文件复制到被修改文件夹
copy_bst_files(target_template_folder_copy, converted_result_folder)

# 将bibstyle改成目标模板的格式
process_tex_files(yourwork_main_tex, target_main_tex)

# ------------------------------
# 以下是针对模板CVPR2022，ECCV2016，NeurIPS2024模板做出的补丁
# 如果你没有使用这些模板，也可以不加载下面的内容

print("以下是针对模板CVPR2022，ECCV2016，NeurIPS2024模板做出的补丁修改")

# bug 1:
# \begin{document}前加入\usepackage[OT1]{fontenc} 
add_fontenc_package(yourwork_main_tex)

# bug 2:
# 使用subfigure时会报错
# 在\begin{document}之前插入\usepackage{subcaption}
add_subcaption_package_before_document(yourwork_main_tex)

# bug 3:
# 当一个文档出现两次hyperref包时会报错
# 出现两次\userpackage{hyperref}，删掉后一个\userpackage{hyperref}
# remove_second_hyperref(yourwork_main_tex)
# 更新：
# 因为有些hyperref是自带在sty中的，所以这个方法并不合理
# 手动注释掉报错的hyperref就可以了



# bug 4:
# \author{...}中有换行，会报错，添加以下行在\begin{document}之前：
# \pdfstringdefDisableCommands{%
#   \def\\{}%
#   \def\texttt#1{<#1>}%
# }
add_pdfstringdef_before_document(yourwork_main_tex)

# bug 5:
# 当出现\eg等在原sty文件中的定义时出现bug，加入：
# \def\onedot{.} % 定义 \onedot 为句点
# % 定义缩写命令
# \def\eg{\emph{e.g}\onedot} 
# \def\Eg{\emph{E.g}\onedot}
# \def\ie{\emph{i.e}\onedot} 
# \def\Ie{\emph{I.e}\onedot}
# \def\cf{\emph{cf}\onedot} 
# \def\Cf{\emph{Cf}\onedot}
# \def\etc{\emph{etc}\onedot} 
# \def\vs{\emph{vs}\onedot}
# \def\wrt{w.r.t\onedot} 
# \def\dof{d.o.f\onedot}
# \def\iid{i.i.d\onedot} 
# \def\wolog{w.l.o.g\onedot}
# \def\etal{\emph{et al}\onedot}
add_custom_macros_before_document(yourwork_main_tex)

# bug 6:
# sty包受到大小写影响，比如emnlp2023.sty，要删掉\usepackage[review]{EMNLP2023}，因为大写所以没删成功

# -----------------------------

# converted_result文件夹中的内容就是修改格式完成后的结果
# 如果你的电脑安装了模糊编译latex文件的插件，此时在converted_result中的pdf文件就是修改完的tex文件编译后的pdf
# 如果没有自动生成pdf文件，请使用你的模糊编译latex文件的插件再次对tex文件进行编译
# 如果有红色错误，请把红色的部分给注释掉，再跑就能成功跑起来了




