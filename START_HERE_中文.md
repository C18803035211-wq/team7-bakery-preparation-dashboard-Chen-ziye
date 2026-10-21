# 🥐 从这里开始：Bakery Dashboard 的中文操作指南

**这个压缩包里已经包含：** 原始 CSV、EDA Notebook、Streamlit App、英文 README、自动核对指标的测试、uv 项目配置。文件不是一个真实已部署的网址；你需要用自己的账号完成 GitHub、Streamlit Cloud、Canvas 三处操作。

## 一、先下载并解压

1. 在 ChatGPT 回复中下载 `bakery-preparation-dashboard.zip`。
2. Windows：右键压缩包 → **全部解压缩 / Extract All**。Mac：双击压缩包解压。
3. 打开解压后的 **bakery-preparation-dashboard** 文件夹（也可能显示为 `bakery-preparation-dashboard`），确认直接看到 `app.py`、`README.md`、`requirements.txt`、`pyproject.toml`、`data`、`notebooks`。
4. 双击 `data` 文件夹，确认内有 `bread_basket.csv`。这个文件是程序要读取的，不要只上传 zip。

## 二、必须自己修改的两处

推荐使用 VS Code（或者能保存纯文本的编辑器）打开文件夹。

**A. 修改 app.py：**

1. 找到顶部的 `TEAM_NAME = "Bakery Insights Team"`。
2. 把 `Bakery Insights Team` 改为你自己的真实小组名称，或老师认可的个人项目名称。
3. 保存（Windows `Ctrl+S`，Mac `Cmd+S`）。

**B. 修改 README.md：**

1. 找到开头的 `Owner / team` 一行，写你的姓名/真实团队名（按课程要求，通常不需要放学号或敏感个人资料）。
2. 阅读 Step 1–4 的英文解释，至少自己核对一遍，并用自己的话补充 1–2 个你最认同的商业设计决定；老师特别看重你的个人判断。
3. 保存。

## 三、可选：在自己的电脑上先运行（推荐）

如果你不想装开发环境，也可以直接跳到下一节的 GitHub 云端部署。作业代码已经经过数据与逻辑测试；实际 Streamlit 运行仍需要在安装依赖后验证。

**安装 uv：** 按官方网页 https://docs.astral.sh/uv/getting-started/installation/ 安装。Mac 打开 Terminal，Windows 打开 PowerShell。安装后重新打开终端，输入 `uv --version`，出现版本号就成功。

**用 VS Code 打开项目并执行：**

1. VS Code → File → Open Folder → 选择解压后的项目文件夹。
2. Terminal → New Terminal（新建终端），确认所在目录包含 `app.py`。
3. 输入：

   ```bash
   uv sync
   uv run streamlit run app.py
   ```

4. 第一次执行 uv 可能自动下载 Python 3.14 与依赖；等待下载完成。浏览器通常会自动打开 `http://localhost:8501`。
5. 检查顶部有你的小组名，选择 `Weekday` 和 `Weekend` 时 KPI、两张图都会变化。
6. 关闭项目可回到终端按 `Ctrl+C`。

要核对逻辑：

```bash
uv run python -m unittest discover -s tests -v
```

**EDA Notebook：** 已包含执行过的输出，直接在 VS Code / GitHub 里打开 `notebooks/01_eda.ipynb` 就能阅读。如要在本机重新运行 Notebook，还需要给 uv 环境安装 `jupyter` 或 `ipykernel`（可以通过 `uv add --dev jupyter ipykernel` 添加）。

## 四、GitHub（必须自己点）

1. 浏览器打开 https://github.com/ 并登录**自己的**账号。
2. 右上角点击 **+** → **New repository**；也可以直接去 https://github.com/new 。
3. `Repository name` 输入 `bakery-preparation-dashboard`（可以换自己的名称）。
4. **Visibility 选 Public（公开）**；因为你已经有 README 文件，建议这里**不要**勾选新建 README。
5. 点击 **Create repository**。
6. 在空仓库页面点击 **uploading an existing file**，或者仓库页面 **Add file → Upload files**。
7. 打开电脑上解压好的项目文件夹，把里面的**文件和子文件夹一起上传**，不要只上传一个 zip：尤其必须有根目录下的 `app.py`、`bakery_analysis.py`、`README.md`、`requirements.txt`，以及 `data/bread_basket.csv`。
8. 提交说明写 `Initial bakery dashboard and EDA`，点击 **Commit changes**。
9. 上传后点开 GitHub 仓库，确认网址类似 `https://github.com/你的用户名/bakery-preparation-dashboard`，且根目录直接能看到 `app.py`（不应多套一层 `bakery-preparation-dashboard/`）。

**隐藏文件小贴士：** `.python-version`、`.streamlit/config.toml` 的文件名以点开头，文件管理器可能隐藏。Mac 按 `Cmd+Shift+.` 显示隐藏文件；Windows 在文件资源管理器 View → Show → Hidden items。未上传主题文件不会影响核心数据图表；不过 `.python-version` 最好也保留。不要上传 `.venv/` 文件夹。

官方图文参考：https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

## 五、Streamlit Cloud（必须自己点）

1. 浏览器打开 https://share.streamlit.io/ ，选择使用 GitHub 账号登录或按页面提示连接代码仓库。
2. 右上角点击 **Create app**。
3. 遇到 `Do you already have an app?`，选择 **Yup, I have an app**。
4. 按界面填写：
   - **Repository**：`你的GitHub用户名/bakery-preparation-dashboard`
   - **Branch**：`main`（如果你的仓库默认分支叫其他名称，以实际为准）
   - **Main file path**：`app.py`
5. 找到 **Advanced settings**，在 Python version 中选 **3.14**（这是老师的明确要求），点击 **Save**。
6. 点击 **Deploy**，等待构建完成。
7. 完成后应看到完整的 KPI 与两张图。实际网址是 `https://你的应用名.streamlit.app` 之类，**不要自己猜网址**，从网站复制真实链接。
8. 用无痕浏览器打开链接，测试不用登录 GitHub 也能看见应用。切换 `Weekday`、`Weekend` 观察结果改变。

**如果部署失败：** 在 Streamlit 页面找到 **Manage app / Logs**，把报错文字或截图发给我，我可以针对真实错误带你逐步修复。常见问题是忘记上传数据 CSV、依赖版本、选错 `app.py` 路径或没选择课程要求的 Python 版本。

官方教程：https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 六、Canvas 提交（必须自己点）

1. 打开老师的 Canvas 作业页面。
2. 复制**已实际打开并验证**的 Streamlit App URL。
3. 复制**你自己**的 GitHub Repository URL，其中必须能看到你的 `README.md`。
4. 按 Canvas 页面要求粘贴两个网址，点击提交按钮。不要只交截图，也不要提交别人的仓库链接。

## 七、提交前简短自检

- [ ] 我知道 `20,507` 是商品记录行数，`9,465` 才是独立交易笔数。
- [ ] 我能解释为什么要按“每个有记录的日期”计算平均日订单。
- [ ] 我能解释为什么没有库存时不能准确算生产数量或浪费。
- [ ] 我的 Dashboard 顶部最多三个 KPI，只有两张支持性图表与一个主要筛选器。
- [ ] 我的 Dashboard 有团队名、使用对象、历史数据时期、生产环境计划刷新频率。
- [ ] 我的 README 回答了老师 Step 1–4，并解释为什么排除另外两类图表。
- [ ] Streamlit Cloud Python 版本按老师要求设置成 3.14。
- [ ] 我的 GitHub URL 和 Streamlit URL 都能打开，Canvas 提交是我自己的成果。

## 需要帮助时

如果你卡在 GitHub 上传、uv 命令或 Streamlit 部署，直接告诉我你当前在哪一步、你看到哪个按钮/报错。我会从那一步继续，不需要你自己搜索一大堆教程。
