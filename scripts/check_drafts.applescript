-- 列出某个邮箱账号草稿箱里的所有草稿：主题、发件人、收件人、附件名和大小。
-- 建完草稿后、以及发送前都用它核对一遍。
--
-- 用法:
--   osascript scripts/check_drafts.applescript "账号名" "草稿箱名"
--
-- 账号名和草稿箱名因邮箱服务商而异（例如 网易邮箱的草稿箱叫 "草稿箱"，Gmail 叫 "Drafts"），
-- 先运行 scripts/list_accounts.applescript 查看。
--
-- 说明: Mail.app 的脚本接口读不到"正在撰写的窗口"里的附件，
-- 所以一定要在草稿保存后，从草稿箱里读回来核对。

on run argv
	if (count of argv) is not 2 then error "需要 2 个参数: 账号名 草稿箱名"
	set acctName to item 1 of argv
	set boxName to item 2 of argv
	tell application "Mail"
		set out to ""
		repeat with m in (messages of mailbox boxName of account acctName)
			set out to out & "主题: " & (subject of m) & linefeed
			set out to out & "  发件人: " & (sender of m) & linefeed
			set out to out & "  收件人: "
			repeat with r in (to recipients of m)
				set out to out & (address of r) & " "
			end repeat
			set out to out & linefeed & "  抄送数: " & (count of cc recipients of m) & linefeed
			set out to out & "  附件: "
			repeat with a in (mail attachments of m)
				set out to out & (name of a) & " (" & (file size of a) & " bytes) "
			end repeat
			set out to out & linefeed
		end repeat
		if out is "" then set out to "草稿箱是空的"
		return out
	end tell
end run
