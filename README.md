# CICD Pipeline with Jenkins, Terraform, Docker, and ECS.

Pushes to Feature Branch are run through terraform planning. 

Pull requests are rerun through the travis jobs to reconfirm build success.

Pushes to master deploy to new cluster in Amazon ECS with required ALB, security groups, task defenition, subnets, and nodes in the cluster.

