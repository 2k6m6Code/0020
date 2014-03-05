#!/usr/bin/perl

require ('/usr/local/apache/qb/qbmod.cgi');

# ---------------------------------------------------------------
# main program start routine
# --------------------------------------------------------------
my $QB_SQUID_XMLCONF="/usr/local/apache/qbconf/pxyinit.xml";
my $QB_SQUID_CONF="/usr/local/squid/etc/squid.conf";
my $new_str;
my $statement;
my $statement1;


#------------------------------------------------------------------
# read the option from the file  /usr/local/apache/qbconf/pxyinit.xml
#------------------------------------------------------------------
my $pxyinit=XMLread($QB_SQUID_XMLCONF);

if( !$pxyinit ) #if the string is NULL
{
    print "$QB_SQUID_XMLCONF is NULL \n";
}

#------------------------------------------------------------------
# modify http_port 
#------------------------------------------------------------------
if ( $pxyinit->{pxyhttpportno})
{
    modifyfile($QB_SQUID_CONF,"http_port.*","http_port ".$pxyinit->{pxyhttpportno}." transparent"); # refresh http proxy port No.
    #modifyfile($QB_SQUID_CONF,"^#*"."http_port","http_port"); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,"^#*"."http_port","#"."http_port"); # Disable http proxy function
}

#------------------------------------------------------------------
# modify https_port 
#------------------------------------------------------------------
#if ( $pxyinit->{pxyhttpsportno})
#{
#    #modifyfile($QB_SQUID_CONF,"https_port.*","https_port ".$pxyinit->{pxyhttpsportno}." cert=/usr/local/squid/etc/cert.pem key=/usr/local/squid/etc/key.pem transparent"); # refresh https proxy port No.
#    #modifyfile($QB_SQUID_CONF,"^#*"."https_port","https_port"); # remove # character in the stateament
#}
#else
#{
#    modifyfile($QB_SQUID_CONF,"^#*"."https_port","#"."https_port"); # Disable https proxy function
#}

#------------------------------------------------------------------
# modify cache mem
#------------------------------------------------------------------
my $mem=runCommand(command=>'head', params=>'-n 1 /proc/meminfo |awk \'{print $2}\'');
my $cachemem=int( $mem /8000 );
if ( $pxyinit->{maxobj})
{
    modifyfile($QB_SQUID_CONF,"cache_mem.*","cache_mem ".$cachemem." MB"); # refresh maximum_object_size.
    modifyfile($QB_SQUID_CONF,"^#*"."cache_mem","cache_mem"); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,"^#*"."cache_mem","#"."cache_mem"); # Disable maximum_object_size function
}

#------------------------------------------------------------------
# modify maxobj 
#------------------------------------------------------------------
if ( $pxyinit->{maxobj})
{
    modifyfile($QB_SQUID_CONF,"maximum_object_size.*","maximum_object_size ".$pxyinit->{maxobj}." KB"); # refresh maximum_object_size.
    modifyfile($QB_SQUID_CONF,"^#*"."maximum_object_size","maximum_object_size"); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,"^#*"."maximum_object_size","#"."maximum_object_size"); # Disable maximum_object_size function
}

#------------------------------------------------------------------
# modify minobj 
#------------------------------------------------------------------
if ( $pxyinit->{minobj})
{
    modifyfile($QB_SQUID_CONF,"minimum_object_size.*","minimum_object_size ".$pxyinit->{minobj}." KB"); # refresh minimum_object_size.
    modifyfile($QB_SQUID_CONF,"^#*"."minimum_object_size","minimum_object_size"); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,"^#*"."minimum_object_size","#"."minimum_object_size"); # Disable minimum_object_size function
}

#------------------------------------------------------------------
# modify cache_swap_low 
#------------------------------------------------------------------
if ( $pxyinit->{replace_usage})
{
    modifyfile($QB_SQUID_CONF,"cache_swap_low.*","cache_swap_low ".$pxyinit->{replace_usage}); # refresh cache_swap_low.
    #modifyfile($QB_SQUID_CONF,"^#*"."cache_swap_low","cache_swap_low"); # remove # character in the stateament
}
else
{
    modifyfile($QB_SQUID_CONF,"^#*"."cache_swap_low","#"."cache_swap_low"); # Disable cache_swap_low function
}

#------------------------------------------------------------------
# modify cache_dir size 
#------------------------------------------------------------------
if ( $pxyinit->{pxycachesize} )
{
    modifyfile($QB_SQUID_CONF,"cache_dir.*","cache_dir ufs /mnt/tclog/squid/cache ".$pxyinit->{pxycachesize}." 8 64"); # 
}
qbSync(); #20130419 To prevent DOM/CF become readonly
