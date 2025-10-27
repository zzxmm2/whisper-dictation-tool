# GitHub Setup Instructions

## 如何将项目推送到GitHub

### 1. 在GitHub上创建新仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 仓库名称：`whisper-dictation-tool`
4. 描述：`A powerful speech-to-text dictation tool using OpenAI's Whisper model`
5. 选择 "Public" 或 "Private"（根据你的需要）
6. **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
7. 点击 "Create repository"

### 2. 连接本地仓库到GitHub

在项目目录中运行以下命令：

```bash
cd /home/zihan/Zihan_GitHub/whisper-dictation-tool

# 添加远程仓库（替换 YOUR_USERNAME 为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/whisper-dictation-tool.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 3. 验证推送

访问你的GitHub仓库页面，确认所有文件都已成功上传。

## 项目结构说明

```
whisper-dictation-tool/
├── dictation.py              # 主要的语音转文字脚本
├── dictation_gui.py          # GUI界面脚本
├── install.sh                # 安装脚本
├── launch_dictation.sh       # 后台启动脚本
├── start_dictation_gui.sh    # GUI启动脚本
├── requirements.txt          # Python依赖包
├── setup.py                  # Python包安装配置
├── test_conversion.py        # 中文转换测试脚本
├── WhisperDictation.desktop  # 桌面快捷方式
├── README.md                 # 项目说明文档
├── MODEL_CONFIG.md           # 模型配置说明
├── .gitignore               # Git忽略文件
└── GITHUB_SETUP.md          # GitHub设置说明（本文件）
```

## 功能特点

- 🎤 使用Alt+D快捷键控制录音
- 🗣️ 基于OpenAI Whisper的实时语音识别
- 🌍 支持中英文混合语音识别
- 🇨🇳 自动将繁体中文转换为简体中文
- ⌨️ 自动将识别结果输入到当前活动窗口
- 🖥️ 提供GUI和命令行两种界面
- 🔧 简单的安装和配置流程

## 使用说明

1. 运行 `./install.sh` 安装依赖
2. 运行 `./start_dictation_gui.sh` 启动GUI版本
3. 或运行 `./launch_dictation.sh` 在后台运行
4. 按Alt+D开始/停止录音
5. 语音会被自动识别并输入到当前窗口

## 技术栈

- Python 3.8+
- OpenAI Whisper
- PyAudio (音频处理)
- PyAutoGUI (自动输入)
- PyPerClip (剪贴板操作)
- PyNput (快捷键监听)
- Tkinter (GUI界面)
