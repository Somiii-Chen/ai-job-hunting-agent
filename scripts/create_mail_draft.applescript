-- 在 Mail.app 里新建一封带附件的邮件并存为草稿。不会发送。
--
-- 用法:
--   osascript scripts/create_mail_draft.applescript \
--     "你的姓名 <you@example.com>" \
--     drafts/2026-10-01/01_公司_岗位.txt \
--     "AI应用工程师 - 你的姓名" \
--     hr@company.com \
--     /绝对路径/你的简历.pdf
--
-- 参数:
--   1 发件人，格式 "姓名 <邮箱>"，邮箱必须是 Mail.app 里已添加的账号
--   2 正文文本文件路径（UTF-8）
--   3 邮件主题
--   4 收件人邮箱
--   5 附件的绝对路径（推荐 PDF）
--
-- 运行后草稿存进该账号的草稿箱，撰写窗口会自动关掉。
-- 用 scripts/check_drafts.applescript 核对发件人、收件人和附件。

on run argv
	if (count of argv) is not 5 then error "需要 5 个参数: 发件人 正文文件 主题 收件人 附件路径"
	set theSender to item 1 of argv
	set bodyPath to item 2 of argv
	set theSubject to item 3 of argv
	set theTo to item 4 of argv
	set attachPath to item 5 of argv
	set theBody to read (POSIX file bodyPath) as «class utf8»

	tell application "Mail"
		set msg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:true, sender:theSender}
		tell msg
			make new to recipient at end of to recipients with properties {address:theTo}
			tell content
				make new attachment with properties {file name:(POSIX file attachPath)} at after the last paragraph
			end tell
		end tell
		delay 3
		save msg
		delay 2
		-- 存好后关掉撰写窗口，避免一次建很多草稿时窗口越堆越多（草稿已在草稿箱里，关窗口不影响）
		repeat with w in (every window)
			try
				if name of w is theSubject then close w saving no
			end try
		end repeat
	end tell
	return "草稿已保存（未发送）: " & theSubject
end run
