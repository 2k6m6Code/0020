#!/usr/bin/perl

BEGIN { unshift (@INC,"/usr/local/apache/qb/perl_lib"); }

use CGI;
use QB_Xml;

my $cgi = new CGI;
my $action = new QB_Xml;
my $service = $cgi->param('service');
my $nic = $cgi->param('isp');
my $group = $cgi->param('group');

print "Content-type:text/html\n\n";
my $ispref=$action->read("/usr/local/apache/qbconf/basic.xml");
my $isplist = $ispref->{isp};
my @ser = split(/:/,$service);
my @nic = split(/:/,$nic);

foreach my $isp (@$isplist)
{
    if (!grep(/$isp->{nic}/,@nic) || $isp->{iid} eq 'system'){next;}
    my $service_priority_list = $isp->{service};
    my @serviceupdate;
    foreach my $services (@ser)
    {
        my ($one_service,$priority) = split(/-/,$services);
        my %new_service;
    	$new_service{service}=$one_service;
    	$new_service{priority}=$priority;
    	push(@serviceupdate,\%new_service); 
    }
    $isp->{service} = \@serviceupdate; 
}
$action->write($ispref,"/usr/local/apache/qbconf/basic.xml");

if ($group)
{
    my $serref=$action->read("/usr/local/apache/qbconf/service.xml");
    my $serlist = $serref->{service};
    my @file_data;
    foreach my $ser_data (@$serlist)
    {
        push(@file_data,$ser_data);    
    }
    my %main_data;
    $main_data{title}=$group;
    $main_data{tmvdefault}='';
    $main_data{type}='sergroup';
    push(@file_data,\%main_data);
    
    $serref->{service}=\@file_data;
    
    my $serlist = $serref->{service};
    
    my @service_array;
    foreach my $services (@ser)
    {
        my ($one_service,$priority) = split(/-/,$services);
         push(@service_array,$one_service);   
    }
    my @port_input;
    foreach my $ser_data (@$serlist)
    {
        if ($ser_data->{type} eq "layer7"){next;}
        if (grep(/$ser_data->{title}/,@service_array))
        {
            my $ser_port = $ser_data->{port};
            foreach my $ser_port_data (@$ser_port)
            {
           	if ($ser_port_data->{protocol} eq 'system'){next;}
           	my %data_input_port;
           	$data_input_port{protocol}=$ser_port_data->{protocol};
           	$data_input_port{value}=$ser_port_data->{value};
    	        push(@port_input,\%data_input_port);
    	    }
        }
    }
    foreach my $ser_data (@$serlist)
    {
        if ($ser_data->{title} ne $group){next;}
        $ser_data->{port} = \@port_input;
    }
    $action->write($serref,"/usr/local/apache/qbconf/service.xml");
}
