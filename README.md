# AI 求职助手（Agent Skill）

装上这个 skill 以后，你的 AI 助手（Claude Code 或 Codex）会帮你找岗位、核实还在招、对照你的真实经历写定制求职邮件，并存进 Mail.app 草稿。**你审核过、明确说"发送"之后才会发出去。**

我自己就在用这套流程找工作：发出的第二封邮件，第二天 HR 就加我微信约了面试。

## 它做什么

```
搜索岗位 ─▶ 打开链接核实还在招 ─▶ 按届别/年限/技能筛选 ─▶ 对照你的真实经历做匹配分析
                                                              │
               ┌──────────────────────────────────────────────┤
               ▼                                              ▼
     有核实过的招聘邮箱                                  只能官网投递
   写定制邮件，附对应简历                           记进工作台，你自己去官网投
   存进 Mail.app 草稿（不发送）
               │
               ▼
        你审核，明确说"发送"
               │
               ▼
     发送前再核对收件人和附件，发送，记录
```

## 三条底线

1. **不自动发送**：所有邮件停在草稿箱，你说"发送编号 1、2"这种明确的话才发。
2. **不编造经历**：只用你经历库里的真实内容，JD 要求而你没有的技能会标成差距，不硬凑。
3. **先核实再投**：每个岗位都打开链接确认在招，看清届别和年限门槛，不猜 HR 邮箱。

## 先说局限

- **能直接发邮件的岗位很少。** 大部分公司用官网招聘系统收简历，所以多数岗位最后会记进工作台，要你自己去官网投。它帮你省的是找岗位、核实、筛选、写邮件这些最耗时间的活。
- 建草稿和发送只支持 **macOS 的 Mail.app**。
- AI 也会看错、漏看，每封草稿发之前请自己读一遍。

## 安装

需要：一台 Mac，Mail.app 里已添加你的求职邮箱；装好 [Claude Code](https://claude.com/claude-code) 或 [Codex](https://openai.com/codex)。

三种装法，选一种就行：

**1. 让 AI 帮你装（最简单）**

对你的 Claude Code 或 Codex 说：

```
帮我安装这个 skill：https://github.com/Wanqing-Chenn/ai-job-hunting-agent
```

**2. 一行命令**

在"终端"里运行：

```bash
# Claude Code
git clone https://github.com/Wanqing-Chenn/ai-job-hunting-agent.git ~/.claude/skills/ai-job-hunting-agent
```

```bash
# Codex
git clone https://github.com/Wanqing-Chenn/ai-job-hunting-agent.git ~/.codex/skills/ai-job-hunting-agent
```

**3. 下载压缩包**

在本页面点绿色的 **Code** 按钮，选 **Download ZIP**。解压后把文件夹改名为 `ai-job-hunting-agent`，放进 `~/.claude/skills/`（Claude Code）或 `~/.codex/skills/`（Codex）。这两个文件夹是隐藏的，在访达里按 Shift+Cmd+G，输入路径就能打开。

更新：用命令安装的，进到上面的文件夹运行 `git pull`；用压缩包安装的，重新下载替换。

## 第一次使用

打开 Claude Code 或 Codex，说：

```
帮我配置求职助手
```

它会一步步问你：求职邮箱、目标城市和岗位、经验情况，然后在 `~/求职工作区/` 帮你建好文件夹，读你的简历整理出经历库（拿不准的地方会问你），最后给你自己的邮箱建一封测试草稿，确认一切正常。

第一次操作 Mail.app 时，macOS 会弹窗问是否允许，点"允许"。

## 常用说法

| 你想做的 | 这样说 |
|---|---|
| 找一轮岗位 | 开始今天的求职任务 |
| 指定方向 | 继续找上海和苏州的外企，方向是 AI 产品经理，重点看应届能投的 |
| 平台上看到好岗位 | 这是我在 Boss 上看到的岗位：（链接或粘贴 JD），帮我看看能不能发邮件 |
| 检查草稿 | 列出草稿箱里的求职邮件，核对收件人和附件 |
| 发送 | 发送编号 1、2 |
| 准备面试 | XX 公司约我明天下午面 XX 岗位，帮我准备 |

## 你的数据放在哪

经历库、简历、投递记录、邮件留档都在你自己电脑的 `~/求职工作区/` 里，不在 skill 文件夹里。更新 skill 不会覆盖你的数据，也不会把它们传到网上。

## 文件说明

```
SKILL.md                     skill 入口：触发条件、首次配置、日常流程
references/rules.md          工作规则细则
references/sources.md        去哪找岗位、常见的坑
references/profile-template.md  经历库模板
assets/config-template.md    工作区配置模板
scripts/workbench.py         生成和更新求职投递工作台（Excel）
scripts/                     Mail.app 脚本：查看账号、建草稿、核对草稿箱、发送
```

## 请善意使用

这套流程的前提是人审核每一封邮件。请不要把它改成自动群发：这会打扰 HR，也容易让你的邮箱被当成垃圾邮件。招聘平台请遵守平台规则自己操作。

## License

MIT
