<!-- markdownlint-disable MD025 MD033 MD060 -->
# archive-org

- Sync Repository between Several Platform

| Type | Executeable | Owner | Group | Path | Description |
|:----:|:-----------:|:-----:|:-----:|:-----|:------------|
| DIR  | FALSE | archive-org | archive-org | /home/archive-org | Home Folder |
| FILE | FALSE | archive-org | crontab | [/var/spool/cron/crontabs/archive-org](archive-org) | Task Schedule Define |
| DIR  | FALSE | archive-org | archive-org | /var/log/archive-org | Log Folder |
| FILE | FLASE | root        | root        | [/etc/logrotate.d/wayback](wayback) | Log Rotate Configure |
| DIR  | FALSE | archive-org | archive-org | /home/archive-org/bin | Bin Folder |
| FILE | TRUE  | archive-org | archive-org | [/home/archive-org/bin/wayback.py](bin/wayback.py) | Main Script |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_log.py](bin/wayback_log.py) | Define Logger |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_domain.py](bin/wayback_domain.py) | Compare Domain on URL |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_list.py](bin/wayback_list.py) | Load Archive List |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_save.py](bin/wayback_save.py) | Archive Webpage |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_site.py](bin/wayback_site.py) | Crawl Site Pages |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/bin/wayback_links.py](bin/wayback_links.py) | Extract Links from Webpate |
| DIR  | FALSE | archive-org | archive-org | /home/archive-org/etc | Environment Folder |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/etc/wayback.list](etc/wayback.list) | Archive Site List |
| FILE | FALSE | archive-org | archive-org | [/home/archive-org/etc/wayback.user-agent](etc/wayback.user-agent) | User-Agent of Request Header |
