# Anti Poaching Platform 中国盗猎大数据统计平台 (暂定名)

通过分析裁判文书网上的判决书, 通过可视化大数据的形式, 呈现出中国盗猎的最新动向和历史信息

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

项目使用Python构建, 通过Docker进行部署

## 开发环境

推荐使用 Linux. Windows下开发可使用 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install)

### 依赖

- [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/), [Python 3.10](https://www.python.org/downloads/release/python-3100/)


部署项目 (开发环境):

构建开发环境

    make build-dev

运行开发环境

    make run-dev

运行测试

    make run-tests

## 结构概览

    ├── Dockerfile
    ├── Makefile
    ├── README.md
    ├── docker-compose.yml
    ├── pyproject.toml
    |   # 数据清洗/处理
    ├── analytics
    │   ├── analyze.py
    |   |   # 现有的数据集, 包含十份判决书与两份从[OpenLaw](http://openlaw.cn/)上批量下载的判决书数据
    │   ├── data
    │   │   ├── *.txt
    │   │   ├── lexicon.json  # 物种名称词库，目前包括：
    |   |   |                 # - 鸟纲
    |   |   |                 # - 爬行纲
    |   |   |                 # - 鱼纲
    |   |   |                 # - 文昌鱼纲
    │   │   ├── openlaw.xlsx  # 批量下载的数据（前50份）
    │   │   ├── openlaw_full.xlsx  # 批量下载的全部数据（1000份）
    │   │   ├── opt.json  # openlaw_full.xlsx清洗过后的数据
    │   │   └── src_keywords.json  # 盗猎来源关键词
    │   ├── get_data.py  # 物种词库爬虫
    |   |
    │   └── lib
    │       ├── data_types.py  # 数据分析的数据结构
    │       ├── debug.py  # 来源分析debug工具
    │       └── tree.py  # 构建来源分析树
    |   # 项目Python依赖
    ├── requirements
    │   ├── common.in
    │   ├── common.txt
    │   ├── dev.in
    │   └── dev.txt

## 待办事项

- [ ] GraphGL支持
- [ ] 数据库表结构及迁移
- [ ] 配置生产环境
- [ ] 集成测试
