<!-- markdownlint-disable MD025 MD033 MD060 -->
# gh_backup

- Backup Pages to Archive.org

| Type | Executeable | Owner | Group | Path | Description |
|:----:|:-----------:|:-----:|:-----:|:-----|:------------|
| DIR  | FALSE | gh_backup | gh_backup | /home/gh_backup | Home Folder |
| FILE | FLASE | gh_backup | crontab | [/var/spool/cron/crontabs/gh_backup](gh_backup) | Task Schedule Define |
| DIR  | FALSE | gh_backup | gh_backup | /var/log/gh_backup | Log Folder |
| DIR  | FLASE | gh_backup | gh_backup | /home/gh_backup/bin | Bin Folder |
| DIR  | TRUE  | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup.py](bin/gh_backup.py) | Main Script |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_check.py](bin/gh_backup_check.py) | Check Configure File |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_clone.py](bin/gh_backup_clone.py) | Clone Source Repository |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_log.py](bin/gh_backup_log.py) | Define Logger |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_name.py](bin/gh_backup_name.py) | Parse Repository Name |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_push.py](bin/gh_backup_push.py) | Push Repository to Destination |
| DIR  | FLASE | gh_backup | gh_backup | [/home/gh_backup/bin/gh_backup_url.py](bin/gh_backup_url.py) | Process Git URL |
| DIR  | FLASE | gh_backup | gh_backup | /home/gh_backup/etc | Environment Folder |
| FILE | FALSE | gh_backup | gh_backup | [/home/gh_backup/etc/example_backup.yml.example](etc/example_backup.yml.example) | Configure File Example |
| MULTI-FILE | FALSE | gh_backup | gh_backup | /home/gh_backup/etc/*_backup.yml | Configure Files |
| MULTI-FILE | FALSE | gh_backup | gh_backup | /home/gh_backup/etc/*.token | Token File Used by *_backup.yml |
