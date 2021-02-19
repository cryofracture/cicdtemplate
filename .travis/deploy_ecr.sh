#!/bin/sh

whiel [ "$1" != "" ]; do
    case $1 in
        --aws)
        shift
        AWS_ACCOUNT=$1
        shift
        ;;
        --region)
        shift
        AWS_REGION=$1
        shift
        ;;
    esac
done

# Deploy to ECR. Needs env vars: AWS_ACCESS_KEY AWS_SECRET_ACCESS_KEY
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
#docker login -u $DOCKER_USER -p $DOCKER_PASS
if [ "$TRAVIS_BRANCH" = "master" ]; then
    TAG="latest"
else
    TAG="$TRAVIS_BRANCH"
fi
docker build -f Dockerfile -t $TRAVIS_REPO_SLUG:$TAG .
#docker push $TRAVIS_REPO_SLUG:$TAG
docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$TRAVIS_REPO_SLUG:$TAG