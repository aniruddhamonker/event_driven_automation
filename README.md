Python StackStorm based Sensors and actions for troubleshooting Brocade VDX platform of switches.

Sensor is triggered when network device Flash disk consumption hits 90%
Action is executed upon sensor trigger to login to switch and identify list of files consuming disk space.
Action execution results contains list of disk consuming files.

[st2admin ~]$ st2 pack install https://github.com/aniruddhamonker/event_driven_automation.git

        [ succeeded ] download pack
        [ succeeded ] make a prerun
        [ succeeded ] install pack dependencies
        [ succeeded ] register pack
