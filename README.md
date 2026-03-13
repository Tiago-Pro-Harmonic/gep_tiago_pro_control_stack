What is working :
- launching full tiago pro
- navigation with cmd_vel for omni_base
- camera (head + wrist) + lidar

What is not working : 
- probleme with mimic joint for end effector. I do not see any movement activating dedicated controller


```bash
# basic launch 
ros2 launch tiago_pro_lfc_bringup tiago_pro_common.launch.py use_gazebo:=true

# launch agimus demo
ros2 launch agimus_demo_02_simple_pd_plus_tiago_pro bringup.launch.py use_gazebo:=true
```


License
---------

This software is distributed under the terms of both the MIT license and the Apache License (Version 2.0).

See LICENSE-APACHE and LICENSE-MIT for details.

Contributors
---------------
Clément Pène