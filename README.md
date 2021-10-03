[![Build Status](https://app.travis-ci.com/cryofracture/cicdtemplate.svg?branch=feature-rebuild_app_env)](https://app.travis-ci.com/cryofracture/cicdtemplate)
# Cryo's CICD Template, with Casper!

An example CICD pipeline utilizing:
    
    Docker
    Pycspr
    Dockerhub image deployment
    AWS ECR publishing

    (and soon):
    AWS ECS deployment of container for interaction with

# Deploy reliably
Using various checks, ensure that no failing commit docker image is deployed to any infrastructure or public repository.


# Test securely
Tests for the pycspr image will be built to ensure longevity of the pycspr SDK.

# ECS Deployment option with Terraform
As an alternative, a terraform plan CI build will be created to ensure ECS deployment success. (WIP)

# 