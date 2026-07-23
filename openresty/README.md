<!-- markdownlint-disable MD025 MD033 MD060 -->
# openresty

- Publish Website

| Type | Executeable | Owner | Group | Path | Description |
|:----:|:-----------:|:-----:|:-----:|:-----|:------------|
| DIR  | FALSE | openresty | openresty | /home/openresty | Home Folder |
| FILE | FALSE | openresty | crontab   | [/var/spool/cron/crontabs/openresty](openresty) | Task Schedule Define |
| DIR  | FALSE | openresty | openresty | /var/log/openresty | Log Folder |
| FILE | FALSE | root      | root      | [/etc/logrotate.d/openresty](openresty) | Log Rotate Configure |
| LINK | FALSE | root      | root      | /etc/openresty | Openresty Service Configure<br>/usr/local/openresty/nginx/conf/ |
| FILE | FALSE | openresty | openresty | [/etc/openresty/nginx.conf](nginx.conf) | Nginx Main Configure |
| DIR  | FALSE | openresty | openresty | /etc/openresty/conf.d | Nginx Configure Folder |
| FILE | FALSE | openresty | openresty | [/etc/openresty/conf.d/site.conf](site.conf) | Main Site Configure Folder |
| FILE | FALSE | openresty | openresty | [/etc/openresty/conf.d/hook.conf](hook.conf) | Hook Site Configure Folder |
| DIR  | FALSE | openresty | openresty | /home/openresty/GitHub | Repository Storage Folder |
| DIR  | FALSE | openresty | openresty | /home/openresty/GitHub/<Repository_Name> | Repository Storage Mirror |
| DIR  | FALSE | openresty | openresty | /home/openresty/html | Site Root Folder |
| DIR  | FALSE | openresty | openresty | /home/openresty/combian | Documents Combian Download Page |
| ANY  | FALSE | openresty | openresty | /home/openresty/html/** | Main Site Pages |
| FILE | FALSE | openresty | openresty | [/home/openresty/html/hook.log](html/hook.log) | Last Hook Log Record |
| FILE | FALSE | openresty | openresty | [/home/openresty/html/hook-view.html](html/hook-view.html) | Hook Log View Page |
| DIR  | FALSE | openresty | openresty | /home/openresty/bin | Bin Folder |
| FILE | TRUE  | openresty | openresty | [/home/openresty/bin/hook.py](bin/hook.py) | Hook Master Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/hook_marker.py](bin/hook_marker.py) | Hook Single Process Locker Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/setup_logging.py](bin/setup_logging.py) | All Functions Define Log Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/load_config.py](bin/load_config.py) | All Functions Load Configure Script |
| FILE | TRUE  | openresty | openresty | [/home/openresty/bin/sync_repo.py](bin/sync_repo.py) | Repository Storage Master Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/sync_repo_git.py](bin/sync_repo_git.py) | Repository Storage Clone and Pull Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/sync_repo_loader.py](bin/sync_repo_loader.py) | Repository Storage Load Exists Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/sync_repo_show.py](bin/sync_repo_show.py) | Repository Storage Show Info Script |
| FILE | TRUE  | openresty | openresty | [/home/openresty/bin/mirror_page.py](bin/mirror_page.py) | Mirror Page Master Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/mirror_page_downloader.py](bin/mirror_page_downloader.py) | Mirror Page Download Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/mirror_page_extractor.py](bin/mirror_page_extractor.py) | Mirror Page Extractor Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/mirror_page_util.py](bin/mirror_page_util.py) | Mirror Page Other Function Script |
| FILE | TRUE  | openresty | openresty | [/home/openresty/bin/combian_pl.py](bin/combian_pl.py) | Combian Documents for "PL" Master Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_util.py](bin/combian_pl_util.py) | Combian Documents for "PL" Utils Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_front.py](bin/combian_pl_front.py) | Combian Documents for "PL" Front Matter Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_no.py](bin/combian_pl_no.py) | Combian Documents for "PL" NO_COMBIAN Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_spec.py](bin/combian_pl_spec.py) | Combian Documents for "PL" SPEC_COMBIAN Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_file.py](bin/combian_pl_file.py) | Combian Documents for "PL" FILE_COMBIAN Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_allinone.py](bin/combian_pl_allinone.py) | Combian Documents for "PL" All-In-One Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_zip.py](bin/combian_pl_.py) | Combian Documents for "PL" Packages Script |
| FILE | FALSE | openresty | openresty | [/home/openresty/bin/combian_pl_html.py](bin/combian_pl_html.py) | Combian Documents for "PL" index.html Script |
| DIR  | FALSE | openresty | openresty | /home/openresty/etc | Environment Folder |
| FILE | FALSE | openresty | openresty | [/home/openresty/etc/hook.toml](etc/hook.toml) | Configures of Hook |
| FILE | FALSE | openresty | openresty | [/home/openresty/etc/sync_repo.toml](etc/sync_repo.toml) | Configures of Repository Storage |
| FILE | FALSE | openresty | openresty | [/home/openresty/etc/mirror_page.toml](etc/mirror_page.toml) | Configures of Mirror Page |
| FILE | FALSE | openresty | openresty | [/home/openresty/etc/combian_pl.toml](etc/combian_pl.toml) | Configures of  Combian Documents for "PL" |
| FILE | FALSE | openresty | openresty | [/home/openresty/etc/geoip2.conf](etc/geoip2.conf) | License Key of GeoIP |
| DIR  | FALSE | openresty | openresty | /home/openresty/var | Variables Folder |
| FILE | FALSE | openresty | openresty | [/home/openresty/var/GeoLite2-Country.mmdb](var/GeoLite2-Country.mmdb) | IP-Location Database by Country |
