-- 列出 Mail.app 里的所有账号、对应邮箱地址和邮箱文件夹名称。
-- 用来确认 check_drafts.applescript 需要的"账号名"和"草稿箱名"。
--
-- 用法:
--   osascript scripts/list_accounts.applescript

tell application "Mail"
	set out to ""
	repeat with a in every account
		set out to out & "账号名: " & (name of a) & " | 地址: " & (email addresses of a as string) & linefeed & "  文件夹: "
		try
			repeat with mb in (every mailbox of a)
				set out to out & (name of mb) & ", "
			end repeat
		end try
		set out to out & linefeed
	end repeat
	return out
end tell
