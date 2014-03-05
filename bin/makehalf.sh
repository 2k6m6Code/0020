#Format for EVAL /Q-Balancer/bin/make-release.sh 3.5.0 3G Aggregator LB EVAL_01
EVAL=$1
/Q-Balancer/bin/make-release.sh 3.5.0 TC 220 LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 420 LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 520 LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 1620 LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 1620_VM LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 2620_dual LB $EVAL
/Q-Balancer/bin/make-release.sh 3.5.0 TC 2620_dual_VM LB $EVAL

