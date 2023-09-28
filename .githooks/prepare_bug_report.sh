#!/usr/bin/env bash
# Description: Generate enough info for a bug report on githooks

set -ex

CWD=$ATHENA_ROOT/src 
LOGFILE=${CWD}/githook.log
cd ${CWD}

echo "--- git rev-parse HEAD ---" > ${LOGFILE}
git rev-parse HEAD >> ${LOGFILE}

echo "--- git merge-base origin/master HEAD ---" >> ${LOGFILE}
git merge-base origin/master HEAD >> ${LOGFILE}

echo "--- hostname ---" >> ${LOGFILE}
echo "hostname $(hostname)" >> ${LOGFILE}

echo "--- git status --ignored ---" >> ${LOGFILE}
git status --ignored >> ${LOGFILE}

echo "--- git diff ---" >> ${LOGFILE}
git diff >> ${LOGFILE}

echo "------- git diff --staged -------" >> ${LOGFILE}
git diff --staged >> ${LOGFILE}

echo "------ config.json -----" >> ${LOGFILE}
cat ${CWD}/.githooks/config.json || true >> ${LOGFILE}

echo "-------- pre-commit -------" >> ${LOGFILE}
${CWD}/.githooks/pre-commit &>> ${LOGFILE}


