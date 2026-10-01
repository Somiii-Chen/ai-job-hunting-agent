-- 发送一封求职邮件。只在用户明确说出"发送编号 X"这类指令后使用。
--
-- Mail.app 的脚本接口不能直接发送草稿箱里已存的草稿，
-- 所以这个脚本按留档的正文重新生成同样的邮件，检查发件人和收件人后再发送。
-- 发送后，草稿箱里的原草稿仍然在，记得请用户决定是否删除，避免重复发送。
--
-- 用法（参数和 create_mail_draft.applescript 完全一样）:
--   osascript scripts/send_mail.applescript \
--     "你的姓名 <you@example.com>" 正文.txt "主题" hr@company.com /绝对路径/简历.pdf

on run argv
	if (count of argv) is not 5 then error "需要 5 个参数: 发件人 正文文件 主题 收件人 附件路径"
	set theSender to item 1 of argv
	set bodyPath to item 2 of argv
	set theSubject to item 3 of argv
	set theTo to item 4 of argv
	set attachPath to item 5 of argv
	set theBody to read (POSIX file bodyPath) as «class utf8»

	-- 附件必须存在
	tell application "System Events"
		if not (exists file attachPath) then error "附件不存在: " & attachPath
	end tell

	tell application "Mail"
		set msg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:true, sender:theSender}
		tell msg
			make new to recipient at end of to recipients with properties {address:theTo}
			tell content
				make new attachment with properties {file name:(POSIX file attachPath)} at after the last paragraph
			end tell
		end tell
		delay 4

		-- 发送前最后检查
		if (count of to recipients of msg) is not 1 then error "收件人数量不对，已停止发送"
		if (address of item 1 of to recipients of msg) is not theTo then error "收件人不一致，已停止发送"
		if (count of cc recipients of msg) is not 0 or (count of bcc recipients of msg) is not 0 then error "存在抄送，已停止发送"
		if (sender of msg) does not contain theSender then error "发件人不一致，已停止发送"
		if (subject of msg) is not theSubject then error "主题不一致，已停止发送"

		send msg
	end tell
	return "已发送: " & theSubject & " -> " & theTo & "（请到'已发送'里确认附件）"
end run
