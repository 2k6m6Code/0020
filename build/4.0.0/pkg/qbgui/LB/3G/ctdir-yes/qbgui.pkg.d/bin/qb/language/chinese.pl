#!/usr/bin/perl

# Link Configuration: basic.
$lanBasic{linkconfig}="連結設定";
$lanBasic{isp_id}="ISP 編號";
$lanBasic{enable}="啟用";
$lanBasic{interface}="介面";
$lanBasic{name}="名稱";
$lanBasic{gateway}="閘道器";
$lanBasic{system_ip}="系統 IP";
$lanBasic{target_ip}="目標 IP";
$lanBasic{dsip}="DSIP";
$lanBasic{subnet}="子網段";
$lanBasic{down_up}='上傳/下載';
$lanBasic{mpv_id}="MPV 編號";
$lanBasic{state}="設定檔狀態";
$lanBasic{tdri}="TDRI";
$lanBasic{tdsi}="TDLI";
$lanBasic{thsi}="THSI";
$lanBasic{thdi}="THDI";
$lanBasic{create}="建立";
$lanBasic{delete}="刪除";
$lanBasic{restore}="回復";
$lanBasic{save}="儲存";
$lanBasic{on}="啟用";
$lanBasic{off}="停用";


# Line Check: hcconf.
$lanHcconf{link_check_parameters}="連線檢查參數";
$lanHcconf{link_check_method}="連線檢查方式";
$lanHcconf{"By Ping"}="根據 Ping";
$lanHcconf{"By Ping And Trace Route"}="根據 Ping 和 Traceroute";
$lanHcconf{"By Connection to Specified Port"}="根據連線到特定埠號";
$lanHcconf{"By Connection And Trace Route"}="根據連線到特定連接埠號和 Traceroute";
$lanHcconf{advanced_setting}="進階設定";
$lanHcconf{disable_passive_line_check}="關閉被動式連線檢查";
$lanHcconf{port}="連接埠號";
$lanHcconf{ping_time_out}="Ping 逾時";
$lanHcconf{traceroute_time_out}="Traceroute 逾時";
$lanHcconf{connection_time_out}="連線特定埠號逾時";
$lanHcconf{check_time_interval}="線路檢查間距";
$lanHcconf{save}="儲存";

# lINK IP Binding
$lanVs{isp_id}="ISP 編號";
$lanVs{name}="名稱";
$lanVs{interface}="介面";
$lanVs{public_ip}="公開 IP";
$lanVs{edit}="編輯";
$lanVs{no_isp}="ISP 尚未設定 !!";
$lanVs{public_ip_to_bind}="欲綁的公開 IP";
$lanVs{add}="加入";
$lanVs{change}="變更";


# Config Management: config.
$lanConfig{configmanage}="設定檔管理";
$lanConfig{load}="載入";
$lanConfig{save}="儲存";
$lanConfig{delete}="刪除";
$lanConfig{templet}="載入樣板";
