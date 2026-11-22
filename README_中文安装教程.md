# PH Infra Watch V9.0：从零建立全新 GitHub 仓库

> 完整包：直接创建 **新 Repository**，无需任何旧版文件，也不需要从 V7、V8 复制内容。
>
> 数据快照：截至本包制作时保留的 266 条项目记录与 227 条企业／主体记录；**媒体新闻最初为 0 条候选，需首次运行 GitHub Actions 后才会联网采集**。

## 1. 新版本包含什么？

V9 保留三个工作区：**菲律宾地图项目**、**工程项目清单与分类筛选**、**投资方／业主／EPC／分包商企业关系**；新增「媒体线索」工作区，将菲律宾新闻媒体与公开公告的候选信息单独展示，**不会自动加入已核验项目地图**。

核心改进：

- 现有 266 条项目与 227 条企业／主体档案均包含在安装包内。
- 配置 25 组来源，其中 **10 组媒体原生 RSS**、**15 组 Google News 定向索引检索**（后者不是直接抓取媒体网站）。
- 支持按媒体、新闻主题、关键词、时间和来源方式筛选新闻线索；可查看采集成功／失败次数及来源状态。
- GitHub Actions 默认在菲律宾时间约 **10:17 和 22:17** 启动；GitHub 定时运行有可能延迟或被暂停。
- 采集结果作为 Pages 静态快照发布，不自动提交到 `main`。通过 Actions Cache 尽量保留历史新闻候选；缓存可以过期或被移除，**不是永久新闻数据库**。
- 该项目不使用付费 AI API，新闻分类／优先级是规则处理，而不是模型完成的事实核验。

## 2. ZIP 解压后的正确结构

```text
ph-infra-watch-v9/     ← 你在 GitHub 新建的仓库名可以不同
├── index.html         ← V9 官方首页，直接访问根网址
├── v9.html            ← 同一页面，兼容独立预览地址
├── .nojekyll
├── README.md
├── README_中文安装教程.md
├── config/
│   └── news_sources.json       ← 25 组媒体／政府公告入口
├── data/
│   ├── projects.json           ← 原有 266 个项目，含原文链接
│   ├── companies.json          ← 227 条企业／主体档案
│   ├── media_leads.json        ← 候选新闻种子，初始为空
│   └── media_status.json       ← 来源采集状态，初始为未运行
├── scripts/
│   └── collect_news_v9.py     ← 自动采集程序（Python 标准库）
├── tests/
│   └── test_collector.py      ← 离线测试
└── .github/
    └── workflows/
        └── collect-public-leads.yml  ← 定时采集 + Pages 发布
```

**最重要：压缩包内的上述文件，应直接位于新仓库根目录。不要额外套第二层同名文件夹，也不要把 ZIP 文件直接作为网站上传。**

## 3. 通过 GitHub Desktop 从零建立仓库（推荐）

1. 启动 GitHub Desktop，点击 **File → New repository**。
2. Repository name 推荐：`ph-infra-watch-v9`（与以前的 `ph-infra-watch-new` 不同）。
3. 选择 `Documents/GitHub` 作为本地父目录，点击 **Create repository**。
4. 右键 ZIP → **全部解压缩**，进入解压得到的文件夹，**选中其中所有内容**，包括 `.github`、`config`、`data`、`scripts`、`tests` 和 HTML 文件，复制到新建的仓库文件夹。
5. 在 GitHub Desktop 左下角 Summary 输入：`Initialize PH Infra Watch V9 full site`，点击 **Commit to main**。
6. 点击顶部 **Publish repository**。仓库选择 **Public（公开）**（使用 GitHub Free 免费 Pages 时通常需要公开）。发布前确保无密码、API Key 或不允许公开的资料。
7. 在浏览器访问新仓库：`https://github.com/你的GitHub用户名/ph-infra-watch-v9`。确认 Code 下有上述文件及目录。

如果不使用 GitHub Desktop，也可以先在 GitHub 网页创建 **Public** 新仓库，然后在根目录用 **Add file → Upload files** 上传解压后的文件夹内容；尤其要检查 `.github/workflows/collect-public-leads.yml` 的路径准确。

## 4. 第一次设置 GitHub Pages

1. 打开仓库顶部的 **Settings → Pages**。
2. 在 **Build and deployment → Source** 下拉框选择 **GitHub Actions**。不需要点 Jekyll/Static HTML 的 Configure。
3. 回到 **Actions**，在左侧选择 **Collect PH project leads and publish Atlas V9**。
4. 点击 **Run workflow → main → Run workflow**。
5. 运行结束后，重点检查 `Collect ... RSS`、`Configure GitHub Pages`、`Upload site artifact`、`Deploy site` 都为绿色对勾。
6. 成功发布后首页地址预计是：

   `https://你的GitHub用户名.github.io/ph-infra-watch-v9/`

   独立页面：`https://你的GitHub用户名.github.io/ph-infra-watch-v9/v9.html`

以你实际创建的仓库名为准。第一次 Pages 初始化、免费计划权限或仓库访问策略不同，可能导致报错；以 Actions 日志定位。

## 5. 第一次进入网站后检查什么？

- 打开 **项目地图**：项目总量应为 266；部分点位仅是行政区参考位置，不是真实施工坐标。
- 打开 **项目清单**：确认风电、光伏、储能、ICT、数据中心、工程阶段、资料日期筛选能用。
- 打开 **企业关系**：能根据名称和已核实参与角色反查工程。没有披露的承包商和分包商不自动补造。
- 打开 **媒体线索 → 来源覆盖及采集结果**：显示 25 组来源、各自响应状态和新闻条数。某些媒体可能封锁 RSS、改版或暂时无法读取，失败会记录。**采集入口数≠成功采集源数**。
- 打开 **新闻候选**：只显示符合能源、基建、数据中心、通信等关键词的**候选报道**。并非已经验证的项目。初次安装前显示 0 是正常的。

## 6. 新媒体和数据更新方式

- 修改 `config/news_sources.json` 中 `sources[]`，可添加 `method: "rss"` 且具有公开 RSS URL 的网站；或 `method: "google_news_search"` 且配置搜索查询的媒体索引。
- `scripts/collect_news_v9.py` 只读取 RSS 元数据及短摘要，不下载付费文章全文、无授权内容或绕过登录。
- 添加确认项目时，编辑 `data/projects.json`；企业档案可以在 `data/companies.json` 中补充 `description`、`description_source_url`、`website` 和 `project_ids`。
- 正式项目应有项目名、实际地区、规模口径、项目主体／业主、来源 URL、资料日期与核验状态；缺少信息要写“待核验”，**不要把新闻标题直接转成正式工程**。
- 只要 `main` 发生影响页面或配置的提交，工作流会重新发布。定时任务每约 12 小时执行一次，不自动往 `main` Push，避免你以前遇到的 `fetch first` 同步冲突。
- 历史线索采用 GitHub Actions Cache 尽力保存；若需要长期永久留存，后续可以再配置独立归档存储。

## 7. 准确性和使用限制

1. 266 条项目是 **已有资料快照**，包括规划／开发中／已运营等不同阶段，不能全部认定为当前可投标项目；DOE 的清单日期也不等于项目开工日期。
2. 227 是企业或项目主体记录总量，不代表 227 家经过工商登记交叉核验的投资机构。页面按名称归一化后显示数量可能略有差异。
3. 原新闻来源可能迁移、删除或返回 404，需以实际可访问的公告或媒体网站核对；可以到外部网站搜索原项目名称。
4. 自动媒体采集依靠公共 RSS／Google News 索引：**不能保证覆盖全菲律宾所有公开网站或所有历史新闻**。如果来源有失败，应先检查来源状态而不是增加错误条目。
5. 新闻标题／短摘要只用于信息发现，转载或复用全文必须遵守来源网站版权和使用条款。
6. 地图使用 Leaflet + OpenStreetMap 公共底图，不需要付费 Key；访问需要网络，且须遵守地图瓦片服务的合理使用政策。

## 8. 离线验证

在仓库根目录执行：

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/collect_news_v9.py
```

无第三方 Python 依赖。网页本身为 HTML / CSS / JavaScript 静态文件。

**注意**：新仓库首次部署需要运行 GitHub Actions；直接双击本地 HTML 也能看到项目数据快照，但实时新闻候选无法凭空生成。
