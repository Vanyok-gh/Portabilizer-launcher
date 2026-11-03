# Portabilizer 新功能

## v9.1

- 界面语言：新增“语言”选项卡（带地球图标），与 Windows 设置类似：每种语言以其自身名称显示，下方是该语言在界面语言中的名称。窗口、提示、日志、对话框和历史记录均已翻译。更改语言会重启窗口；您的设置会保留
- 语言：34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- 首次启动时使用 Windows 的语言（如果在已翻译的语言之列），否则使用英语
- portabilizer.log 文件仍以俄语写入，这样更便于排查错误

## v9.0

- 无需安装库：程序会识别游戏或应用所需的库，并提议将其放在 exe 旁边（这些文件已内置于 Portabilizer）
- DirectX：2010 年 6 月版以及 2005-2009 年的旧版本（d3dx9_24…43、d3dx10、XACT、XAudio、xinput），适用于老游戏
- Visual C++ 2010、2012、2013 和 2015-2022，OpenAL（连同 wrap_oal.dll）
- 程序自身无法读取的 Cab 包不再被跳过：由 expand.exe（Windows）负责解压
- 库集合由 tools/collect_redist.bat 脚本生成

## v8.9

- 模式 R：普通 exe 不再被复制，而是移动到 App 文件夹。在同一驱动器上这是瞬间完成的，且无需额外空间（以前运行期间需要两倍的空间）
- 对于压缩包和安装程序，模式 R 仍然需要空间：它们会先被解压，然后才删除源文件。您可以通过“目标”字段解压到另一个驱动器
- 已更新模式 R 的提示和确认窗口
- 像素风铅笔图标（普通版本为蓝色，R 为红色），用于“经典（系统）”主题；其他主题保留平滑图标

## v8.8

- 更新检查：程序自行检查 GitHub Releases，并在新版本发布时通知您（可通过“版本”选项卡上的复选框关闭）
- 与 Portabilizer Launcher 配合更好：版本以列表显示、“新功能”说明、一键安装

## v8.7

- 主题：浅色、深色、适用于模式 R 的红色主题，可自选颜色
- 自动搜索已安装的 7-Zip
- DirectX 库内置于程序中（如果游戏缺少这些库，会出现对话框）
- 对要求管理员权限的程序，可在不出现 UAC 提示的情况下启动
- 移除了重复的内存提示
