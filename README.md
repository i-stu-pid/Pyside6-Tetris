# 一、说明
  仿照 pyside6 官方例程实现的俄罗斯方块游戏

# 二、可执行文件
  1. 工程目录的dist文件夹下为已经打包好的可执行文件
  2. 拷贝 tetris_game 文件夹到自己的目录，运行其中的 tetris_game.exe 文件即可
  
# 三、开发说明
  1. 语言 : python (3.12)
  2. 环境 : vscode + miniconda
  3. 包 : 
     1. conda : environment.yml (执行命令一键安装: conda env create -f environment.yml )
     2. pip : requirements.text (执行命令一键安装: pip install -r requirements.txt )
  4. 生成可执行文件 : 
     1. 打开 build.bat 文件, 配置参数并保存
     2. 双击运行 build.bat 文件
  5. 清除编译缓存 : 双击运行 cleanup.bat 文件
