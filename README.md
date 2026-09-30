# AI Job Hunting Agent

让 AI 编程助手（Codex / Claude Code）帮你找岗位、写定制求职邮件、存进 Mail.app 草稿，**由你审核后再发送**。

我自己用这套流程找工作：发出的第二封邮件，第二天 HR 就加微信约了面试。这里把规则和脚本整理成模板，所有个人信息都已去掉，你换成自己的就能用。

## 它做什么

```
搜索岗位 ─▶ 打开链接核实还在招 ─▶ 按届别/年限/技能筛选 ─▶ 对照你的真实经历写匹配分析
                                                              │
               ┌──────────────────────────────────────────────┤
               ▼                                              ▼
     有核实过的招聘邮箱                                  只能官网投递
   写定制邮件，附对应简历                           整理进投递清单，你自己去投
   存进 Mail.app 草稿（不发送）
               │
               ▼
        你审核，明确说"发送"
               │
               ▼
     发送前再核对收件人/附件，发送，记录
```

## 三条原则（写死在 AGENTS.md 里）

1. **不自动发送**。所有邮件停在草稿箱，只有你说"发送编号 1、2"这种明确的话才发。
2. **不编造经历**。简历和邮件只能用你经历库里的真实内容，JD 要求你没有的技能就标为缺口，不硬凑。
3. **先核实再投**。每个岗位都要打开链接确认还在招，看清毕业届别和年限门槛，不猜 HR 邮箱。

## 先说局限

- **能直接发邮件的岗位很少。** 大多数公司用官网招聘系统收简历，所以大部分岗位最后会整理成官网投递清单，要你自己去投。详见 [SOURCES.md](SOURCES.md)。
- 只支持 **macOS + Mail.app**（用 AppleScript 建草稿）。
- AI 可能看错、漏看，所以每封草稿发之前都要你自己读一遍。

## 需要准备

- 一台 Mac，Mail.app 里已添加你的求职邮箱账号
- 一个能读写本地文件、能运行命令的 AI 编程助手：[Claude Code](https://claude.com/claude-code) 或 [Codex](https://openai.com/codex)
- 你的简历（docx 和导出好的 PDF）

## 配置步骤

1. **下载**这个仓库到本地，比如 `~/job-hunting-agent`。

2. **填经历库**：复制 `profile/profile.template.md` 为 `profile/profile.md`，填上你的真实经历。不想手填的话，把简历放进 `resumes/`，用 [prompts/prompts.md](prompts/prompts.md) 里的第一条指令让 AI 帮你整理，它拿不准的地方会来问你。

3. **放简历**：简历放进 `resumes/`。

4. **改规则**：打开 `AGENTS.md`，把所有 `{{...}}` 换成你的信息：姓名、求职邮箱、目标城市和岗位、各版本简历的用途。

5. **建 tracker**：
   ```bash
   mkdir -p applications && cp templates/application_tracker.csv applications/
   ```

6. **确认 Mail.app 账号名**：
   ```bash
   osascript scripts/list_accounts.applescript
   ```
   记下求职邮箱对应的"账号名"和草稿箱的名字（网易邮箱叫"草稿箱"，Gmail 叫"Drafts"）。第一次运行时 macOS 会弹窗问是否允许终端或 AI 助手控制 Mail，选允许。

7. **试建一封草稿**（收件人填你自己的邮箱）：
   ```bash
   osascript scripts/create_mail_draft.applescript "你的姓名 <你的求职邮箱>" 正文.txt "测试主题" 你自己的邮箱 /绝对路径/简历.pdf
   osascript scripts/check_drafts.applescript "账号名" "草稿箱"
   ```
   草稿箱里出现这封、附件正确，就配置好了。

## 使用

在 AI 助手里打开这个文件夹，说：

```
读 AGENTS.md，按规则开始今天的求职任务。做完停下来汇报，不要发送任何邮件。
```

更多指令（指定方向、交给它平台上看到的岗位、审核草稿、发送、准备面试）见 [prompts/prompts.md](prompts/prompts.md)。

## 目录

```
AGENTS.md                  工作规则（Codex 读这个）
CLAUDE.md                  指向 AGENTS.md（Claude Code 读这个）
SOURCES.md                 去哪找岗位、常见的坑
profile/profile.template.md  经历库模板
prompts/prompts.md         常用指令
scripts/                   Mail.app 脚本：建草稿、核对草稿箱、查看账号
templates/                 tracker 表头模板
resumes/                   放你的简历（不会被上传）
```

## 隐私

`profile/`、`resumes/`、`applications/`、`drafts/`、`jobs/` 都在 `.gitignore` 里，默认不会被提交。如果你要 fork 后公开自己的版本，提交前再检查一遍，别把手机号、邮箱、简历、HR 的信息传上去。

## 请善意使用

这套流程的前提是**人审核每一封邮件**。请不要把它改成自动群发：这会打扰 HR，也会让你的邮箱被当成垃圾邮件。招聘平台（Boss 直聘、猎聘等）请遵守平台规则自己操作，不要用自动化脚本。

## License

MIT
