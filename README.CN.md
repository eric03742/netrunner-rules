# 《矩阵潜袭完整规则书》生成工具

## 简介

本项目是 [rubenpieters/netrunner-comprehensive-rules](https://github.com/rubenpieters/netrunner-comprehensive-rules) 的中文版开发 fork 分支。

netrunner-comprehensive-rules 是用于将YAML格式书写的规则文档转换为HTML或PDF等格式化输出的项目。

本项目主要用于实现将规则文档翻译为中文、并使用与原项目相同的方式生成HTML格式输出的工作流。

## 分支说明

本项目的分支使用说明如下：

* `master`：主分支，不允许进行任何修改与提交。此分支仅用于同步原项目的上游改动。
* `translation`：开发分支，项目开发、文档更新、翻译更新等修改全部在此分支上进行。

## 项目说明：

本项目实际的翻译工作主要在 [ParaTranz](https://paratranz.cn/) 上进行，本项目在原项目的基础上创建了 `transformer` 工程，用于在项目中的规则文档与ParaTranz所使用的格式之间进行转换并同步更新翻译内容。

本项目主要实现和使用的工作流如下：

* 保存来自ParaTranz的翻译文件：
    * 从ParaTranz下载的翻译文件放在 `transformer/paratranz` 中
* 将YAML格式源文档转为ParaTranz使用的JSON格式：
    * 在 `transformer` 文件夹中执行：`python to_ParaTranz.py`
    * 这一工作流会将 `data/input` 中YAML格式的规则文档转为ParaTranz使用的JSON格式，保存在 `transformer/yaml2json` 中
    * 如果 `transformer/paratranz` 中有对应的译文，转换时也将同步导入已有的译文
* 将ParaTranz下载的JSON格式译文转为源文档所使用的YAML格式:
    * 在 `transformer` 文件夹中执行：`python from_ParaTranz.py`
    * 这一工作流会使用 `transformer/paratranz` 中的译文将原项目文档中的文本替换为翻译后的译文，并保持其原结构不变，保存在 `transformer/json2yaml` 中
* 生成HTML页面：
    * 在项目根目录执行：`python -m rules_doc_generator`
    * 生成脚本已改为使用 `transformer/json2yaml` 中翻译后的规则文档
    * 生成的HTML页面位于 `html/rules.html`
    * `frame.html` 可以浏览中英双语对照版本

## 版权

项目维护：Eric03742
规则翻译：Eric03742
