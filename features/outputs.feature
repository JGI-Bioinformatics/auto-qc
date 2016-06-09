Feature: Printing different output formats
  In order to visualise the QC results
  The auto-qc tool can generate different output formats

  Scenario Outline: Generating text formatted output
   Given I create the file "analysis.yml" with the contents:
     """
     metadata:
     data:
       value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 2.0.0
     thresholds:
     - - name: example test
         fail_msg: fails
         pass_msg: passes
       - '>'
       - :value
       - <literal>
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      <result>

        * <msg>

      Auto QC Version: 2.0.0

      """

  Examples: Outputs
      | literal | result | msg    |
      | 0       | PASS   | passes |
      | 2       | FAIL   | fails  |


  Scenario Outline: Generating JSON formatted output
   Given I create the file "analysis.yml" with the contents:
     """
     metadata:
     data:
       value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 2.0.0
     thresholds:
     - - name: example test
         fail_msg: fails
         pass_msg: passes
       - '>'
       - :value
       - <literal>
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
       | --json-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      {
          "auto_qc_version": "2.0.0",
          "pass": <pass>,
          "qc": [
              {
                  "message": "<msg>",
                  "name": "example test",
                  "pass": <pass>
              }
          ]
      }

      """

  Examples: Outputs
      | literal | pass   | msg    |
      | 0       | true   | passes |
      | 2       | false  | fails  |
