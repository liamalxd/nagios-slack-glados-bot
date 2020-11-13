---
A simple Slack bot to process Nagios notifications
---
**Install Instructions**

**Slack**

First you'll need to create a custom app in Slack to post notifications through.

You can do learn about this here: https://api.slack.com/start/overview

Once this is done, you should get a URL to post notifications through, along the lines of 'https://hooks.slack.com/services/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

Update WEBHOOK_URL in slack-notifications.py with this URL.

You will also need to update IMP_NOTIFY_USER with the user you wish the bot to @ when a 'UNREACHABLE','CRITICAL' or 'DOWN' alarm is triggered. (Please feel free to tweak the severity as you see fit)

**Nagios**

Personally, I have the following inside my nagios configuration:

/etc/nagios/objects/commands.cfg

```
# custom slack event handler
define command{
        command_name    notify-slack-services
        command_line    /opt/slack-notifications/slack-notifications.py "$SERVICESTATE$" "***** Nagios Service Alarm ***** Notification Type: $NOTIFICATIONTYPE$ Service: $SERVICEDESC$ Host: $HOSTALIAS$ Address: $HOSTADDRESS$ State: $SERVICESTATE$ Date/Time: $LONGDATETIME$ Additional Info: $SERVICEOUTPUT$"
        }

define command{
        command_name    notify-slack-hosts
        command_line    /opt/slack-notifications/slack-notifications.py "$HOSTSTATE$" "***** Nagios Host Alarm ***** Notification Type: $NOTIFICATIONTYPE$ Host: $HOSTNAME$ Address: $HOSTADDRESS$ State: $HOSTSTATE$ Info: $HOSTOUTPUT$ Date/Time: $LONGDATETIME$"
        }
```

/etc/nagios/objects/remotehost.cfg

```
define host{
        use                     linux-server
        host_name               mrtg
        alias                   mrtg
        address                 172.16.16.4
        hostgroups              Linux-Servers
        parents                 Zabanya Gundam
        statusmap_image         centos (1).png
        event_handler           notify-slack-hosts
}

define service{
        use                             generic-service         ; Name of service template to use
        host_name                       mrtg
        service_description             PING
        check_command                   check_ping!10.0,20%!50.0,60%
        event_handler                   notify-slack-services
}
```

This causes nagios alarms to be sent directly to the script and processed.

**Script**

As long as you have python3 installed you can install the Python required packages with:  
pip3 install -r requirements.txt
