# Anti Poaching Platform 中国盗猎大数据统计平台 (暂定名)

通过分析裁判文书网上的判决书, 通过可视化大数据的形式, 呈现出中国盗猎的最新动向和历史信息

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

项目使用Python开发, 通过Docker Compose进行部署

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

## 待办事项

- TODO List: [#2](https://github.com/Henry3510/anti-poaching-platform/issues/2)
