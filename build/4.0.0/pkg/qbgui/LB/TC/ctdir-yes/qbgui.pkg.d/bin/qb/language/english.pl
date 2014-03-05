#!/usr/bin/perl
$lanBasic{linkconfig}="Link Configuration";
$lanBasic{isp_id}="ISP ID";
$lanBasic{enable}="Enable";
$lanBasic{interface}="Interface";
$lanBasic{name}="Name";
$lanBasic{gateway}="Gateway";
$lanBasic{system_ip}="System IP";
$lanBasic{auth}="Auth. Type";
$lanBasic{target_ip}="Target IP";
$lanBasic{dsip}="DSIP";
$lanBasic{subnet}="Subnet";
$lanBasic{down_up}='Down/Up';

#2005-0921 Brian
$lanBasic{pppoe_name}="PPPoE's Name";
$lanBasic{pppoe_passwd}="PPPoE's Password";

#2005-0905 Brian
#$lanBasic{duplex}='Duplex';

$lanBasic{state}='State';
$lanBasic{mpv_id}="MPV ID";
$lanBasic{tdri}="TDRI";
$lanBasic{tdsi}="TDLI";
$lanBasic{thsi}="THSI";
$lanBasic{thdi}="THDI";
$lanBasic{create}="Create";
$lanBasic{delete}="Delete";
$lanBasic{restore}="Restore";
$lanBasic{save}="Save";
$lanBasic{stoppppoe}="Stop PPPoE";
$lanBasic{on}="On";
$lanBasic{off}="Off";

# Line Check: hcconf.
$lanHcconf{link_check_parameters}="Link Check Parameters";
$lanHcconf{link_check_method}="Link Check Method";
$lanHcconf{"By Ping"}="By Ping";
$lanHcconf{"By Ping And Trace Route"}="By Ping and Trace Route";
$lanHcconf{"By Connection to Specified Port"}="By Connection to Specified Port";
$lanHcconf{"By Connection And Trace Route"}="By Connection and Trace Route";
$lanHcconf{advanced_setting}="Advanced Setting";
$lanHcconf{disable_passive_line_check}="Disable Passive Line Check";
$lanHcconf{port}="Port";
$lanHcconf{ping_time_out}="Ping Time Out";
$lanHcconf{traceroute_time_out}="Traceroute Time Out";
$lanHcconf{connection_time_out}="Connection Time Out";
$lanHcconf{check_time_interval}="Check Time Interval";
$lanHcconf{save}="Save";

# Link IP Binding
$lanVs{isp_id}="ISP ID";
$lanVs{name}="Name";
$lanVs{interface}="Interface";
$lanVs{public_ip}="Public IP";
$lanVs{edit}="Edit";
$lanVs{public_ip_to_bind}="Publib IP to bind";
$laNvS{no_isp}="No ISP Configured !!";
$lanVs{add}="Add";
$lanVs{change}="Change";



# Config Management: config.
$lanConfig{configmanage}="Config. Management";
$lanConfig{load}="Load";
$lanConfig{save}="Save";
$lanConfig{delete}="Delete";
$lanConfig{templet}="Template";
