#!/usr/bin/env bats

# test_run_python_script.bats

# Test if the Bash script runs the Python script and doesn't fail
@test "script runs" {

    function make() {
        echo ""
    }

    export -f make

    # change to the task directory
    cd task

    # Run the Bash script and capture the output
    run ./run.sh

    # Assert that the exit status is 0 (success)
    [ "$status" -eq 0 ]
}

