#!/bin/bash

# test files "data/?" are compared with the expected result in "data/?_res"
# test files with captial letters are used to test the non-CIDR "-l" option

../build_docker.sh

for i in data/?; do
	[[ ${i: -1} =~ [A-Z] ]] && NO_CIDR='-l' || NO_CIDR=''
	cat "${i}" | ../run_docker.sh ${NO_CIDR} | diff "${i}_res" -
	if [ $? -ne 0 ]; then
		echo ""
		echo "Test '${i}' failed."
		echo ""
		exit 1
	fi
done

echo ""
echo "All tests sucessful"
echo ""
