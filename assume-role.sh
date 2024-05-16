#!/bin/sh
#
# Re-assume the ACQEngAdm role from the AWS Users account that has already
# assumed the role CSD/CSP and run a command. We re-assume the role to generate
# access keys and tokens.
#
# Usage: assume-role command args...
#

if [ -z "$AWS_PROFILE" ] ; then
    echo "AWS_PROFILE must be set"
    exit 1
fi

# based on AWS_PROFILE, guess which role we want
case "$AWS_PROFILE" in
  *dev|csd)
    echo "Assuming into cloudservicesdev"
    ROLE_ARN=arn:aws:iam::672327909798:role/ACQEngAdm
    ;;
  cloudservicesprod|csp)
    echo "Assuming into cloudservicesprod"
    ROLE_ARN=arn:aws:iam::345874614325:role/ACQEngAdm
    ;;
  *)
    echo "It's not clear which account you are aiming for with $AWS_PROFILE"
    echo "Name your profile something like cloudservicesdev or cloudservicesprod"
    exit 1
    ;;
esac

# clean up the environment
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRE

AccountId=$(aws sts get-caller-identity --query Account --output text)
echo "Starting at AWS_PROFILE $AWS_PROFILE in account $AccountId"

echo "Assuming into $ROLE_ARN"
creds_json=$(aws sts assume-role --role-arn $ROLE_ARN --role-session-name $(date +%s))
export AWS_ACCESS_KEY_ID=$(echo ${creds_json} | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo ${creds_json} | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo ${creds_json} | jq -r '.Credentials.SessionToken')
export AWS_SESSION_EXPIRE=$(echo ${creds_json} | jq -r '.Credentials.Expiration')
