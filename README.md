![image](./README.assets/image.png)

## 简介

一个极其简单的调用阿里云接口，文本生成语音的GUI工具

特点

- 简单：主打一个简单，核心代码不到两百行，修改自定义方便，诞生的目的是给自家人用，配置好之后只需要点点点

- 安全：使用自己的阿里云接口，没有第三方能看到你的内容

功能

- 设置语速
- 合成语音
- 设置发音人
- 设置自定义路径
- 合成之后点击播放

后续任务
- 设置语调

## 使用方法

### 编译：

1. 自己编译

   ```shell
   # 克隆项目，使用git或者直接下载包
   git clone https://github.com/Sisyphean-a/AliyunSpeakEasy.git
   
   # 安装环境，推荐pipenv
   # 如果不想使用3.11，就把Pipfile以及Pipfile.lock删除再进行后续操作
   winget install Python.Python.3.11
   pip install pipenv
   
   # 创建虚拟环境
   cd .\AliyunSpeakEasy
   pipenv install

   # 进入虚拟环境
   pipenv shell
   
   # 打包成单文件
   pyinstaller -F -w --icon icon.ico main.py
   ```

2. 使用我打包的文件

### 获取阿里云API

进入阿里云，注册访问控制和语音合成，获取三大项

1. 访问控制：https://ram.console.aliyun.com/overview

   这里生成一个用户，赋予权限，获取**AccessKey ID**与**AccessKey Secret**

2. 职能语音交互：https://nls-portal.console.aliyun.com/overview

   这里生成一个项目，获取**appkey**

### 开始使用

点击设置，填入三大项，路径可以填可以不填，不填默认当前路径


## 项目主要结构

```shell
C:.
|   aliyun_api.py		# 阿里云接口调用api
|   main.py				# 代码入口，也是代码的主体部分
|   read_setting.py		# 配置文件读取类，用来读取配置文件信息并提供判断
|   setting_gui.py		# 设置面板
|
+---.github
|   \---workflows
|           windows-app.yml		# 调用Github Action直接生成exe文件
|
+---test
        aliyun_api_test.py  	# 测试阿里云接口类
        read_setting_test.py	# 测试配置文件读取类
        setting_gui_test.py		# 测试设置GUI面板类
```

### 推荐自定义修改内容：

- main.py：
  - 设置组件（大小、文本、位置），绘制主体GUI面板
  - 设置发音人相关内容，搜索**voice**组件进行修改，第一个值为默认值。参考：[阿里云发音人选项](https://help.aliyun.com/document_detail/84435.html?spm=a2c4g.84425.0.i0#section-uft-ohr-827)
  - 设置音频命名格式，搜索**music_path**变量进行修改
- aliyun_api.py：
  - 设置目标地址url，搜索**API_URL**变量进行修改。参考：[阿里云语音合成服务地址](https://help.aliyun.com/document_detail/84435.html?spm=a2c4g.84425.0.i0#section-nme-tcl-xuc)

- setting_gui.py：
  - 设置设置组件（大小、文本、位置），绘制设置GUI面板
  - 设置配置文件保存地址、配置文件名称，相关参数：**user_dir**、**load_path**
